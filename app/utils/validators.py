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


def validate_password(password: str, min_length: int = 8) -> bool:
    if not password or len(password) < min_length:
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
