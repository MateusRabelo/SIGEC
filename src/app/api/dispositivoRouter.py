from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schema.dispositivoSchema import (
    DispositivoCreate,
    DispositivoHeartbeat,
    DispositivoResponse,
    DispositivoUpdate,
)
from app.services.dispositivoService import DispositivoService
from app.services.salaService import SalaService

router = APIRouter()


@router.get("", response_model=list[DispositivoResponse])
async def list_dispositivos(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    return await DispositivoService.get_all(db, skip=skip, limit=limit)


@router.post("", response_model=DispositivoResponse, status_code=status.HTTP_201_CREATED)
async def create_dispositivo(
    dispositivo_in: DispositivoCreate,
    db: AsyncSession = Depends(get_db),
):
    sala = await SalaService.get_by_id(db, dispositivo_in.sala_id)
    if not sala:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala associada não encontrada")
    if dispositivo_in.mac_address:
        existing = await DispositivoService.get_by_mac(db, dispositivo_in.mac_address)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dispositivo com este MAC address já cadastrado",
            )
    return await DispositivoService.create(db, dispositivo_in)


@router.get("/{dispositivo_id}", response_model=DispositivoResponse)
async def get_dispositivo(
    dispositivo_id: int,
    db: AsyncSession = Depends(get_db),
):
    dispositivo = await DispositivoService.get_by_id(db, dispositivo_id)
    if not dispositivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado")
    return dispositivo


@router.get("/sala/{sala_id}", response_model=list[DispositivoResponse])
async def list_dispositivos_by_sala(
    sala_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await DispositivoService.get_by_sala(db, sala_id)


@router.patch("/{dispositivo_id}", response_model=DispositivoResponse)
async def update_dispositivo(
    dispositivo_id: int,
    dispositivo_in: DispositivoUpdate,
    db: AsyncSession = Depends(get_db),
):
    dispositivo = await DispositivoService.get_by_id(db, dispositivo_id)
    if not dispositivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado")
    return await DispositivoService.update(db, dispositivo, dispositivo_in)


@router.post("/heartbeat", response_model=DispositivoResponse)
async def register_heartbeat(
    heartbeat_in: DispositivoHeartbeat,
    db: AsyncSession = Depends(get_db),
):
    dispositivo = await DispositivoService.heartbeat(db, heartbeat_in.mac_address)
    if not dispositivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado")
    return dispositivo


@router.delete("/{dispositivo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dispositivo(
    dispositivo_id: int,
    db: AsyncSession = Depends(get_db),
):
    dispositivo = await DispositivoService.get_by_id(db, dispositivo_id)
    if not dispositivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado")
    await DispositivoService.delete(db, dispositivo)
