"""Tests unitarios para servicio de precios."""
import pytest
from app.services.pricing_service import (
    calculate_discount,
    calculate_price_after_discount,
    calculate_tax,
    calculate_price_with_tax,
    calculate_total_order,
    calculate_order_summary,
    calculate_average_price,
    is_price_in_range,
)


class TestCalculateDiscount:
    """Tests para cálculo de descuento."""

    def test_calculate_discount_basic(self):
        assert calculate_discount(100, 10) == 10.0

    def test_calculate_discount_zero_discount(self):
        assert calculate_discount(100, 0) == 0.0

    def test_calculate_discount_full_discount(self):
        assert calculate_discount(100, 100) == 100.0

    def test_calculate_discount_decimal_result(self):
        assert calculate_discount(50, 33) == 16.5

    def test_calculate_discount_negative_price(self):
        assert calculate_discount(-100, 10) == 0.0

    def test_calculate_discount_negative_percent(self):
        assert calculate_discount(100, -10) == 0.0

    def test_calculate_discount_percent_over_100(self):
        assert calculate_discount(100, 150) == 0.0

    def test_calculate_discount_invalid_types(self):
        assert calculate_discount("100", "10") == 0.0


class TestCalculatePriceAfterDiscount:
    """Tests para precio después de descuento."""

    def test_price_after_discount_basic(self):
        assert calculate_price_after_discount(100, 10) == 90.0

    def test_price_after_discount_zero(self):
        assert calculate_price_after_discount(100, 0) == 100.0

    def test_price_after_discount_full(self):
        assert calculate_price_after_discount(100, 100) == 0.0

    def test_price_after_discount_decimal(self):
        assert calculate_price_after_discount(50, 33) == 33.5

    def test_price_after_discount_invalid_input(self):
        assert calculate_price_after_discount("100", "10") == 0.0


class TestCalculateTax:
    """Tests para cálculo de impuesto."""

    def test_calculate_tax_basic(self):
        assert calculate_tax(100, 16) == 16.0

    def test_calculate_tax_zero_rate(self):
        assert calculate_tax(100, 0) == 0.0

    def test_calculate_tax_decimal_result(self):
        assert calculate_tax(99.99, 16) == 16.0

    def test_calculate_tax_negative_price(self):
        assert calculate_tax(-100, 16) == 0.0

    def test_calculate_tax_negative_rate(self):
        assert calculate_tax(100, -10) == 0.0

    def test_calculate_tax_invalid_types(self):
        assert calculate_tax("100", "16") == 0.0


class TestCalculatePriceWithTax:
    """Tests para precio con impuesto incluido."""

    def test_price_with_tax_basic(self):
        assert calculate_price_with_tax(100, 16) == 116.0

    def test_price_with_tax_zero_rate(self):
        assert calculate_price_with_tax(100, 0) == 100.0

    def test_price_with_tax_decimal(self):
        assert calculate_price_with_tax(99.99, 16) == 115.99


class TestCalculateTotalOrder:
    """Tests para cálculo de total de orden."""

    def test_total_order_no_discount_no_tax(self):
        assert calculate_total_order(100) == 100.0

    def test_total_order_with_discount(self):
        assert calculate_total_order(100, 10) == 90.0

    def test_total_order_with_tax(self):
        assert calculate_total_order(100, 0, 16) == 116.0

    def test_total_order_with_discount_and_tax(self):
        # 100 - 10% (10) = 90
        # 90 + 16% (14.4) = 104.4
        assert calculate_total_order(100, 10, 16) == 104.4

    def test_total_order_invalid_input(self):
        assert calculate_total_order("100") == 0.0


class TestCalculateOrderSummary:
    """Tests para resumen de orden."""

    def test_order_summary_basic(self):
        result = calculate_order_summary(100)
        assert result["subtotal"] == 100.0
        assert result["discount_amount"] == 0.0
        assert result["total"] == 100.0
        assert result["quantity"] == 1

    def test_order_summary_with_quantity(self):
        result = calculate_order_summary(100, quantity=2)
        assert result["subtotal"] == 200.0
        assert result["quantity"] == 2

    def test_order_summary_with_discount(self):
        result = calculate_order_summary(100, discount_percent=10)
        assert result["discount_amount"] == 10.0
        assert result["price_after_discount"] == 90.0

    def test_order_summary_complete(self):
        result = calculate_order_summary(100, 10, 16, 2)
        assert result["subtotal"] == 200.0
        assert result["discount_amount"] == 20.0
        assert result["price_after_discount"] == 180.0
        assert result["tax_amount"] == 28.8
        assert result["total"] == 208.8
        assert result["quantity"] == 2

    def test_order_summary_has_all_keys(self):
        result = calculate_order_summary(100)
        expected_keys = {
            "subtotal", "discount_percent", "discount_amount",
            "price_after_discount", "tax_rate", "tax_amount", "total", "quantity"
        }
        assert set(result.keys()) == expected_keys


class TestCalculateAveragePrice:
    """Tests para precio promedio."""

    def test_average_price_basic(self):
        assert calculate_average_price([100, 200, 300]) == 200.0

    def test_average_price_single_item(self):
        assert calculate_average_price([100]) == 100.0

    def test_average_price_with_decimals(self):
        assert calculate_average_price([10.5, 20.5, 30.0]) == 20.33

    def test_average_price_empty_list(self):
        assert calculate_average_price([]) == 0.0

    def test_average_price_invalid_input(self):
        assert calculate_average_price("not a list") == 0.0

    def test_average_price_with_negative(self):
        # Los negativos se filtran
        assert calculate_average_price([100, -50, 200]) == 150.0

    def test_average_price_with_invalid_items(self):
        # Los items inválidos se filtran
        assert calculate_average_price([100, "invalid", 200]) == 150.0


