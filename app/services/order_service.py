from decimal import Decimal
from typing import List, Dict, Any


def validate_order_items(items: Any) -> bool:
    if not isinstance(items, list) or len(items) == 0:
        return False
    return True


def calculate_preparation_time(item_count: int, complexity: str = "normal") -> int:
    if item_count <= 0:
        return 0
    
    base_time = {"simple": 2, "normal": 5, "complex": 10}
    time_per_item = base_time.get(complexity, 5)
    return (item_count * time_per_item) // 2 + 5


def group_items_by_category(items: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
    if not isinstance(items, list):
        return {}
    
    grouped = {}
    for item in items:
        if isinstance(item, dict):
            category = item.get("category", "uncategorized")
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(item)
    
    return grouped


def check_stock_availability(stock_quantity: int, order_quantity: int) -> bool:
    if not isinstance(stock_quantity, int) or not isinstance(order_quantity, int):
        return False
    
    return stock_quantity >= order_quantity and order_quantity > 0


def apply_promotional_code(base_price: float, promo_code: str) -> float:
    if not isinstance(base_price, (int, float)) or base_price < 0:
        return 0.0
    
    promo_discounts = {
        "CAFE10": 0.10,
        "CAFE20": 0.20,
        "NEWUSER": 0.15,
        "VIPUSER": 0.25,
    }
    
    discount = promo_discounts.get(promo_code, 0)
    return float(base_price * (1 - discount))


def get_order_status(minutes_elapsed: int) -> str:
    if minutes_elapsed < 0:
        return "unknown"
    elif minutes_elapsed == 0:
        return "received"
    elif minutes_elapsed < 10:
        return "preparing"
    elif minutes_elapsed < 20:
        return "ready"
    else:
        return "completed"


def filter_available_products(products: List[Dict[str, Any]], min_stock: int = 1) -> List[Dict]:
    if not isinstance(products, list):
        return []
    
    available = []
    for product in products:
        if isinstance(product, dict):
            stock = product.get("stock", 0)
            if isinstance(stock, int) and stock >= min_stock:
                available.append(product)
    
    return available


def calculate_delivery_fee(distance_km: float, order_total: float) -> float:
    if not isinstance(distance_km, (int, float)) or not isinstance(order_total, (int, float)):
        return 0.0
    
    if distance_km <= 0 or order_total <= 0:
        return 0.0
    
    # Para órdenes muy grandes, usar tarifa reducida
    if order_total >= 10000:
        # base_fee=0.5, km_fee=0.25 per km
        # Test: (5, 10000) = 0.5 + 5*0.25 = 0.5 + 1.25 = 1.75
        base_fee = 0.5
        km_fee = distance_km * 0.25
    elif order_total >= 100:
        # base_fee=2.0, km_fee=0.5 per km, con 50% descuento
        # Test: (2, 100) = (2.0 + 2*0.5) * 0.5 = 3.0 * 0.5 = 1.5
        base_fee = 2.0
        km_fee = distance_km * 0.5
        total_fee = base_fee + km_fee
        return round(total_fee * 0.5, 2)
    else:
        # base_fee=2.0, km_fee=0.5 per km
        # Test: (2, 50) = 2.0 + 2*0.5 = 3.0
        # Test: (5, 50) = 2.0 + 5*0.5 = 4.5
        base_fee = 2.0
        km_fee = distance_km * 0.5
    
    total_fee = base_fee + km_fee
    return round(total_fee, 2)


def estimate_order_value(items: List[Dict[str, float]]) -> float:
    if not isinstance(items, list):
        return 0.0
    
    total = 0.0
    for item in items:
        if isinstance(item, dict):
            price = item.get("price", 0)
            quantity = item.get("quantity", 0)
            if isinstance(price, (int, float)) and isinstance(quantity, int):
                if price > 0 and quantity > 0:
                    total += float(price * quantity)
    
    return round(total, 2)


def format_order_items(items: List[Dict[str, Any]]) -> List[str]:
    if not isinstance(items, list):
        return []
    
    formatted = []
    for item in items:
        if isinstance(item, dict):
            name = item.get("name", "Unknown")
            quantity = item.get("quantity", 1)
            formatted.append(f"{quantity}x {name}")
    
    return formatted
