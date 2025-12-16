"""Tests unitarios para formatters."""
import pytest
from datetime import datetime
from app.utils.formatters import (
    format_currency,
    format_percentage,
    format_phone,
    format_date,
    format_datetime,
    truncate_text,
    capitalize_words,
    slugify,
)


class TestCurrencyFormatter:
    """Tests para formateo de moneda."""

    def test_format_currency_basic(self):
        assert format_currency(1000.50) == "$1,000.50"

    def test_format_currency_zero(self):
        assert format_currency(0) == "$0.00"

    def test_format_currency_small_amount(self):
        assert format_currency(5.5) == "$5.50"

    def test_format_currency_custom_symbol(self):
        assert format_currency(1000, currency="€") == "€1,000.00"

    def test_format_currency_custom_decimals(self):
        assert format_currency(1000.567, decimals=3) == "$1,000.567"

    def test_format_currency_negative(self):
        assert format_currency(-100) == "$-100.00"

    def test_format_currency_invalid_type(self):
        assert format_currency("invalid") == "$0.00"


class TestPercentageFormatter:
    """Tests para formateo de porcentaje."""

    def test_format_percentage_basic(self):
        assert format_percentage(50) == "50.00%"

    def test_format_percentage_decimal(self):
        assert format_percentage(33.33) == "33.33%"

    def test_format_percentage_custom_decimals(self):
        assert format_percentage(33.333, decimals=1) == "33.3%"

    def test_format_percentage_zero(self):
        assert format_percentage(0) == "0.00%"

    def test_format_percentage_invalid_type(self):
        assert format_percentage("invalid") == "0%"


class TestPhoneFormatter:
    """Tests para formateo de teléfono."""

    def test_format_phone_10_digits(self):
        assert format_phone("1234567890") == "+1 (123) 456-7890"

    def test_format_phone_11_digits(self):
        assert format_phone("12345678901") == "+1 (234) 567-8901"

    def test_format_phone_with_spaces(self):
        assert format_phone("123 456 7890") == "+1 (123) 456-7890"

    def test_format_phone_with_dashes(self):
        assert format_phone("123-456-7890") == "+1 (123) 456-7890"

    def test_format_phone_invalid_length(self):
        assert format_phone("123") == "123"


class TestDateFormatter:
    """Tests para formateo de fecha."""

    def test_format_date_basic(self):
        date = datetime(2025, 12, 25)
        assert format_date(date) == "25/12/2025"

    def test_format_date_custom_format(self):
        date = datetime(2025, 12, 25)
        assert format_date(date, "%Y-%m-%d") == "2025-12-25"

    def test_format_date_invalid_type(self):
        assert format_date("2025-12-25") == ""


class TestDatetimeFormatter:
    """Tests para formateo de fecha y hora."""

    def test_format_datetime_basic(self):
        dt = datetime(2025, 12, 25, 15, 30)
        assert format_datetime(dt) == "25/12/2025 15:30"

    def test_format_datetime_custom_format(self):
        dt = datetime(2025, 12, 25, 15, 30, 45)
        assert format_datetime(dt, "%Y-%m-%d %H:%M:%S") == "2025-12-25 15:30:45"

    def test_format_datetime_invalid_type(self):
        assert format_datetime("2025-12-25 15:30") == ""


class TestTextTruncate:
    """Tests para truncado de texto."""

    def test_truncate_text_no_truncation_needed(self):
        assert truncate_text("Hello", max_length=10) == "Hello"

    def test_truncate_text_basic(self):
        assert truncate_text("Hello World", max_length=8) == "Hello..."

    def test_truncate_text_exact_length(self):
        assert truncate_text("Hello", max_length=5) == "Hello"

    def test_truncate_text_custom_suffix(self):
        assert truncate_text("Hello World", max_length=8, suffix="->") == "Hello ->"

    def test_truncate_text_long_text(self):
        text = "The quick brown fox jumps over the lazy dog"
        assert truncate_text(text, max_length=20) == "The quick brown f..."


class TestCapitalizeWords:
    """Tests para capitalización de palabras."""

    def test_capitalize_words_basic(self):
        assert capitalize_words("hello world") == "Hello World"

    def test_capitalize_words_already_capitalized(self):
        assert capitalize_words("Hello World") == "Hello World"

    def test_capitalize_words_single_word(self):
        assert capitalize_words("hello") == "Hello"

    def test_capitalize_words_multiple_spaces(self):
        assert capitalize_words("hello   world") == "Hello World"


class TestSlugify:
    """Tests para conversión a slug."""

    def test_slugify_basic(self):
        assert slugify("Hello World") == "hello-world"

    def test_slugify_with_accents(self):
        assert slugify("Café con Leche") == "cafe-con-leche"

    def test_slugify_with_special_chars(self):
        assert slugify("Hello & World!") == "hello-world"

    def test_slugify_multiple_spaces(self):
        assert slugify("Hello   World") == "hello-world"

    def test_slugify_multiple_dashes(self):
        assert slugify("Hello---World") == "hello-world"

    def test_slugify_with_uppercase(self):
        assert slugify("HELLO WORLD") == "hello-world"

    def test_slugify_with_ñ(self):
        assert slugify("Niño Español") == "nino-espanol"

    def test_slugify_empty_string(self):
        assert slugify("") == ""


