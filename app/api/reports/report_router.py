# /app/api/reports/report_router.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse # <-- IMPORTANTE
import io # <-- IMPORTANTE
from sqlmodel import Session
from uuid import UUID
from typing import Optional, List
import logging # <-- Añadido

# Dependencia para la sesión de BBDD
from app.core.database import get_db

# Importaciones del módulo de reportes
from app.api.reports.report_service import ReportService
from app.api.reports.report_schema import (
    ReportCreateSchema, # <-- REVERTIDO: Usamos el schema de creación
    ReportResponseSchema,
    PaginatedReportResponse,
    ReportStatus
)

# Creamos el router
router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

logger = logging.getLogger(__name__)

# --- Dependencia para el Servicio (Sin cambios) ---
def get_report_service(session: Session = Depends(get_db)) -> ReportService:
    return ReportService(session)

# --- Definición de Endpoints ---

@router.post(
    "/",
    response_model=ReportResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Solicita un nuevo reporte (Guarda Data-Snapshot)"
)
async def request_new_report(
    # --- REVERTIDO: Aceptamos JSON, no Forms ---
    report_data: ReportCreateSchema, 
    service: ReportService = Depends(get_report_service)
):
    """
    Crea un registro de reporte.
    
    1.  Recibe parámetros (fechas, tipo).
    2.  El servicio consulta las tablas de datos (ej. Ventas).
    3.  Guarda un snapshot JSON de esos datos en la BBDD.
    4.  Responde con el reporte (estado 'generado').
    """
    try:
        # --- REVERTIDO: Llamamos al nuevo servicio 'create_report_snapshot' ---
        new_report = await service.create_report_snapshot(report_data)
        
        if not new_report:
             raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="El servicio de reportes falló pero no lanzó excepción."
            )
        return new_report
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error no controlado en router request_new_report: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar la solicitud de reporte"
        )


# --- NUEVO ENDPOINT DE DESCARGA DINÁMICA ---
@router.get(
    "/{report_id}/download",
    summary="Genera y descarga el archivo del reporte (PDF/XLSX)",
    response_class=StreamingResponse # Importante: no devuelve JSON
)
async def download_report_file(
    report_id: UUID,
    service: ReportService = Depends(get_report_service)
):
    """
    Genera un archivo (PDF o Excel) en memoria basado en el
    snapshot de datos guardado y lo envía al cliente.
    """
    try:
        # 1. El servicio genera el archivo en memoria
        file_buffer, filename, media_type = await service.generate_file_from_snapshot(report_id)
        
        # 2. Definimos headers para forzar la descarga
        headers = {
            # Esto le dice al navegador que lo descargue vs. mostrarlo
            'Content-Disposition': f'attachment; filename="{filename}"'
        }

        # 3. Enviamos el buffer como un stream
        return StreamingResponse(
            content=file_buffer,
            media_type=media_type,
            headers=headers
        )
    except Exception as e:
        logger.error(f"Error al generar descarga para {report_id}: {e}", exc_info=True)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Error al generar el archivo")


# --- LOS OTROS ENDPOINTS (GET, DELETE) COMPLETOS ---
# (Tomados de tu archivo original)

@router.get(
    "/",
    response_model=PaginatedReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener historial de reportes"
)
async def get_reports_history(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = Query(None, description="Buscar por nombre"),
    status: Optional[ReportStatus] = Query(None, description="Filtrar por estado"),
    report_type: Optional[str] = Query(None, alias="type", description="Filtrar por tipo"),
    service: ReportService = Depends(get_report_service)
):
    reports, total = await service.get_all_reports(
        skip=skip, 
        limit=limit, 
        search=search, 
        status=status, 
        report_type=report_type
    )
    return PaginatedReportResponse(total=total, reports=reports)


@router.get(
    "/{report_id}",
    response_model=ReportResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Obtener un reporte por ID"
)
async def get_report_by_id(
    report_id: UUID,
    service: ReportService = Depends(get_report_service)
):
    report = await service.get_report_by_id(report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado"
        )
    return report

@router.delete(
    "/{report_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un reporte"
)
async def delete_report(
    report_id: UUID,
    service: ReportService = Depends(get_report_service)
):
    success = await service.delete_report(report_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado, no se pudo eliminar"
        )
    return None