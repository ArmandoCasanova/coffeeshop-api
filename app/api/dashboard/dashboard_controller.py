from sqlmodel import Session, select, func
from datetime import datetime, timedelta
from .dashboard_schema import DashboardStatsResponse, SalesChartItem
from app.models.orders.order_model import OrderModel


class DashboardController:
    def __init__(self, session: Session):
        self.session = session

    def _get_sales_sum(self, start_date: datetime, end_date: datetime) -> float:
        query = select(func.sum(OrderModel.total_amount)).where(
            OrderModel.order_date >= start_date,
            OrderModel.order_date < end_date,
            OrderModel.status == "paid",
        )
        result = self.session.exec(query).first()
        return result if result else 0.0

    def _get_order_count(self, start_date: datetime, end_date: datetime) -> int:
        query = select(func.count(OrderModel.order_id)).where(
            OrderModel.order_date >= start_date,
            OrderModel.order_date < end_date,
            OrderModel.status == "paid",
        )
        result = self.session.exec(query).first()
        return result if result else 0

    async def get_stats(self) -> DashboardStatsResponse:
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        week_start = today_start - timedelta(days=now.weekday())
        month_start = today_start.replace(day=1)

        sales_today = self._get_sales_sum(today_start, today_end)
        sales_week = self._get_sales_sum(week_start, today_end)
        sales_month = self._get_sales_sum(month_start, today_end)
        orders_today = self._get_order_count(today_start, today_end)

        start_30d = today_start - timedelta(days=29)

        date_day = func.date_trunc("day", OrderModel.order_date).label("date")

        chart_query = (
            select(
                date_day,
                func.sum(OrderModel.total_amount).label("total"),
            )
            .where(OrderModel.order_date >= start_30d)
            .where(OrderModel.status == "paid")
            .group_by(date_day)
            .order_by(date_day)
        )

        chart_results = self.session.exec(chart_query).all()

        sales_chart_30d = [
            SalesChartItem(date=r.date.isoformat(), total=r.total)
            for r in chart_results
        ]

        response_data = DashboardStatsResponse(
            sales_today=sales_today,
            sales_week=sales_week,
            sales_month=sales_month,
            orders_today=orders_today,
            sales_chart_30d=sales_chart_30d,
        )

        return response_data
