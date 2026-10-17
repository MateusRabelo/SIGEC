from fastapi import APIRouter

from app.api.comandoRouter import router as comando_router
from app.api.dispositivoRouter import router as dispositivo_router
from app.api.salaRouter import router as sala_router
from app.api.telemetriaRouter import router as telemetria_router
from app.api.wsRouter import router as ws_router

router = APIRouter()


@router.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}


router.include_router(sala_router, prefix="/salas", tags=["salas"])
router.include_router(dispositivo_router, prefix="/dispositivos", tags=["dispositivos"])
router.include_router(telemetria_router, prefix="/telemetrias", tags=["telemetrias"])
router.include_router(comando_router, prefix="/comandos", tags=["comandos"])
router.include_router(ws_router, prefix="/ws", tags=["websocket"])
