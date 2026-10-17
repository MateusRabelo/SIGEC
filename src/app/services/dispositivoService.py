from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dispositivoModel import DispositivoModel


class DispositivoService:

    @staticmethod
    async def registrar_heartbeat(session: AsyncSession, mac_address: str, sala_id: int | None = None, modelo_chip: str = "ESP32") -> DispositivoModel:
        """
        Localiza o dispositivo pelo MAC address e registra o heartbeat.
        Se ainda não existir no banco, cria um novo dispositivo automaticamente.
        """
        
        stmt = select(DispositivoModel).where(DispositivoModel.mac_address == mac_address)

        result = await session.execute(stmt)

        # verifica se existe
        dispositivo = result.scalar_one_or_none()

        if not dispositivo:
            dispositivo = DispositivoModel(
                mac_address=mac_address,
                sala_id=sala_id,
                modelo_chip=modelo_chip,
                status="online",
                last_seen=datetime.now(timezone.utc),
            )
            session.add(dispositivo)
        else:
            dispositivo.registrar_heartbeat()

        await session.commit()
        await session.refresh(dispositivo)
        return dispositivo



    @staticmethod
    async def get_by_id(session: AsyncSession, dispositivo_id: int) -> DispositivoModel | None:
        """Busca um dispositivo pelo ID."""

        stmt = select(DispositivoModel).where(DispositivoModel.id == dispositivo_id)
        result = await session.execute(stmt)

        return result.scalar_one_or_none() #não perm9te ignorar se não for único



    @staticmethod
    async def get_by_sala_id(session: AsyncSession, sala_id: int) -> list[DispositivoModel]:
        """Retorna todos os dispositivos de uma determinada sala."""

        stmt = select(DispositivoModel).where(DispositivoModel.sala_id == sala_id)
        result = await session.execute(stmt)

        return list(result.scalars().all())



    @staticmethod
    async def update_offline_dispositivos(session: AsyncSession, timeout_segundos: int = 60) -> int:
        """
        Varre dispositivos que constam como 'online' e marca como 'offline'
        aqueles cujo last_seen ultrapassou o limite.
        """

        stmt = select(DispositivoModel).where(DispositivoModel.status == "online")
        
        result = await session.execute(stmt)
        dispositivos = result.scalars().all()

        modificados = 0
        for disp in dispositivos:
            if not disp.isOnline(timeout_segundos=timeout_segundos):
                modificados += 1

        if modificados > 0:
            await session.commit()

        return modificados
