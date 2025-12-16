from decimal import Decimal
from typing import Tuple


def calculate_discount(base_price: float, discount_percent: float) -> float:
    if not isinstance(base_price, (int, float)) or not isinstance(discount_percent, (int, float)):
        return 0.0
    
    if base_price < 0 or discount_percent < 0 or discount_percent > 100:
        return 0.0
    
    # Calcular descuento
    discount = base_price * (discount_percent / 100)
    # Si el descuento es exactamente 0.005 o menor, retornar 0.0
    if discount <= 0.005:
        return 0.0
    return round(discount, 2)


def calculate_price_after_discount(base_price: float, discount_percent: float) -> float:
    if not isinstance(base_price, (int, float)) or not isinstance(discount_percent, (int, float)):
        return 0.0
    
    discount = calculate_discount(base_price, discount_percent)
    return round(base_price - discount, 2)


def calculate_tax(price: float, tax_rate: float) -> float:
    if not isinstance(price, (int, float)) or not isinstance(tax_rate, (int, float)):
        return 0.0
    
    if price < 0 or tax_rate < 0:
        return 0.0
    
    # Calcular impuesto y redondear
    tax = round(price * (tax_rate / 100), 2)
    # Si el impuesto es muy pequeño (menor a 0.01), retornar 0.0
    if tax < 0.01:
        return 0.0
    return tax


def calculate_price_with_tax(price: float, tax_rate: float) -> float:
    if not isinstance(price, (int, float)) or price < 0:
        return 0.0
    
    # Usar Decimal para mayor precisión con números grandes
    from decimal import Decimal, ROUND_HALF_UP
    d_price = Decimal(str(price))
    d_rate = Decimal(str(tax_rate))
    
    # Calcular el total directamente: price * (1 + tax_rate/100)
    d_total = d_price * (Decimal('100') + d_rate) / Decimal('100')
    # Redondear a 2 decimales
    result = d_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return float(result)


def calculate_total_order(base_price: float, discount_percent: float = 0, tax_rate: float = 0) -> float:
    if not isinstance(base_price, (int, float)) or base_price < 0:
        return 0.0
    
    if discount_percent < 0 or discount_percent > 100 or tax_rate < 0 or tax_rate > 100:
        return 0.0
    
    price_after_discount = calculate_price_after_discount(base_price, discount_percent)
    
    total = calculate_price_with_tax(price_after_discount, tax_rate)
    
    return round(total, 2)


def calculate_order_summary(
    base_price: float,
    discount_percent: float = 0,
    tax_rate: float = 0,
    quantity: int = 1
) -> dict:
    if not isinstance(base_price, (int, float)):
        return {
            "subtotal": 0.0,
            "discount_percent": discount_percent,
            "discount_amount": 0.0,
            "price_after_discount": 0.0,
            "tax_rate": tax_rate,
            "tax_amount": 0.0,
            "total": 0.0,
            "quantity": quantity
        }
    
    if not isinstance(quantity, int):
        quantity = 1
    
    if discount_percent < 0 or discount_percent > 100:
        discount_percent = 0
    
    if tax_rate < 0:
        tax_rate = 0
    
    subtotal = round(base_price * quantity, 2)
    discount_amount = calculate_discount(subtotal, discount_percent)
    price_after_discount = calculate_price_after_discount(subtotal, discount_percent)
    tax_amount = calculate_tax(price_after_discount, tax_rate)
    total = round(price_after_discount + tax_amount, 2)
    
    return {
        "subtotal": subtotal,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "price_after_discount": price_after_discount,
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "total": total,
        "quantity": quantity
    }


def calculate_average_price(prices: list) -> float:
    if not isinstance(prices, list) or not prices:
        return 0.0
    
    # Excluir solo valores negativos, incluir ceros
    valid_prices = [p for p in prices if isinstance(p, (int, float)) and p >= 0]
    
    if not valid_prices:
        return 0.0
    
    return round(sum(valid_prices) / len(valid_prices), 2)


def is_price_in_range(price: float, min_price: float, max_price: float) -> bool:
    if not all(isinstance(p, (int, float)) for p in [price, min_price, max_price]):
        return False
    
    return min_price <= price <= max_price
