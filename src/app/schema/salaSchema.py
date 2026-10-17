from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SalaBase(BaseModel):
    numero: int
    unidade: int
    bloco: int
    potencial_base_kw: float = 2.5
    setpoint_atual: float = 24.0
    ativa: bool = True


class SalaCreate(SalaBase):
    pass


class SalaUpdate(BaseModel):
    numero: int | None = None
    unidade: int | None = None
    bloco: int | None = None
    potencial_base_kw: float | None = None
    setpoint_atual: float | None = None
    ativa: bool | None = None


class SalaResponse(SalaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
