# /app/api/reports/report_repository.py

from typing import Optional, List, Tuple
from sqlmodel import Session, select, func
from uuid import UUID
import logging

# Importa el modelo y el schema
from app.models.reports.report_model import ReportModel, ReportStatus
from app.api.reports.report_schema import ReportStatus as ReportStatusSchema

logger = logging.getLogger(__name__)

class ReportRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_report(self, report_data: dict) -> ReportModel:
        """
        Crea un nuevo registro de reporte en la BBDD.
        Es una operación síncrona.
        """
        try:
            # Crea la instancia del modelo con los datos del servicio
            new_report = ReportModel(**report_data)
            self.session.add(new_report)
            self.session.commit()
            self.session.refresh(new_report)
            return new_report
        except Exception:
            self.session.rollback()
            logger.error("Error al crear el reporte en BBDD", exc_info=True)
            raise

    def get_report_by_id(self, report_id: UUID) -> Optional[ReportModel]:
        """
        Busca un reporte por su columna 'id'.
        Como 'id' no es Primary Key, esta consulta será lenta.
        """
        try:
            statement = select(ReportModel).where(ReportModel.id == report_id)
            report = self.session.exec(statement).first()
            return report
        except Exception:
            logger.error(f"Error al buscar reporte por ID {report_id}", exc_info=True)
            raise

    def get_all_reports(
        self,
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
        status: Optional[ReportStatusSchema] = None,
        report_type: Optional[str] = None,
    ) -> Tuple[List[ReportModel], int]:
        """
        Obtiene una lista paginada de reportes con filtros.
        """
        try:
            # Construcción de la consulta base
            query = select(ReportModel)
            
            # Aplicar filtros
            if search:
                query = query.where(ReportModel.name.ilike(f"%{search}%"))
            if status:
                # Comparamos el valor del Enum
                query = query.where(ReportModel.status == status.value)
            if report_type:
                query = query.where(ReportModel.type == report_type)

            # Clonar la query para contar el total ANTES de paginar
            # Esto es más eficiente que traer todos los resultados
            total_query = select(func.count()).select_from(query.subquery())
            total = self.session.exec(total_query).one()

            # Aplicar paginación y orden
            results_query = query.order_by(ReportModel.request_date.desc()).offset(skip).limit(limit)
            reports = self.session.exec(results_query).all()

            return list(reports), total
        except Exception:
            logger.error("Error al obtener todos los reportes", exc_info=True)
            raise

    def delete_report(self, report_id: UUID) -> bool:
        """
        Elimina un reporte de la BBDD usando su 'id'.
        Esta operación también será lenta.
        """
        try:
            # Primero buscamos el reporte
            report = self.get_report_by_id(report_id)
            if not report:
                return False # No se encontró, nada que borrar

            # Si se encontró, se elimina
            self.session.delete(report)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            logger.error(f"Error al eliminar el reporte {report_id}", exc_info=True)
            raise

    # --- Métodos para la Tarea en Segundo Plano ---
    # Estos métodos serán llamados por 'generate_report_task'
    
    def update_report_task_complete(self, report_id: UUID, file_url: str) -> Optional[ReportModel]:
        """Actualiza el reporte a 'generado' y guarda la URL del archivo."""
        try:
            report = self.get_report_by_id(report_id)
            if not report:
                logger.error(f"TASK_ERROR: No se encontró reporte {report_id} para actualizar.")
                return None
            
            report.status = ReportStatus.generado
            report.file_url = file_url
            
            self.session.add(report)
            self.session.commit()
            self.session.refresh(report)
            return report
        except Exception:
            self.session.rollback()
            logger.error(f"Error actualizando reporte {report_id} a completado", exc_info=True)
            raise

    def update_report_task_error(self, report_id: UUID) -> Optional[ReportModel]:
        """Actualiza el reporte a 'error'."""
        try:
            report = self.get_report_by_id(report_id)
            if not report:
                logger.error(f"TASK_ERROR: No se encontró reporte {report_id} para marcar como error.")
                return None
            
            report.status = ReportStatus.error
            
            self.session.add(report)
            self.session.commit()
            self.session.refresh(report)
            return report
        except Exception:
            self.session.rollback()
            logger.error(f"Error actualizando reporte {report_id} a error", exc_info=True)
            raise