# /app/models/reports/report_model.py

import enum
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Any
from sqlmodel import Field, SQLModel, JSON, Column
from sqlalchemy.dialects import postgresql as sa_pg
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy import func

# 1. Definimos el Enum (Sin cambios)
class ReportStatus(str, enum.Enum):
    en_proceso = "en_proceso"
    generado = "generado"
    error = "error"

report_status_enum = pgEnum(
    ReportStatus,
    name="reportstatus",
    create_type=False
)

# 2. Definimos el modelo
class ReportModel(SQLModel, table=True):
    __tablename__ = "reports"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )

    name: str = Field(max_length=255)
    type: str = Field(max_length=100, index=True)

    status: ReportStatus = Field(
        sa_column=Column(
            report_status_enum,
            nullable=False,
            default=ReportStatus.en_proceso,
            index=True,
        )
    )

    request_date: datetime = Field(
        sa_column=Column(
            sa_pg.TIMESTAMP(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

    # --- CAMBIO ---
    # Usaremos 'parameters' para guardar el snapshot JSON de los datos
    parameters: Optional[dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    # 'file_url' ya no se usa y se elimina
    # file_url: Optional[str] = Field(default=None, max_length=512)