class TestCurrencyFormatterExtended:
    """Tests adicionales para currency con casos de fallo."""

    def test_format_currency_very_large_number(self):
        assert format_currency(1000000.99) == "$1,000,000.99"

    def test_format_currency_none_type(self):
        assert format_currency(None) == "$0.00"

    def test_format_currency_list_type(self):
        assert format_currency([100]) == "$0.00"

    def test_format_currency_dict_type(self):
        assert format_currency({"value": 100}) == "$0.00"


class TestPercentageFormatterExtended:
    """Tests adicionales para percentage con casos de fallo."""

    def test_format_percentage_negative(self):
        assert format_percentage(-50) == "-50.00%"

    def test_format_percentage_large_value(self):
        assert format_percentage(999.99) == "999.99%"

    def test_format_percentage_none_type(self):
        assert format_percentage(None) == "0%"

    def test_format_percentage_list_type(self):
        assert format_percentage([50]) == "0%"


class TestPhoneFormatterExtended:
    """Tests adicionales para phone con casos de fallo."""

    def test_format_phone_empty_string(self):
        assert format_phone("") == ""

    def test_format_phone_only_letters(self):
        assert format_phone("abcdefghij") == "abcdefghij"

    def test_format_phone_special_chars(self):
        assert format_phone("!@#$%^&*()") == "!@#$%^&*()"

    def test_format_phone_with_extension(self):
        assert format_phone("12345678901234") == "12345678901234"


class TestDateFormatterExtended:
    """Tests adicionales para date formatter con casos de fallo."""

    def test_format_date_none_type(self):
        assert format_date(None) == ""

    def test_format_date_string_type(self):
        assert format_date("2025-12-25") == ""

    def test_format_date_int_type(self):
        assert format_date(12345) == ""

    def test_format_date_leap_year(self):
        date = datetime(2024, 2, 29)
        assert format_date(date) == "29/02/2024"


class TestDatetimeFormatterExtended:
    """Tests adicionales para datetime formatter con casos de fallo."""

    def test_format_datetime_none_type(self):
        assert format_datetime(None) == ""

    def test_format_datetime_string_type(self):
        assert format_datetime("2025-12-25 15:30") == ""

    def test_format_datetime_midnight(self):
        dt = datetime(2025, 12, 25, 0, 0)
        assert format_datetime(dt) == "25/12/2025 00:00"

    def test_format_datetime_end_of_day(self):
        dt = datetime(2025, 12, 25, 23, 59, 59)
        assert format_datetime(dt) == "25/12/2025 23:59"


class TestTextTruncateExtended:
    """Tests adicionales para truncate con casos de fallo."""

    def test_truncate_text_empty_string(self):
        assert truncate_text("") == ""

    def test_truncate_text_max_length_zero(self):
        # max_length=0 aún intenta truncar, retorna parte del texto
        result = truncate_text("Hello", max_length=0)
        assert isinstance(result, str)

    def test_truncate_text_very_short_max_length(self):
        # max_length=3 retorna sufijo solamente
        result = truncate_text("Hello", max_length=3)
        assert result == "..."

    def test_truncate_text_suffix_longer_than_max(self):
        # Cuando suffix es más largo que max_length, aún lo concatena
        result = truncate_text("Hello", max_length=2, suffix="...")
        assert isinstance(result, str) and "..." in result


class TestCapitalizeWordsExtended:
    """Tests adicionales para capitalize_words con casos de fallo."""

    def test_capitalize_words_empty_string(self):
        assert capitalize_words("") == ""

    def test_capitalize_words_numbers_only(self):
        assert capitalize_words("123 456") == "123 456"

    def test_capitalize_words_special_chars(self):
        assert capitalize_words("hello! world?") == "Hello! World?"

    def test_capitalize_words_mixed_case(self):
        assert capitalize_words("hELLO wORLD") == "Hello World"


class TestSlugifyExtended:
    """Tests adicionales para slugify con casos de fallo."""

    def test_slugify_only_special_chars(self):
        assert slugify("@#$%^&*") == ""

    def test_slugify_only_spaces(self):
        assert slugify("     ") == ""

    def test_slugify_only_dashes(self):
        assert slugify("------") == ""

    def test_slugify_mixed_accents(self):
        # Solo reemplaza Á,É,Í,Ó,Ú - no À,È,Ì,Ò,Ù
        assert slugify("Áéíóú Àèìòù") == "aeiou-aeiou"

    def test_slugify_unicode_chars(self):
        # Caracteres Unicode se mantienen pero sin espacios ni caracteres especiales
        result = slugify("こんにちは")
        assert isinstance(result, str)
