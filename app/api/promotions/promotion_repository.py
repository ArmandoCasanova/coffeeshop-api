from typing import Optional, List
from sqlmodel import Session, select, func
from uuid import UUID
from datetime import datetime
from app.models.catalog.product_model import ProductModel
from app.models.promotions.product_promotion_model import ProductPromotionModel
from app.models.promotions.promotion_model import PromotionModel


class PromotionRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create_promotion(self, promotion_data: dict) -> PromotionModel:
        try:
            new_promotion = PromotionModel(**promotion_data)
            self.session.add(new_promotion)
            self.session.commit()
            self.session.refresh(new_promotion)
            return new_promotion
        except Exception:
            self.session.rollback()
            raise

    async def get_promotion_by_id(self, promotion_id: UUID) -> Optional[PromotionModel]:
        try:
            statement = select(PromotionModel).where(
                PromotionModel.promotion_id == promotion_id
            )
            promotion = self.session.exec(statement).first()
            return promotion
        except Exception:
            raise

    async def get_all_applied_promotions(
        self, skip: int = 0, limit: int = 10
    ) -> tuple[List, int]:
        """
        Obtiene una lista paginada de promociones aplicadas a productos,
        uniendo las tablas products, promotions y product_promotions.
        """
        try:
            query = (
                select(
                    ProductModel.product_id,
                    ProductModel.base_price, 
                    PromotionModel.promotion_id,
                    PromotionModel.discount_type,
                    PromotionModel.discount_value,
                    PromotionModel.start_date,
                    PromotionModel.end_date,
                )
                .join(
                    ProductPromotionModel,
                    ProductModel.product_id == ProductPromotionModel.product_id,
                )
                .join(
                    PromotionModel,
                    PromotionModel.promotion_id == ProductPromotionModel.promotion_id,
                )
                .order_by(ProductModel.product_id, PromotionModel.start_date)
            )

            total_query = select(func.count(ProductPromotionModel.product_id))

            total = self.session.exec(total_query).one()
            results = self.session.exec(query.offset(skip).limit(limit)).all()
            
            return list(results), total
        except Exception:
            self.session.rollback()
            raise

    async def update_promotion(
        self, promotion_id: UUID, update_data: dict
    ) -> Optional[PromotionModel]:
        try:
            statement = select(PromotionModel).where(
                PromotionModel.promotion_id == promotion_id
            )
            promotion = self.session.exec(statement).first()

            if not promotion:
                return None
            update_data["updated_at"] = datetime.utcnow()
            
            for field, value in update_data.items():
                if hasattr(promotion, field) and value is not None:
                    setattr(promotion, field, value)

            self.session.add(promotion)
            self.session.commit()
            self.session.refresh(promotion)
            return promotion
        except Exception:
            self.session.rollback()
            raise

    async def delete_promotion(self, promotion_id: UUID) -> bool:
        try:
            statement = select(PromotionModel).where(
                PromotionModel.promotion_id == promotion_id
            )
            promotion = self.session.exec(statement).first()

            if not promotion:
                return False

            self.session.delete(promotion)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise
    
    async def get_promotion_by_code(self, code: str) -> Optional[PromotionModel]:
        try:
            statement = select(PromotionModel).where(
                PromotionModel.code == code,
                PromotionModel.start_date <= datetime.utcnow(),
                PromotionModel.end_date >= datetime.utcnow()
            )
            promotion = self.session.exec(statement).first()
            return promotion
        except Exception:
            raise