from typing import Any, Dict, List
from decimal import Decimal
from datetime import datetime


def format_currency(value: float, currency: str = "$", decimals: int = 2) -> str:
    if not isinstance(value, (int, float)):
        return f"{currency}0.00"
    
    formatted = f"{value:,.{decimals}f}"
    return f"{currency}{formatted}"


def format_percentage(value: float, decimals: int = 2) -> str:
    if not isinstance(value, (int, float)):
        return "0%"
    
    return f"{value:.{decimals}f}%"


def format_phone(phone: str) -> str:
    digits = ''.join(filter(str.isdigit, phone))
    
    if len(digits) == 10:
        return f"+1 ({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11:
        return f"+{digits[0]} ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    
    return phone


def format_date(date: datetime, format_str: str = "%d/%m/%Y") -> str:
    if not isinstance(date, datetime):
        return ""
    
    return date.strftime(format_str)


def format_datetime(date: datetime, format_str: str = "%d/%m/%Y %H:%M") -> str:
    if not isinstance(date, datetime):
        return ""
    
    return date.strftime(format_str)


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def capitalize_words(text: str) -> str:
    return ' '.join(word.capitalize() for word in text.split())


def slugify(text: str) -> str:
    import re
    
    text = text.lower()
    
    # Reemplazar acentos agudos y graves
    text = text.replace('á', 'a').replace('é', 'e').replace('í', 'i')
    text = text.replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
    text = text.replace('à', 'a').replace('è', 'e').replace('ì', 'i')
    text = text.replace('ò', 'o').replace('ù', 'u')
        
    text = re.sub(r'[^\w\s\-]', '', text)
        
    text = re.sub(r'[\s]+', '-', text)
        
    text = re.sub(r'\-+', '-', text)
    
    return text.strip('-')
