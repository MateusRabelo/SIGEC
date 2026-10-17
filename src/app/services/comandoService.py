from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comandoModel import ComandoModel
from app.models.salaModel import SalaModel
from app.schema.comandoSchema import ComandoCreate


class ComandoService:
    @staticmethod
    async def get_by_id(db: AsyncSession, comando_id: int) -> ComandoModel | None:
        result = await db.execute(select(ComandoModel).where(ComandoModel.id == comando_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_sala(db: AsyncSession, sala_id: int, limit: int = 50) -> list[ComandoModel]:
        result = await db.execute(
            select(ComandoModel)
            .where(ComandoModel.sala_id == sala_id)
            .order_by(desc(ComandoModel.created_at))
            .limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def create(db: AsyncSession, comando_in: ComandoCreate) -> ComandoModel:
        comando = ComandoModel(**comando_in.model_dump())
        db.add(comando)

        if comando_in.setpoint_alvo:
            try:
                target_temp = float(comando_in.setpoint_alvo)
                sala_result = await db.execute(select(SalaModel).where(SalaModel.id == comando_in.sala_id))
                sala = sala_result.scalar_one_or_none()
                if sala:
                    sala.setpoint_atual = target_temp
            except ValueError:
                pass

        await db.commit()
        await db.refresh(comando)
        return comando
