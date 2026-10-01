from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SalaModel(Base):
    __tablename__ = "salas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numero: Mapped[int] = mapped_column(Integer, nullable=False)
    unidade: Mapped[int] = mapped_column(Integer, nullable=False)
    bloco: Mapped[int] = mapped_column(Integer, nullable=False)
    potencial_base_kw: Mapped[float] = mapped_column(Float, nullable=False, default=2.5)
    setpoint_atual: Mapped[float] = mapped_column(Float, nullable=False, default=24.0)
    ativa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
