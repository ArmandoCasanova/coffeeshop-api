"""Tests unitarios para validadores."""
import pytest
from app.utils.validators import (
    validate_email,
    validate_phone,
    validate_password,
    validate_price,
    validate_discount_percent,
    validate_uuid_string,
    validate_name,
)


class TestEmailValidator:
    """Tests para validación de email."""

    def test_valid_email(self):
        assert validate_email("user@example.com") is True

    def test_valid_email_with_numbers(self):
        assert validate_email("user123@example.com") is True

    def test_valid_email_with_dots(self):
        assert validate_email("first.last@example.co.uk") is True

    def test_invalid_email_no_at(self):
        assert validate_email("userexample.com") is False

    def test_invalid_email_no_domain(self):
        assert validate_email("user@.com") is False

    def test_invalid_email_no_extension(self):
        assert validate_email("user@example") is False

    def test_empty_email(self):
        assert validate_email("") is False

    def test_none_email(self):
        assert validate_email(None) is False

    def test_email_with_spaces(self):
        assert validate_email("user @example.com") is False


class TestPhoneValidator:
    """Tests para validación de teléfono."""

    def test_valid_phone_10_digits(self):
        assert validate_phone("1234567890") is True

    def test_valid_phone_11_digits(self):
        assert validate_phone("12345678901") is True

    def test_valid_phone_with_spaces(self):
        assert validate_phone("123 456 7890") is True

    def test_valid_phone_with_dashes(self):
        assert validate_phone("123-456-7890") is True

    def test_valid_phone_with_parentheses(self):
        assert validate_phone("(123) 456-7890") is True

    def test_invalid_phone_too_short(self):
        assert validate_phone("123") is False

    def test_invalid_phone_with_letters(self):
        assert validate_phone("12345abcde") is False

    def test_empty_phone(self):
        assert validate_phone("") is False

    def test_none_phone(self):
        assert validate_phone(None) is False


class TestPasswordValidator:
    """Tests para validación de contraseña."""

    def test_valid_password(self):
        assert validate_password("ValidPassword123") is True

    def test_invalid_password_no_uppercase(self):
        assert validate_password("validpassword123") is False

    def test_invalid_password_no_lowercase(self):
        assert validate_password("VALIDPASSWORD123") is False

    def test_invalid_password_no_digit(self):
        assert validate_password("ValidPassword") is False

    def test_invalid_password_too_short(self):
        assert validate_password("Pass1") is False

    def test_valid_password_custom_min_length(self):
        assert validate_password("Pass1", min_length=5) is True

    def test_empty_password(self):
        assert validate_password("") is False

    def test_none_password(self):
        assert validate_password(None) is False


class TestPriceValidator:
    """Tests para validación de precio."""

    def test_valid_price_integer(self):
        assert validate_price(100) is True

    def test_valid_price_float(self):
        assert validate_price(99.99) is True

    def test_invalid_price_zero(self):
        assert validate_price(0) is False

    def test_invalid_price_negative(self):
        assert validate_price(-10) is False

    def test_invalid_price_string(self):
        assert validate_price("100") is False

    def test_invalid_price_none(self):
        assert validate_price(None) is False


class TestDiscountPercentValidator:
    """Tests para validación de porcentaje de descuento."""

    def test_valid_discount_0(self):
        assert validate_discount_percent(0) is True

    def test_valid_discount_50(self):
        assert validate_discount_percent(50) is True

    def test_valid_discount_100(self):
        assert validate_discount_percent(100) is True

    def test_invalid_discount_negative(self):
        assert validate_discount_percent(-10) is False

    def test_invalid_discount_over_100(self):
        assert validate_discount_percent(150) is False

    def test_invalid_discount_string(self):
        assert validate_discount_percent("50") is False


class TestUUIDValidator:
    """Tests para validación de UUID."""

    def test_valid_uuid(self):
        assert validate_uuid_string("550e8400-e29b-41d4-a716-446655440000") is True

    def test_valid_uuid_uppercase(self):
        assert validate_uuid_string("550E8400-E29B-41D4-A716-446655440000") is True

    def test_invalid_uuid_wrong_format(self):
        assert validate_uuid_string("550e8400e29b41d4a716446655440000") is False

    def test_invalid_uuid_wrong_length(self):
        assert validate_uuid_string("550e8400-e29b-41d4-a716-44665544") is False

    def test_empty_uuid(self):
        assert validate_uuid_string("") is False

    def test_none_uuid(self):
        assert validate_uuid_string(None) is False


