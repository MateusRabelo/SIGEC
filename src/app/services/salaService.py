from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salaModel import SalaModel
from app.schema.salaSchema import SalaCreate, SalaUpdate


class SalaService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[SalaModel]:
        result = await db.execute(select(SalaModel).offset(skip).limit(limit))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, sala_id: int) -> SalaModel | None:
        result = await db.execute(select(SalaModel).where(SalaModel.id == sala_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_numero_unidade_bloco(
        db: AsyncSession, numero: int, unidade: int, bloco: int
    ) -> SalaModel | None:
        result = await db.execute(
            select(SalaModel).where(
                SalaModel.numero == numero,
                SalaModel.unidade == unidade,
                SalaModel.bloco == bloco,
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, sala_in: SalaCreate) -> SalaModel:
        sala = SalaModel(**sala_in.model_dump())
        db.add(sala)
        await db.commit()
        await db.refresh(sala)
        return sala

    @staticmethod
    async def update(db: AsyncSession, sala: SalaModel, sala_in: SalaUpdate) -> SalaModel:
        data = sala_in.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(sala, key, value)
        await db.commit()
        await db.refresh(sala)
        return sala

    @staticmethod
    async def delete(db: AsyncSession, sala: SalaModel) -> None:
        await db.delete(sala)
        await db.commit()