class TestIsPriceInRange:
    """Tests para verificar precio en rango."""

    def test_price_in_range_basic(self):
        assert is_price_in_range(50, 0, 100) is True

    def test_price_in_range_at_min(self):
        assert is_price_in_range(0, 0, 100) is True

    def test_price_in_range_at_max(self):
        assert is_price_in_range(100, 0, 100) is True

    def test_price_in_range_below_min(self):
        assert is_price_in_range(-10, 0, 100) is False

    def test_price_in_range_above_max(self):
        assert is_price_in_range(150, 0, 100) is False

    def test_price_in_range_invalid_types(self):
        assert is_price_in_range("50", "0", "100") is False

    def test_price_in_range_with_decimals(self):
        assert is_price_in_range(50.5, 50.0, 100.0) is True


class TestCalculateDiscountExtended:
    """Tests adicionales para descuento con casos de fallo."""

    def test_calculate_discount_very_large_price(self):
        assert calculate_discount(999999.99, 10) == 100000.0

    def test_calculate_discount_very_small_price(self):
        assert calculate_discount(0.01, 50) == 0.0

    def test_calculate_discount_float_percent(self):
        assert calculate_discount(100, 10.5) == 10.5

    def test_calculate_discount_none_values(self):
        assert calculate_discount(None, None) == 0.0

    def test_calculate_discount_list_input(self):
        assert calculate_discount([100], [10]) == 0.0


class TestCalculatePriceAfterDiscountExtended:
    """Tests adicionales para precio con descuento."""

    def test_price_after_discount_very_large_amount(self):
        assert calculate_price_after_discount(999999.99, 50) == 500000.0

    def test_price_after_discount_none_values(self):
        assert calculate_price_after_discount(None, None) == 0.0

    def test_price_after_discount_float_percent(self):
        assert calculate_price_after_discount(100, 25.5) == 74.5


class TestCalculateTaxExtended:
    """Tests adicionales para cálculo de impuesto."""

    def test_calculate_tax_very_large_amount(self):
        assert calculate_tax(999999.99, 16) == 160000.0

    def test_calculate_tax_very_small_amount(self):
        assert calculate_tax(0.01, 16) == 0.0

    def test_calculate_tax_decimal_rate(self):
        assert calculate_tax(100, 16.5) == 16.5

    def test_calculate_tax_none_values(self):
        assert calculate_tax(None, None) == 0.0


class TestCalculatePriceWithTaxExtended:
    """Tests adicionales para precio con impuesto."""

    def test_price_with_tax_very_high_rate(self):
        assert calculate_price_with_tax(100, 50) == 150.0

    def test_price_with_tax_negative_input(self):
        assert calculate_price_with_tax(-100, 16) == 0.0


class TestCalculateTotalOrderExtended:
    """Tests adicionales para total de orden."""

    def test_total_order_large_discount_large_tax(self):
        # 1000 - 50% (500) = 500
        # 500 + 50% (250) = 750
        assert calculate_total_order(1000, 50, 50) == 750.0

    def test_total_order_negative_values(self):
        assert calculate_total_order(-100, 10, 16) == 0.0

    def test_total_order_zero_amount(self):
        assert calculate_total_order(0, 10, 16) == 0.0

    def test_total_order_invalid_discount_and_tax(self):
        assert calculate_total_order(100, 150, 200) == 0.0


class TestCalculateOrderSummaryExtended:
    """Tests adicionales para resumen de orden."""

    def test_order_summary_zero_price(self):
        result = calculate_order_summary(0)
        assert result["subtotal"] == 0.0
        assert result["total"] == 0.0

    def test_order_summary_negative_quantity(self):
        result = calculate_order_summary(100, quantity=-5)
        assert result["quantity"] == -5

    def test_order_summary_very_high_discount(self):
        result = calculate_order_summary(100, discount_percent=200)
        assert result["discount_amount"] == 0.0

    def test_order_summary_invalid_price_type(self):
        result = calculate_order_summary("invalid")
        assert result["subtotal"] == 0.0


class TestCalculateAveragePriceExtended:
    """Tests adicionales para precio promedio."""

    def test_average_price_all_negative(self):
        assert calculate_average_price([-100, -200, -300]) == 0.0

    def test_average_price_all_zeros(self):
        assert calculate_average_price([0, 0, 0]) == 0.0

    def test_average_price_mixed_with_zero(self):
        assert calculate_average_price([0, 100, 200]) == 100.0

    def test_average_price_very_large_numbers(self):
        assert calculate_average_price([999999.99, 1000000.01]) == 1000000.0

    def test_average_price_dict_input(self):
        assert calculate_average_price({"a": 100}) == 0.0


class TestIsPriceInRangeExtended:
    """Tests adicionales para verificar precio en rango."""

    def test_price_in_range_negative_range(self):
        assert is_price_in_range(-50, -100, -10) is True

    def test_price_in_range_inverted_bounds(self):
        assert is_price_in_range(50, 100, 0) is False

    def test_price_in_range_same_bounds(self):
        assert is_price_in_range(50, 50, 50) is True

    def test_price_in_range_none_input(self):
        assert is_price_in_range(None, 0, 100) is False

    def test_price_in_range_string_bounds(self):
        assert is_price_in_range(50, "0", "100") is False
