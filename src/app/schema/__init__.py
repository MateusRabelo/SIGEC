from app.schema.comandoSchema import (
    ComandoBase,
    ComandoCreate,
    ComandoResponse,
)
from app.schema.dispositivoSchema import (
    DispositivoBase,
    DispositivoCreate,
    DispositivoHeartbeat,
    DispositivoResponse,
    DispositivoUpdate,
)
from app.schema.salaSchema import (
    SalaBase,
    SalaCreate,
    SalaResponse,
    SalaUpdate,
)
from app.schema.telemetriaSchema import (
    TelemetriaBase,
    TelemetriaCreate,
    TelemetriaResponse,
)

__all__ = [
    "SalaBase",
    "SalaCreate",
    "SalaUpdate",
    "SalaResponse",
    "DispositivoBase",
    "DispositivoCreate",
    "DispositivoUpdate",
    "DispositivoResponse",
    "DispositivoHeartbeat",
    "TelemetriaBase",
    "TelemetriaCreate",
    "TelemetriaResponse",
    "ComandoBase",
    "ComandoCreate",
    "ComandoResponse",
]
