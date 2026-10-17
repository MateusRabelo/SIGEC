from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class TelemetriaModel(Base):
    __tablename__ = "telemetrias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sala_id: Mapped[int] = mapped_column(Integer, ForeignKey("salas.id"), nullable=False)
    dispositivo_id: Mapped[int] = mapped_column(Integer, ForeignKey("dispositivos.id"), nullable=False)

    co2: Mapped[float] = mapped_column(Float, nullable=False)
    temperatura: Mapped[float] = mapped_column(Float, nullable=False)
    umidade: Mapped[float] = mapped_column(Float, nullable=True)
    corrente_rms: Mapped[float] = mapped_column(Float, nullable=False)
    potencia_ativa_kw: Mapped[float] = mapped_column(Float, nullable=False)
    setpoint: Mapped[float] = mapped_column(Float, nullable=False)
    economia_ciclo_brl: Mapped[float] = mapped_column(Float, nullable=True)
    economia_acumulada_brl: Mapped[float] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False )
    update_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False )

    