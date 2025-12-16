"""Tests unitarios para servicio de órdenes."""
import pytest
from app.services.order_service import (
    validate_order_items,
    calculate_preparation_time,
    group_items_by_category,
    check_stock_availability,
    apply_promotional_code,
    get_order_status,
    filter_available_products,
    calculate_delivery_fee,
    estimate_order_value,
    format_order_items,
)


class TestValidateOrderItems:    
    def test_validate_order_items_valid(self):
        assert validate_order_items([{"item": "coffee"}]) is True

    def test_validate_order_items_empty_list(self):
        assert validate_order_items([]) is False

    def test_validate_order_items_not_list(self):
        assert validate_order_items("not a list") is False

    def test_validate_order_items_multiple_items(self):
        assert validate_order_items([{"item": 1}, {"item": 2}]) is True

    def test_validate_order_items_none(self):
        assert validate_order_items(None) is False


class TestCalculatePreparationTime:    
    def test_preparation_time_single_item_simple(self):
        assert calculate_preparation_time(1, "simple") == 6

    def test_preparation_time_single_item_normal(self):
        assert calculate_preparation_time(1, "normal") == 7

    def test_preparation_time_single_item_complex(self):
        assert calculate_preparation_time(1, "complex") == 10

    def test_preparation_time_multiple_items(self):
        assert calculate_preparation_time(3, "normal") == 12

    def test_preparation_time_zero_items(self):
        assert calculate_preparation_time(0) == 0

    def test_preparation_time_default_complexity(self):
        assert calculate_preparation_time(2) == 10


class TestGroupItemsByCategory:
    def test_group_items_single_category(self):
        items = [{"name": "coffee", "category": "beverages"}]
        result = group_items_by_category(items)
        assert "beverages" in result
        assert len(result["beverages"]) == 1

    def test_group_items_multiple_categories(self):
        items = [
            {"name": "coffee", "category": "beverages"},
            {"name": "cake", "category": "food"},
        ]
        result = group_items_by_category(items)
        assert len(result) == 2
        assert len(result["beverages"]) == 1
        assert len(result["food"]) == 1

    def test_group_items_same_category_multiple(self):
        items = [
            {"name": "coffee", "category": "beverages"},
            {"name": "tea", "category": "beverages"},
        ]
        result = group_items_by_category(items)
        assert len(result["beverages"]) == 2

    def test_group_items_empty_list(self):
        assert group_items_by_category([]) == {}

    def test_group_items_not_list(self):
        assert group_items_by_category("not a list") == {}


class TestCheckStockAvailability:
    """Tests para verificación de disponibilidad de stock."""

    def test_stock_available_exact_match(self):
        assert check_stock_availability(10, 10) is True

    def test_stock_available_more_than_needed(self):
        assert check_stock_availability(20, 10) is True

    def test_stock_not_available(self):
        assert check_stock_availability(5, 10) is False

    def test_stock_zero_available(self):
        assert check_stock_availability(0, 1) is False

    def test_stock_zero_ordered(self):
        assert check_stock_availability(10, 0) is False

    def test_stock_invalid_types(self):
        assert check_stock_availability("10", "5") is False


class TestApplyPromotionalCode:
    """Tests para aplicación de código promocional."""

    def test_promo_code_cafe10(self):
        assert apply_promotional_code(100, "CAFE10") == 90.0

    def test_promo_code_cafe20(self):
        assert apply_promotional_code(100, "CAFE20") == 80.0

    def test_promo_code_newuser(self):
        assert apply_promotional_code(100, "NEWUSER") == 85.0

    def test_promo_code_vipuser(self):
        assert apply_promotional_code(100, "VIPUSER") == 75.0

    def test_promo_code_invalid(self):
        assert apply_promotional_code(100, "INVALID") == 100.0

    def test_promo_code_invalid_price(self):
        assert apply_promotional_code("invalid", "CAFE10") == 0.0


class TestGetOrderStatus:
    """Tests para obtención de estado de orden."""

    def test_status_zero_minutes(self):
        assert get_order_status(0) == "received"

    def test_status_preparing(self):
        assert get_order_status(5) == "preparing"

    def test_status_ready(self):
        assert get_order_status(15) == "ready"

    def test_status_completed(self):
        assert get_order_status(30) == "completed"

    def test_status_negative_minutes(self):
        assert get_order_status(-5) == "unknown"


class TestFilterAvailableProducts:
    """Tests para filtro de productos disponibles."""

    def test_filter_products_all_available(self):
        products = [
            {"name": "coffee", "stock": 5},
            {"name": "tea", "stock": 10},
        ]
        result = filter_available_products(products)
        assert len(result) == 2

    def test_filter_products_some_unavailable(self):
        products = [
            {"name": "coffee", "stock": 5},
            {"name": "tea", "stock": 0},
        ]
        result = filter_available_products(products)
        assert len(result) == 1
        assert result[0]["name"] == "coffee"

    def test_filter_products_custom_min_stock(self):
        products = [
            {"name": "coffee", "stock": 5},
            {"name": "tea", "stock": 20},
        ]
        result = filter_available_products(products, min_stock=10)
        assert len(result) == 1
        assert result[0]["name"] == "tea"

    def test_filter_products_empty_list(self):
        assert filter_available_products([]) == []

    def test_filter_products_not_list(self):
        assert filter_available_products("not a list") == []


