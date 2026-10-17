from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TelemetriaBase(BaseModel):
    sala_id: int
    dispositivo_id: int
    co2: float
    temperatura: float
    umidade: float | None = None
    corrente_rms: float
    potencia_ativa_kw: float
    setpoint: float
    economia_ciclo_brl: float | None = None
    economia_acumulada_brl: float | None = None


class TelemetriaCreate(TelemetriaBase):
    pass


class TelemetriaResponse(TelemetriaBase):
    id: int
    created_at: datetime
    update_at: datetime

    model_config = ConfigDict(from_attributes=True)
