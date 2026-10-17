import asyncio
import json
import logging
from typing import Any
import aiomqtt
from sqlalchemy import select

from app.core.config import settings
from app.core.database import async_session_maker
from app.models.dispositivoModel import DispositivoModel
from app.models.salaModel import SalaModel
from app.schema.telemetriaSchema import MqttTelemetriaPayload, TelemetriaCreate
from app.services.telemetriaService import TelemetriaService
from app.services.websocket_manager import ws_manager

logger = logging.getLogger("mqtt_worker")


async def handle_telemetry_message(topic: str, payload_bytes: bytes) -> None:
    try:
        raw_data = json.loads(payload_bytes.decode("utf-8"))
        payload = MqttTelemetriaPayload.model_validate(raw_data)
    except Exception as exc:
        logger.warning(f"Failed to parse MQTT message on {topic}: {exc}")
        return

    async with async_session_maker() as db:
        try:
            sala_result = await db.execute(select(SalaModel).where(SalaModel.id == payload.sala_id))
            sala = sala_result.scalar_one_or_none()
            if not sala:
                logger.warning(f"Sala ID {payload.sala_id} not found for telemetry")
                return

            dispositivo_id = payload.dispositivo_id
            if not dispositivo_id and payload.mac_address:
                dev_result = await db.execute(
                    select(DispositivoModel).where(DispositivoModel.mac_address == payload.mac_address)
                )
                dispositivo = dev_result.scalar_one_or_none()
                if not dispositivo:
                    dispositivo = DispositivoModel(
                        sala_id=payload.sala_id,
                        mac_address=payload.mac_address,
                        status="online",
                    )
                    db.add(dispositivo)
                    await db.flush()
                else:
                    dispositivo.registrar_heartbeat()
                    dispositivo.sala_id = payload.sala_id
                dispositivo_id = dispositivo.id
            elif dispositivo_id:
                dev_result = await db.execute(
                    select(DispositivoModel).where(DispositivoModel.id == dispositivo_id)
                )
                dispositivo = dev_result.scalar_one_or_none()
                if dispositivo:
                    dispositivo.registrar_heartbeat()

            if not dispositivo_id:
                logger.warning(f"No valid dispositivo for telemetry on {topic}")
                return

            telemetria_create = TelemetriaCreate(
                sala_id=payload.sala_id,
                dispositivo_id=dispositivo_id,
                co2=payload.co2,
                temperatura=payload.temperatura,
                umidade=payload.umidade,
                corrente_rms=payload.corrente_rms,
                potencia_ativa_kw=payload.potencia_ativa_kw,
                setpoint=payload.setpoint,
                economia_ciclo_brl=payload.economia_ciclo_brl,
                economia_acumulada_brl=payload.economia_acumulada_brl,
            )

            telemetria = await TelemetriaService.create(db, telemetria_create)

            broadcast_data = {
                "id": telemetria.id,
                "sala_id": telemetria.sala_id,
                "dispositivo_id": telemetria.dispositivo_id,
                "co2": telemetria.co2,
                "temperatura": telemetria.temperatura,
                "umidade": telemetria.umidade,
                "corrente_rms": telemetria.corrente_rms,
                "potencia_ativa_kw": telemetria.potencia_ativa_kw,
                "setpoint": telemetria.setpoint,
                "economia_ciclo_brl": telemetria.economia_ciclo_brl,
                "economia_acumulada_brl": telemetria.economia_acumulada_brl,
                "created_at": telemetria.created_at.isoformat(),
            }

            await ws_manager.broadcast_to_sala(payload.sala_id, broadcast_data)
            await ws_manager.broadcast_global(broadcast_data)
        except Exception as exc:
            await db.rollback()
            logger.error(f"Error persisting telemetry message: {exc}", exc_info=True)


async def run_mqtt_listener() -> None:
    reconnect_delay = 5
    while True:
        try:
            async with aiomqtt.Client(
                hostname=settings.MQTT_BROKER_HOST,
                port=settings.MQTT_BROKER_PORT,
                identifier=settings.MQTT_CLIENT_ID,
            ) as client:
                await client.subscribe(settings.MQTT_TOPIC_TELEMETRY)
                async for message in client.messages:
                    await handle_telemetry_message(str(message.topic), message.payload)
        except aiomqtt.MqttError:
            await asyncio.sleep(reconnect_delay)
        except asyncio.CancelledError:
            break
        except Exception:
            await asyncio.sleep(reconnect_delay)


async def publish_mqtt_command(sala_id: int, command: dict[str, Any]) -> bool:
    topic = f"ufc/campus_russas/{sala_id}/commands"
    payload = json.dumps(command)
    try:
        async with aiomqtt.Client(
            hostname=settings.MQTT_BROKER_HOST,
            port=settings.MQTT_BROKER_PORT,
            identifier=f"{settings.MQTT_CLIENT_ID}_publisher",
        ) as client:
            await client.publish(topic, payload=payload, qos=1)
            return True
    except Exception:
        return False