class TestCalculateDeliveryFee:
    """Tests para cálculo de tarifa de entrega."""

    def test_delivery_fee_base(self):
        assert calculate_delivery_fee(2, 50) == 3.0

    def test_delivery_fee_longer_distance(self):
        assert calculate_delivery_fee(5, 50) == 4.5

    def test_delivery_fee_large_order(self):
        assert calculate_delivery_fee(2, 100) == 1.5

    def test_delivery_fee_negative_distance(self):
        assert calculate_delivery_fee(-2, 50) == 0.0

    def test_delivery_fee_zero_order(self):
        assert calculate_delivery_fee(2, 0) == 0.0

    def test_delivery_fee_invalid_type(self):
        assert calculate_delivery_fee("2", "50") == 0.0


class TestEstimateOrderValue:
    """Tests para estimación de valor de orden."""

    def test_estimate_single_item(self):
        items = [{"price": 10, "quantity": 1}]
        assert estimate_order_value(items) == 10.0

    def test_estimate_multiple_items(self):
        items = [
            {"price": 10, "quantity": 2},
            {"price": 5, "quantity": 3},
        ]
        assert estimate_order_value(items) == 35.0

    def test_estimate_empty_list(self):
        assert estimate_order_value([]) == 0.0

    def test_estimate_invalid_type(self):
        assert estimate_order_value("not a list") == 0.0

    def test_estimate_item_with_zero_price(self):
        items = [{"price": 0, "quantity": 1}]
        assert estimate_order_value(items) == 0.0


class TestFormatOrderItems:
    """Tests para formateado de items de orden."""

    def test_format_single_item(self):
        items = [{"name": "coffee", "quantity": 1}]
        result = format_order_items(items)
        assert result[0] == "1x coffee"

    def test_format_multiple_items(self):
        items = [
            {"name": "coffee", "quantity": 2},
            {"name": "cake", "quantity": 1},
        ]
        result = format_order_items(items)
        assert "2x coffee" in result
        assert "1x cake" in result

    def test_format_default_quantity(self):
        items = [{"name": "coffee"}]
        result = format_order_items(items)
        assert result[0] == "1x coffee"

    def test_format_empty_list(self):
        assert format_order_items([]) == []

    def test_format_not_list(self):
        assert format_order_items("not a list") == []


class TestValidateOrderItemsExtended:
    """Tests adicionales para validación de órdenes."""

    def test_validate_items_dict_input(self):
        assert validate_order_items({"item": "coffee"}) is False

    def test_validate_items_nested_list(self):
        assert validate_order_items([[]]) is True

    def test_validate_items_numeric_list(self):
        assert validate_order_items([1, 2, 3]) is True


class TestCalculatePreparationTimeExtended:
    """Tests adicionales para tiempo de preparación."""

    def test_preparation_time_many_items_simple(self):
        assert calculate_preparation_time(10, "simple") == 15

    def test_preparation_time_invalid_complexity(self):
        assert calculate_preparation_time(2, "invalid") == 10

    def test_preparation_time_negative_items(self):
        assert calculate_preparation_time(-5, "normal") == 0

    def test_preparation_time_very_high_quantity(self):
        result = calculate_preparation_time(100, "normal")
        assert result > 0


class TestGroupItemsByCategoryExtended:
    """Tests adicionales para agrupar items."""

    def test_group_items_no_category_key(self):
        items = [{"name": "coffee"}]
        result = group_items_by_category(items)
        assert "uncategorized" in result

    def test_group_items_mixed_with_no_category(self):
        items = [
            {"name": "coffee", "category": "beverages"},
            {"name": "tea"},
        ]
        result = group_items_by_category(items)
        assert len(result) == 2

    def test_group_items_invalid_dict_items(self):
        items = [{"name": "coffee", "category": "beverages"}, "invalid"]
        result = group_items_by_category(items)
        assert len(result) == 1

    def test_group_items_none_input(self):
        assert group_items_by_category(None) == {}


class TestCheckStockAvailabilityExtended:
    """Tests adicionales para verificación de stock."""

    def test_stock_negative_available(self):
        assert check_stock_availability(-10, 5) is False

    def test_stock_negative_ordered(self):
        assert check_stock_availability(10, -5) is False

    def test_stock_float_quantities(self):
        assert check_stock_availability(10.5, 5.3) is False

    def test_stock_none_input(self):
        assert check_stock_availability(None, 10) is False


