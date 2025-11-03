from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel
from datetime import date


class SalesChartItem(BaseModel):
    date: str
    total: float


class DashboardStatsResponse(BaseModel):
    sales_today: float = 0.0
    sales_week: float = 0.0
    sales_month: float = 0.0
    orders_today: int = 0
    sales_chart_30d: list[SalesChartItem] = []

    class Config:
        alias_generator = to_camel
        populate_by_name = True
