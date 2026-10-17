from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DispositivoBase(BaseModel):
    sala_id: int
    mac_address: str | None = None
    modelo_chip: str | None = None
    status: str = "offline"


class DispositivoCreate(DispositivoBase):
    pass


class DispositivoUpdate(BaseModel):
    sala_id: int | None = None
    mac_address: str | None = None
    modelo_chip: str | None = None
    status: str | None = None


class DispositivoResponse(DispositivoBase):
    id: int
    last_seen: datetime

    model_config = ConfigDict(from_attributes=True)


class DispositivoHeartbeat(BaseModel):
    mac_address: str
    status: str = "online"