class TestApplyPromotionalCodeExtended:
    """Tests adicionales para códigos promocionales."""

    def test_promo_code_lowercase(self):
        assert apply_promotional_code(100, "cafe10") == 100.0

    def test_promo_code_empty_string(self):
        assert apply_promotional_code(100, "") == 100.0

    def test_promo_code_none_code(self):
        assert apply_promotional_code(100, None) == 100.0

    def test_promo_code_negative_price(self):
        assert apply_promotional_code(-100, "CAFE10") == 0.0

    def test_promo_code_zero_price(self):
        assert apply_promotional_code(0, "CAFE10") == 0.0


class TestGetOrderStatusExtended:
    """Tests adicionales para estado de orden."""

    def test_status_boundary_9_minutes(self):
        assert get_order_status(9) == "preparing"

    def test_status_boundary_10_minutes(self):
        assert get_order_status(10) == "ready"

    def test_status_boundary_19_minutes(self):
        assert get_order_status(19) == "ready"

    def test_status_boundary_20_minutes(self):
        assert get_order_status(20) == "completed"

    def test_status_very_large_minutes(self):
        assert get_order_status(10000) == "completed"


class TestFilterAvailableProductsExtended:
    """Tests adicionales para filtro de productos."""

    def test_filter_products_no_stock_key(self):
        products = [{"name": "coffee"}]
        result = filter_available_products(products)
        assert len(result) == 0

    def test_filter_products_zero_min_stock(self):
        products = [
            {"name": "coffee", "stock": 0},
            {"name": "tea", "stock": 1},
        ]
        result = filter_available_products(products, min_stock=0)
        assert len(result) == 2

    def test_filter_products_invalid_stock_type(self):
        products = [
            {"name": "coffee", "stock": "five"},
            {"name": "tea", "stock": 10},
        ]
        result = filter_available_products(products)
        assert len(result) == 1

    def test_filter_products_none_input(self):
        assert filter_available_products(None) == []

    def test_filter_products_negative_stock(self):
        products = [{"name": "coffee", "stock": -5}]
        result = filter_available_products(products)
        assert len(result) == 0


class TestCalculateDeliveryFeeExtended:
    """Tests adicionales para tarifa de entrega."""

    def test_delivery_fee_zero_distance(self):
        assert calculate_delivery_fee(0, 50) == 0.0

    def test_delivery_fee_very_large_distance(self):
        result = calculate_delivery_fee(1000, 50)
        assert result > 500

    def test_delivery_fee_very_large_order(self):
        result = calculate_delivery_fee(5, 10000)
        assert result == 1.75

    def test_delivery_fee_none_input(self):
        assert calculate_delivery_fee(None, 50) == 0.0

    def test_delivery_fee_list_input(self):
        assert calculate_delivery_fee([5], [50]) == 0.0


class TestEstimateOrderValueExtended:
    """Tests adicionales para estimación de valor."""

    def test_estimate_items_with_zero_quantity(self):
        items = [{"price": 10, "quantity": 0}]
        assert estimate_order_value(items) == 0.0

    def test_estimate_items_missing_price(self):
        items = [{"quantity": 1}]
        assert estimate_order_value(items) == 0.0

    def test_estimate_items_missing_quantity(self):
        items = [{"price": 10}]
        assert estimate_order_value(items) == 0.0

    def test_estimate_items_negative_price(self):
        items = [{"price": -10, "quantity": 2}]
        assert estimate_order_value(items) == 0.0

    def test_estimate_items_negative_quantity(self):
        items = [{"price": 10, "quantity": -2}]
        assert estimate_order_value(items) == 0.0

    def test_estimate_items_invalid_type(self):
        items = [{"price": "10", "quantity": "2"}]
        assert estimate_order_value(items) == 0.0

    def test_estimate_mixed_valid_invalid(self):
        items = [
            {"price": 10, "quantity": 2},
            {"price": "invalid", "quantity": 3},
        ]
        # Si tiene al menos uno válido debe contar
        assert estimate_order_value(items) >= 20.0


class TestFormatOrderItemsExtended:
    """Tests adicionales para formateo de items."""

    def test_format_items_large_quantity(self):
        items = [{"name": "coffee", "quantity": 100}]
        result = format_order_items(items)
        assert result[0] == "100x coffee"

    def test_format_items_zero_quantity(self):
        items = [{"name": "coffee", "quantity": 0}]
        result = format_order_items(items)
        assert result[0] == "0x coffee"

    def test_format_items_missing_name(self):
        items = [{"quantity": 1}]
        result = format_order_items(items)
        # Debería manejar gracefully
        assert isinstance(result, list)

    def test_format_items_special_characters(self):
        items = [{"name": "café con leche", "quantity": 1}]
        result = format_order_items(items)
        assert "café con leche" in result[0]

    def test_format_items_none_input(self):
        assert format_order_items(None) == []
