# En: app/api/dashboard/dashboard_router.py
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_db
from app.api.dashboard.dashboard_controller import DashboardController
from app.api.dashboard.dashboard_schema import DashboardStatsResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(session: Session = Depends(get_db)):
    """
    Obtener todas las estadísticas agregadas para el dashboard.
    """
    controller = DashboardController(session)
    return await controller.get_stats()
