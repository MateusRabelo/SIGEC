from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dispositivoModel import DispositivoModel
from app.schema.dispositivoSchema import DispositivoCreate, DispositivoUpdate


class DispositivoService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[DispositivoModel]:
        result = await db.execute(select(DispositivoModel).offset(skip).limit(limit))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, dispositivo_id: int) -> DispositivoModel | None:
        result = await db.execute(select(DispositivoModel).where(DispositivoModel.id == dispositivo_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_mac(db: AsyncSession, mac_address: str) -> DispositivoModel | None:
        result = await db.execute(select(DispositivoModel).where(DispositivoModel.mac_address == mac_address))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_sala(db: AsyncSession, sala_id: int) -> list[DispositivoModel]:
        result = await db.execute(select(DispositivoModel).where(DispositivoModel.sala_id == sala_id))
        return list(result.scalars().all())

    @staticmethod
    async def create(db: AsyncSession, dispositivo_in: DispositivoCreate) -> DispositivoModel:
        dispositivo = DispositivoModel(**dispositivo_in.model_dump())
        db.add(dispositivo)
        await db.commit()
        await db.refresh(dispositivo)
        return dispositivo

    @staticmethod
    async def update(
        db: AsyncSession, dispositivo: DispositivoModel, dispositivo_in: DispositivoUpdate
    ) -> DispositivoModel:
        data = dispositivo_in.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(dispositivo, key, value)
        await db.commit()
        await db.refresh(dispositivo)
        return dispositivo

    @staticmethod
    async def heartbeat(db: AsyncSession, mac_address: str) -> DispositivoModel | None:
        result = await db.execute(select(DispositivoModel).where(DispositivoModel.mac_address == mac_address))
        dispositivo = result.scalar_one_or_none()
        if not dispositivo:
            return None
        dispositivo.registrar_heartbeat()
        await db.commit()
        await db.refresh(dispositivo)
        return dispositivo

    @staticmethod
    async def delete(db: AsyncSession, dispositivo: DispositivoModel) -> None:
        await db.delete(dispositivo)
        await db.commit()
