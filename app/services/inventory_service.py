"""
Servicio para gestión de inventario de ingredientes
"""
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.inventory.ingredient_model import IngredientModel
from app.models.catalog.product_model import ProductModel


class InventoryService:
    """Servicio para manejar descuento de stock de ingredientes"""
    
    def __init__(self, session: Session):
        self.session = session
    
    async def deduct_stock_for_order(self, order_items: list) -> dict:
        """
        Descuenta el stock de ingredientes basado en los items de una orden
        
        Args:
            order_items: Lista de items con estructura:
                [
                    {
                        "product_id": "uuid",
                        "quantity": 2,
                        "customizations": {...}
                    }
                ]
        
        Returns:
            dict: Resumen de ingredientes descontados
        
        Raises:
            HTTPException: Si no hay suficiente stock
        """
        ingredients_to_deduct = {}
        insufficient_stock = []
        
        # 1. Calcular total de ingredientes necesarios
        for item in order_items:
            # Validar que product_id existe y no está vacío
            if not item.get("product_id"):
                print(f"[INVENTORY] Skipping item without product_id: {item}")
                continue
            
            try:
                product_id = UUID(item["product_id"])
            except (ValueError, TypeError) as e:
                print(f"[INVENTORY] Invalid product_id: {item.get('product_id')}, error: {e}")
                continue
            
            quantity = item["quantity"]
            
            # Obtener producto con sus ingredientes
            product = self.session.get(ProductModel, product_id)
            if not product:
                continue
            
            # Si el producto no tiene ingredientes definidos, continuar
            if not product.ingredients_json or "ingredients" not in product.ingredients_json:
                continue
            
            # Acumular ingredientes
            for ingredient_data in product.ingredients_json["ingredients"]:
                ingredient_id = UUID(ingredient_data["ingredientId"])
                ingredient_quantity = ingredient_data["quantity"]
                total_needed = ingredient_quantity * quantity
                
                if ingredient_id not in ingredients_to_deduct:
                    ingredients_to_deduct[ingredient_id] = 0
                
                ingredients_to_deduct[ingredient_id] += total_needed
        
        # 2. Verificar stock disponible
        for ingredient_id, quantity_needed in ingredients_to_deduct.items():
            ingredient = self.session.get(IngredientModel, ingredient_id)
            if not ingredient:
                continue
            
            if ingredient.stock_current_level < quantity_needed:
                insufficient_stock.append({
                    "ingredient_name": ingredient.name,
                    "available": ingredient.stock_current_level,
                    "needed": quantity_needed
                })
        
        # 3. Si hay stock insuficiente, lanzar error
        if insufficient_stock:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Stock insuficiente para completar la orden",
                    "insufficient_ingredients": insufficient_stock
                }
            )
        
        # 4. Realizar descuento de stock
        deducted_summary = []
        for ingredient_id, quantity_to_deduct in ingredients_to_deduct.items():
            ingredient = self.session.get(IngredientModel, ingredient_id)
            if not ingredient:
                continue
            
            ingredient.stock_current_level -= quantity_to_deduct
            self.session.add(ingredient)
            
            deducted_summary.append({
                "ingredient_id": str(ingredient_id),
                "ingredient_name": ingredient.name,
                "quantity_deducted": quantity_to_deduct,
                "remaining_stock": ingredient.stock_current_level
            })
        
        self.session.commit()
        
        return {
            "success": True,
            "deducted_ingredients": deducted_summary
        }
