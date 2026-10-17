from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schema.salaSchema import SalaCreate, SalaResponse, SalaUpdate
from app.services.salaService import SalaService

router = APIRouter()


@router.get("", response_model=list[SalaResponse])
async def list_salas(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    return await SalaService.get_all(db, skip=skip, limit=limit)


@router.post("", response_model=SalaResponse, status_code=status.HTTP_201_CREATED)
async def create_sala(
    sala_in: SalaCreate,
    db: AsyncSession = Depends(get_db),
):
    existing = await SalaService.get_by_numero_unidade_bloco(
        db, sala_in.numero, sala_in.unidade, sala_in.bloco
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sala já cadastrada para esta unidade e bloco",
        )
    return await SalaService.create(db, sala_in)


@router.get("/{sala_id}", response_model=SalaResponse)
async def get_sala(
    sala_id: int,
    db: AsyncSession = Depends(get_db),
):
    sala = await SalaService.get_by_id(db, sala_id)
    if not sala:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala não encontrada")
    return sala


@router.patch("/{sala_id}", response_model=SalaResponse)
async def update_sala(
    sala_id: int,
    sala_in: SalaUpdate,
    db: AsyncSession = Depends(get_db),
):
    sala = await SalaService.get_by_id(db, sala_id)
    if not sala:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala não encontrada")
    return await SalaService.update(db, sala, sala_in)


@router.delete("/{sala_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sala(
    sala_id: int,
    db: AsyncSession = Depends(get_db),
):
    sala = await SalaService.get_by_id(db, sala_id)
    if not sala:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala não encontrada")
    await SalaService.delete(db, sala)
