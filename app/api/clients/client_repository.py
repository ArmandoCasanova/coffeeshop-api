from typing import Optional, List
from sqlmodel import Session, select, func, and_
from sqlalchemy import literal_column
from uuid import UUID
from datetime import datetime
from app.models.orders.order_model import OrderModel, OrderStatus
from app.models.users.user_model import UserModel, UserRole 


class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create_client(self, client_data: dict) -> UserModel:
        try:
            new_client = UserModel(**client_data)
            self.session.add(new_client)
            self.session.commit()
            self.session.refresh(new_client)
            return new_client
        except Exception:
            self.session.rollback()
            raise

    async def get_user_by_email(self, email: str) -> Optional[UserModel]:
        try:
            statement = select(UserModel).where(UserModel.email == email)
            user = self.session.exec(statement).first()
            return user
        except Exception:
            raise

    async def get_client_by_id(self, user_id: UUID) -> Optional[UserModel]:
        try:
            statement = select(UserModel).where(
                and_(
                    UserModel.user_id == user_id,
                    UserModel.role == UserRole.customer
                )
            )
            client = self.session.exec(statement).first()
            return client
        except Exception:
            raise

    async def get_all_clients(
        self, skip: int = 0, limit: int = 10, is_verified: Optional[bool] = None
    ) -> tuple[List[UserModel], int]:
        try:
            base_condition = (UserModel.role == UserRole.customer)
            if is_verified is not None:
                query_condition = and_(base_condition, UserModel.is_verified == is_verified)
            else:
                query_condition = base_condition

            # --- Subconsultas Correlacionadas para Estadísticas de Órdenes ---
            # Usamos un alias para la tabla de órdenes en las subconsultas
            OrderSub = OrderModel

            # 1. Subquery para total de órdenes (COUNT)
            total_orders_subq = (
                select(func.count(OrderSub.order_id))
                .where(
                    and_(
                        OrderSub.user_id == UserModel.user_id, # Correlación
                        OrderSub.status.in_([OrderStatus.paid, OrderStatus.delivered])
                    )
                )
                .label("total_orders")
            )

            # 2. Subquery para gasto total (SUM)
            total_spent_subq = (
                select(func.coalesce(func.sum(OrderSub.total_amount), 0.0)) # coalesce para evitar NULL
                .where(
                    and_(
                        OrderSub.user_id == UserModel.user_id, # Correlación
                        OrderSub.status.in_([OrderStatus.paid, OrderStatus.delivered])
                    )
                )
                .label("total_spent")
            )

            # 3. Subquery para fecha de última orden (MAX)
            last_order_date_subq = (
                select(func.max(OrderSub.order_date))
                .where(
                    and_(
                        OrderSub.user_id == UserModel.user_id, # Correlación
                        OrderSub.status.in_([OrderStatus.paid, OrderStatus.delivered])
                    )
                )
                .label("last_order_date")
            )

            # 4. Subquery para lista de IDs (ARRAY_AGG - Específico de PostgreSQL)
            OrderSub = OrderModel # Alias
            completed_orders_subq = (
                select(
                    # Coalesce para devolver '[]' (un JSON array vacío) en lugar de NULL
                    func.coalesce(
                        func.json_agg(
                            # Construye un objeto JSON por cada fila
                            func.json_build_object(
                                'order_id', OrderSub.order_id,
                                'total_amount', OrderSub.total_amount,
                                'order_date', OrderSub.order_date
                            )
                        ),
                        # --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---
                        # Cambia 'jsonb' por 'json' para que coincida con json_agg
                        literal_column("'[]'::json") 
                        # --------------------------------
                    )
                )
                .where(
                    and_(
                        OrderSub.user_id == UserModel.user_id, # Correlación
                        OrderSub.status.in_([OrderStatus.paid, OrderStatus.delivered])
                    )
                )
                .label("completed_orders") # El label debe coincidir con el Schema
            )

            # --- Consulta Principal ---
            query = (
                select(
                    UserModel,
                    total_orders_subq,
                    total_spent_subq,
                    last_order_date_subq,
                    completed_orders_subq  # <-- Se usa la nueva subquery
                )
                .where(query_condition)
                .order_by(UserModel.name)
                .offset(skip)
                .limit(limit)
            )

            total_query = select(func.count(UserModel.user_id)).where(query_condition)
            total = self.session.exec(total_query).one()
            
            # --- Procesamiento de Resultados (Leve modificación) ---
            results_raw = self.session.exec(query).all()
            
            clients_with_stats = []
            for row in results_raw:
                client_data = row.UserModel.model_dump()
                
                client_data["total_orders"] = row.total_orders or 0
                client_data["total_spent"] = row.total_spent or 0.0
                client_data["last_order_date"] = row.last_order_date
                
                # El resultado de la query ya es un JSON parseable por Pydantic
                client_data["completed_orders"] = row.completed_orders 
                
                clients_with_stats.append(client_data)

            return list(clients_with_stats), total
        except Exception as e:
            print(e)
            self.session.rollback()
            raise

    async def update_client(
        self, user_id: UUID, update_data: dict
    ) -> Optional[UserModel]:
        try:
            client = await self.get_client_by_id(user_id) 

            if not client:
                return None
            update_data["updated_at"] = datetime.utcnow()
            
            for field, value in update_data.items():
                if hasattr(client, field) and value is not None:
                    setattr(client, field, value)

            self.session.add(client)
            self.session.commit()
            self.session.refresh(client)
            return client
        except Exception:
            self.session.rollback()
            raise

    async def delete_client(self, user_id: UUID) -> bool:
        try:
            client = await self.get_client_by_id(user_id)

            if not client:
                return False

            self.session.delete(client)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise