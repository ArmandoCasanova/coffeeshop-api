# /app/api/reports/report_service.py

from app.core.http_response import CoffeeAppHttpResponse
from typing import Optional, Tuple, List, Any
from sqlmodel import Session
from fastapi import HTTPException # <-- Importar HTTPException
from uuid import UUID
import logging

# --- NUEVAS IMPORTACIONES PARA GENERACIÓN DE ARCHIVOS ---
import io
import openpyxl # (Recuerda: pip install openpyxl)
from reportlab.pdfgen import canvas # (Recuerda: pip install reportlab)
# --- FIN DE NUEVAS IMPORTACIONES ---

# Importaciones del módulo de reportes
# Importamos el Schema de creación que usaremos
from app.api.reports.report_schema import ReportCreateSchema, ReportStatus
from app.api.reports.report_repository import ReportRepository
from app.models.reports.report_model import ReportModel

logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = ReportRepository(session)
        # Ya no necesitamos crear directorios 'static'

    # --- Función para crear el Snapshot ---
    async def create_report_snapshot(
        self, report_data: ReportCreateSchema
    ) -> ReportModel:
        """
        Consulta datos de otras tablas y guarda un snapshot JSON.
        """
        
        logger.info(f"Creando snapshot para reporte tipo: {report_data.report_type}")

        # 1. (SIMULACIÓN) Aquí consultarías otras tablas
        try:
            data_snapshot = {
                "report_format": report_data.format, # Guardamos el formato
                "title": f"Reporte de {report_data.report_type}",
                "range": f"{report_data.start_date} a {report_data.end_date}",
                "generated_by": "system",
                "simulated_sales": [
                    {"item": "Café Americano", "qty": 50, "total": 2500},
                    {"item": "Croissant", "qty": 30, "total": 1800},
                    {"item": "Té Verde", "qty": 25, "total": 1250},
                ]
            }
        except Exception as e:
            logger.error(f"Error al simular la consulta de datos: {e}", exc_info=True)
            CoffeeAppHttpResponse.internal_error("Error al consultar los datos para el reporte")
        
        report_name = (
            f"Reporte de {report_data.report_type} "
            f"({report_data.start_date} a {report_data.end_date})"
        )
        
        # 2. Guardamos el snapshot en 'parameters'
        db_data = {
            "name": report_name,
            "type": report_data.report_type,
            "status": ReportStatus.generado, # Se genera al instante
            "parameters": data_snapshot, # <-- AQUI VA EL JSON
        }
        
        try:
            new_report = self.repository.create_report(db_data)
            logger.info(f"Snapshot de reporte {new_report.id} guardado.")
            return new_report
        except Exception as e:
            logger.error(f"Error al guardar el snapshot en BBDD: {e}", exc_info=True)
            CoffeeAppHttpResponse.internal_error("Error al guardar el registro del reporte")

    # --- Función para generar el archivo ---
    async def generate_file_from_snapshot(self, report_id: UUID) -> Tuple[io.BytesIO, str, str]:
        """
        Lee el JSON de la BBDD y genera un archivo en memoria.
        """
        logger.info(f"Iniciando generación de archivo para reporte {report_id}")
        
        report = await self.get_report_by_id(report_id)
        if not report or not report.parameters:
            logger.warning(f"Reporte o datos no encontrados para {report_id}")
            raise HTTPException(status_code=404, detail="Reporte o datos no encontrados")
            
        data = report.parameters
        file_format = data.get("report_format", "pdf") # Default a 'pdf'

        buffer = io.BytesIO()

        try:
            # --- ¡ESTA ES LA LÍNEA DE LA CORRECCIÓN! ---
            # Aceptamos 'xlsx' O 'excel'
            if file_format == "xlsx" or file_format == "excel":
                
                # --- Lógica de EXCEL (con openpyxl) ---
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Reporte"
                
                ws.append([data.get("title", "Reporte")])
                ws.append([data.get("range", "")])
                ws.append([]) # Línea vacía
                ws.append(["Item", "Cantidad", "Total"])
                
                for item in data.get("simulated_sales", []):
                    ws.append([item["item"], item["qty"], item["total"]])

                wb.save(buffer) # Guarda el Excel en el buffer
                
                filename = f"{report.name.replace(' ', '_')}.xlsx"
                media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            else:
                # --- Lógica de PDF (con reportlab) ---
                p = canvas.Canvas(buffer)
                p.drawString(100, 800, data.get("title", "Reporte"))
                p.drawString(100, 780, data.get("range", ""))
                
                y = 750
                p.drawString(100, y, "Item - Cantidad - Total")
                y -= 20
                for item in data.get("simulated_sales", []):
                    p.drawString(100, y, f"{item['item']} - Qty: {item['qty']} - Total: {item['total']}")
                    y -= 20
                    
                p.showPage()
                p.save() # Guarda el PDF en el buffer

                filename = f"{report.name.replace(' ', '_')}.pdf"
                media_type = "application/pdf"

        except Exception as e:
            logger.error(f"Error al generar el archivo en memoria: {e}", exc_info=True)
            CoffeeAppHttpResponse.internal_error("Error al construir el archivo")

        buffer.seek(0) # Rebobinamos el buffer al inicio
        logger.info(f"Archivo {filename} generado en memoria.")
        return buffer, filename, media_type

    # --- Los otros métodos (get/delete) se mantienen ---

    async def get_report_by_id(self, report_id: UUID) -> Optional[ReportModel]:
        try:
            return self.repository.get_report_by_id(report_id)
        except Exception as e:
            logger.error(f"Error en service get_report_by_id: {e}", exc_info=True)
            CoffeeAppHttpResponse.internal_error()

    async def get_all_reports(
        self,
        skip: int,
        limit: int,
        search: Optional[str],
        status: Optional[ReportStatus],
        report_type: Optional[str],
    ) -> Tuple[List[ReportModel], int]:
        try:
            return self.repository.get_all_reports(
                skip=skip,
                limit=limit,
                search=search,
                status=status,
                report_type=report_type,
            )
        except Exception as e:
            logger.error(f"Error en service get_all_reports: {e}", exc_info=True)
            CoffeeAppHttpResponse.internal_error()

    async def delete_report(self, report_id: UUID) -> bool:
        try:
            return self.repository.delete_report(report_id)
        except Exception as e:
            logger.error(f"Error en service delete_report: {e}", exc_info=True)
            CoffeeAppHttpResponse.internal_error()