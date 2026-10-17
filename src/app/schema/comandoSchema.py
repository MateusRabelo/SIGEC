from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ComandoBase(BaseModel):
    sala_id: int
    acao: str
    setpoint_alvo: str


class ComandoCreate(ComandoBase):
    pass


class ComandoResponse(ComandoBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
