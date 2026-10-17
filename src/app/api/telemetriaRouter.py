from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schema.telemetriaSchema import TelemetriaCreate, TelemetriaResponse
from app.services.dispositivoService import DispositivoService
from app.services.salaService import SalaService
from app.services.telemetriaService import TelemetriaService

router = APIRouter()


@router.post("", response_model=TelemetriaResponse, status_code=status.HTTP_201_CREATED)
async def create_telemetria(
    telemetria_in: TelemetriaCreate,
    db: AsyncSession = Depends(get_db),
):
    sala = await SalaService.get_by_id(db, telemetria_in.sala_id)
    if not sala:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala não encontrada")

    dispositivo = await DispositivoService.get_by_id(db, telemetria_in.dispositivo_id)
    if not dispositivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado")

    return await TelemetriaService.create(db, telemetria_in)


@router.get("/sala/{sala_id}/latest", response_model=TelemetriaResponse)
async def get_latest_telemetria(
    sala_id: int,
    db: AsyncSession = Depends(get_db),
):
    telemetria = await TelemetriaService.get_latest_by_sala(db, sala_id)
    if not telemetria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma telemetria encontrada para esta sala",
        )
    return telemetria


@router.get("/sala/{sala_id}/history", response_model=list[TelemetriaResponse])
async def get_history_telemetria(
    sala_id: int,
    limit: int = Query(default=100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    sala = await SalaService.get_by_id(db, sala_id)
    if not sala:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala não encontrada")
    return await TelemetriaService.get_history_by_sala(db, sala_id, limit=limit)
