from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schema.comandoSchema import ComandoCreate, ComandoResponse
from app.services.comandoService import ComandoService
from app.services.salaService import SalaService

router = APIRouter()


@router.post("", response_model=ComandoResponse, status_code=status.HTTP_201_CREATED)
async def create_comando(
    comando_in: ComandoCreate,
    db: AsyncSession = Depends(get_db),
):
    sala = await SalaService.get_by_id(db, comando_in.sala_id)
    if not sala:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala não encontrada")
    return await ComandoService.create(db, comando_in)


@router.get("/sala/{sala_id}", response_model=list[ComandoResponse])
async def list_comandos_by_sala(
    sala_id: int,
    limit: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    sala = await SalaService.get_by_id(db, sala_id)
    if not sala:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala não encontrada")
    return await ComandoService.get_by_sala(db, sala_id, limit=limit)
