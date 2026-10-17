import json
from typing import Any
from fastapi import WebSocket


class WebSocketManager:
    def __init__(self) -> None:
        self.active_connections: dict[int, list[WebSocket]] = {}
        self.global_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, sala_id: int | None = None) -> None:
        await websocket.accept()
        if sala_id is not None:
            if sala_id not in self.active_connections:
                self.active_connections[sala_id] = []
            self.active_connections[sala_id].append(websocket)
        else:
            self.global_connections.append(websocket)

    def disconnect(self, websocket: WebSocket, sala_id: int | None = None) -> None:
        if sala_id is not None and sala_id in self.active_connections:
            if websocket in self.active_connections[sala_id]:
                self.active_connections[sala_id].remove(websocket)
            if not self.active_connections[sala_id]:
                del self.active_connections[sala_id]
        elif websocket in self.global_connections:
            self.global_connections.remove(websocket)

    async def broadcast_to_sala(self, sala_id: int, message: dict[str, Any]) -> None:
        if sala_id in self.active_connections:
            data = json.dumps(message)
            disconnected: list[WebSocket] = []
            for connection in self.active_connections[sala_id]:
                try:
                    await connection.send_text(data)
                except Exception:
                    disconnected.append(connection)
            for connection in disconnected:
                self.disconnect(connection, sala_id)

    async def broadcast_global(self, message: dict[str, Any]) -> None:
        data = json.dumps(message)
        disconnected: list[WebSocket] = []
        for connection in self.global_connections:
            try:
                await connection.send_text(data)
            except Exception:
                disconnected.append(connection)
        for connection in disconnected:
            self.disconnect(connection)


ws_manager = WebSocketManager()
