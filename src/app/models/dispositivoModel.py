from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DispositivoModel(Base):
    __tablename__ = "dispositivos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sala_id: Mapped[int] = mapped_column(Integer, ForeignKey("salas.id"))
    mac_address: Mapped[str | None] = mapped_column(String, nullable=True)
    modelo_chip: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="offline")
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)



    def registrar_heartbeat(self) -> None:
        self.last_seen = datetime.now(timezone.utc)
        self.status = "online"


    def isOnline(self, timeout_segundos: int = 60) -> bool:
        if not self.last_seen:
            self.status = "offline"
            return False

        agora = datetime.now(timezone.utc)
        last_seen = self.last_seen if self.last_seen.tzinfo else self.last_seen.replace(tzinfo=timezone.utc)

        isOnline = (agora - last_seen).total_seconds() <= timeout_segundos
        if not isOnline:
            self.status = "offline"

        return isOnline