class TestNameValidator:
    """Tests para validación de nombre."""

    def test_valid_name(self):
        assert validate_name("Juan") is True

    def test_valid_name_with_spaces(self):
        assert validate_name("Juan Carlos") is True

    def test_valid_name_with_accents(self):
        assert validate_name("José María") is True

    def test_valid_name_with_dash(self):
        assert validate_name("María-Luz") is True

    def test_invalid_name_with_numbers(self):
        assert validate_name("Juan123") is False

    def test_invalid_name_too_short(self):
        assert validate_name("", min_length=1) is False

    def test_invalid_name_too_long(self):
        assert validate_name("A" * 101, max_length=100) is False

    def test_valid_name_custom_length(self):
        assert validate_name("Jo", min_length=2, max_length=10) is True

    def test_none_name(self):
        assert validate_name(None) is False

    def test_invalid_name_only_special_chars(self):
        assert validate_name("@#$%") is False

    def test_invalid_name_with_symbols(self):
        assert validate_name("Juan@") is False

    def test_invalid_name_integer_input(self):
        assert validate_name(12345) is False


class TestEmailValidatorExtended:
    """Tests adicionales para email con casos de fallo."""

    def test_invalid_email_double_at(self):
        assert validate_email("user@@example.com") is False

    def test_invalid_email_only_at(self):
        assert validate_email("@") is False

    def test_invalid_email_trailing_dot(self):
        assert validate_email("user@example.com.") is False

    def test_invalid_email_leading_dot(self):
        assert validate_email(".user@example.com") is False

    def test_invalid_email_special_chars(self):
        assert validate_email("user!@example.com") is False

    def test_valid_email_subdomain(self):
        assert validate_email("user@mail.example.co.uk") is True


class TestPhoneValidatorExtended:
    """Tests adicionales para teléfono con casos de fallo."""

    def test_invalid_phone_only_letters(self):
        assert validate_phone("abcdefghij") is False

    def test_invalid_phone_mixed_letters_numbers(self):
        assert validate_phone("123abc7890") is False

    def test_invalid_phone_special_characters(self):
        assert validate_phone("123@456#890") is False

    def test_valid_phone_with_plus_sign(self):
        assert validate_phone("+1 234 567 8901") is True


class TestPasswordValidatorExtended:
    """Tests adicionales para contraseña con casos de fallo."""

    def test_invalid_password_only_numbers(self):
        assert validate_password("12345678") is False

    def test_invalid_password_only_lowercase(self):
        assert validate_password("abcdefgh") is False

    def test_invalid_password_only_uppercase(self):
        assert validate_password("ABCDEFGH") is False

    def test_valid_password_special_chars(self):
        assert validate_password("ValidPassword123!") is True

    def test_valid_password_exactly_8_chars(self):
        assert validate_password("Passw0rd") is True


class TestPriceValidatorExtended:
    """Tests adicionales para precio con casos de fallo."""

    def test_invalid_price_empty_string(self):
        assert validate_price("") is False

    def test_invalid_price_list(self):
        assert validate_price([100]) is False

    def test_invalid_price_dict(self):
        assert validate_price({"value": 100}) is False

    def test_valid_price_large_amount(self):
        assert validate_price(999999.99) is True

    def test_valid_price_small_decimal(self):
        assert validate_price(0.01) is True


class TestDiscountValidatorExtended:
    """Tests adicionales para descuento con casos de fallo."""

    def test_invalid_discount_decimal_over_100(self):
        assert validate_discount_percent(100.5) is False

    def test_valid_discount_decimal(self):
        assert validate_discount_percent(50.5) is True

    def test_invalid_discount_list(self):
        assert validate_discount_percent([50]) is False

    def test_invalid_discount_float_negative(self):
        assert validate_discount_percent(-0.5) is False


class TestUUIDValidatorExtended:
    """Tests adicionales para UUID con casos de fallo."""

    def test_invalid_uuid_with_spaces(self):
        assert validate_uuid_string("550e8400 -e29b-41d4-a716-446655440000") is False

    def test_invalid_uuid_missing_digits(self):
        assert validate_uuid_string("550e8400-e29b-41d4-a716-44665544000") is False

    def test_invalid_uuid_invalid_characters(self):
        assert validate_uuid_string("550e8400-e29b-41d4-a716-44665544000g") is False

    def test_invalid_uuid_all_zeros(self):
        assert validate_uuid_string("00000000-0000-0000-0000-000000000000") is True
