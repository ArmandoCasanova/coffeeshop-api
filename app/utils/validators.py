import re
from typing import Optional


def validate_email(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False
    
    # No permitir leading dot, trailing dot, o dots consecutivos
    if email.startswith('.') or email.endswith('.'):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    if not phone or not isinstance(phone, str):
        return False
    
    # Remover espacios y caracteres especiales, pero permitir +
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    return len(cleaned) >= 10 and cleaned.isdigit()


def validate_password(password: str, min_length: int = 8, max_length: int = 255) -> bool:
    if not password or not isinstance(password, str):
        return False
    
    if len(password) < min_length or len(password) > max_length:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_upper and has_lower and has_digit


def validate_price(price: float) -> bool:
    if not isinstance(price, (int, float)):
        return False
    
    return price > 0


def validate_discount_percent(percent: float) -> bool:
    if not isinstance(percent, (int, float)):
        return False
    
    return 0 <= percent <= 100


def validate_uuid_string(uuid_str: str) -> bool:
    if not uuid_str or not isinstance(uuid_str, str):
        return False
    
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return re.match(uuid_pattern, uuid_str, re.IGNORECASE) is not None


def validate_name(name: str, min_length: int = 1, max_length: int = 100) -> bool:
    if not name or not isinstance(name, str):
        return False
    
    name = name.strip()
    
    if len(name) < min_length or len(name) > max_length:
        return False
        
    return re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-\.]+$", name) is not None


def validate_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False
    
    url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(url_pattern, url, re.IGNORECASE) is not None


def validate_string_length(value: str, min_length: int = 0, max_length: int = 1000) -> bool:
    if not isinstance(value, str):
        return False
    
    return min_length <= len(value) <= max_length


def validate_integer_range(value: int, min_val: int = 0, max_val: int = 1000000) -> bool:
    if not isinstance(value, int):
        return False
    
    return min_val <= value <= max_val


def validate_alphanumeric(value: str, allow_special: Optional[list] = None) -> bool:
    if not isinstance(value, str):
        return False
    
    if allow_special is None:
        allow_special = []
    
    special_chars = "".join(allow_special)
    pattern = f"^[a-zA-Z0-9{re.escape(special_chars)}]+$"
    
    return re.match(pattern, value) is not None


def validate_enum(value: str, allowed_values: list) -> bool:
    return value in allowed_values


def validate_ipv4(ip: str) -> bool:
    if not ip or not isinstance(ip, str):
        return False
    
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    
    for octet in ip.split('.'):
        if int(octet) > 255:
            return False
    
    return True


def validate_postcode(postcode: str) -> bool:
    if not postcode or not isinstance(postcode, str):
        return False
    
    pattern = r'^[a-zA-Z0-9\-\s]{3,20}$'
    return re.match(pattern, postcode) is not None
