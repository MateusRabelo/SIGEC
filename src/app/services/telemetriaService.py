from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.salaModel import SalaModel
from app.models.telemetriaModel import TelemetriaModel
from app.schema.telemetriaSchema import TelemetriaCreate


class TelemetriaService:
    @staticmethod
    async def get_by_id(db: AsyncSession, telemetria_id: int) -> TelemetriaModel | None:
        result = await db.execute(select(TelemetriaModel).where(TelemetriaModel.id == telemetria_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_latest_by_sala(db: AsyncSession, sala_id: int) -> TelemetriaModel | None:
        result = await db.execute(
            select(TelemetriaModel)
            .where(TelemetriaModel.sala_id == sala_id)
            .order_by(desc(TelemetriaModel.created_at))
            .limit(1)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_history_by_sala(
        db: AsyncSession, sala_id: int, limit: int = 100
    ) -> list[TelemetriaModel]:
        result = await db.execute(
            select(TelemetriaModel)
            .where(TelemetriaModel.sala_id == sala_id)
            .order_by(desc(TelemetriaModel.created_at))
            .limit(limit)
        )
        records = list(result.scalars().all())
        records.reverse()
        return records

    @staticmethod
    async def create(db: AsyncSession, telemetria_in: TelemetriaCreate) -> TelemetriaModel:
        data = telemetria_in.model_dump()

        if data.get("economia_ciclo_brl") is None:
            sala_result = await db.execute(select(SalaModel).where(SalaModel.id == telemetria_in.sala_id))
            sala = sala_result.scalar_one_or_none()
            baseline = sala.potencial_base_kw if sala else settings.BASELINE_POWER_KW
            saved_kw = max(0.0, baseline - telemetria_in.potencia_ativa_kw)
            cycle_economy = (saved_kw * (1.0 / 60.0)) * settings.DEFAULT_TARIFF_KWH
            data["economia_ciclo_brl"] = round(cycle_economy, 4)

        if data.get("economia_acumulada_brl") is None:
            latest = await TelemetriaService.get_latest_by_sala(db, telemetria_in.sala_id)
            prev_accum = latest.economia_acumulada_brl if latest and latest.economia_acumulada_brl else 0.0
            data["economia_acumulada_brl"] = round(prev_accum + (data["economia_ciclo_brl"] or 0.0), 4)

        telemetria = TelemetriaModel(**data)
        db.add(telemetria)
        await db.commit()
        await db.refresh(telemetria)
        return telemetria
