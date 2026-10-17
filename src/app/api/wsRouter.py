from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.websocket_manager import ws_manager

router = APIRouter()


@router.websocket("/salas/{sala_id}")
async def websocket_sala_endpoint(websocket: WebSocket, sala_id: int):
    await ws_manager.connect(websocket, sala_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, sala_id)


@router.websocket("/live")
async def websocket_global_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
