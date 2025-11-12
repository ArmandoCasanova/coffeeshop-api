# /app/api/reports/report_schema.py

import enum
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Any

# --- Este Enum ya lo tenías (lo importa el repo) ---
class ReportStatus(str, enum.Enum):
    en_proceso = "en_proceso"
    generado = "generado"
    error = "error"

# --- Este es el schema de ENTRADA (ya lo tenías) ---
class ReportCreateSchema(BaseModel):
    report_type: str
    start_date: str
    end_date: str
    format: str = "pdf" # pdf o csv

# --- NUEVO: Schema de RESPUESTA ---
# Define qué campos del ReportModel se devuelven al cliente
class ReportResponseSchema(BaseModel):
    # Habilitamos el modo "ORM" para que Pydantic pueda leer
    # desde el objeto de SQLModel
    model_config = ConfigDict(from_attributes=True) 

    id: UUID
    name: str
    type: str
    status: ReportStatus # Usa el Enum
    request_date: datetime
    parameters: Optional[dict[str, Any]] = None
    file_url: Optional[str] = None

# --- NUEVO: Schema para paginación ---
# Para el endpoint GET /reports/
class PaginatedReportResponse(BaseModel):
    total: int
    reports: List[ReportResponseSchema]