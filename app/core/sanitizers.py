import bleach
import re
from typing import Any, Dict
from html import unescape


class InputSanitizer:

    ALLOWED_TAGS = []
    ALLOWED_ATTRIBUTES = {}

    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        if not isinstance(value, str):
            return ""
        
        value = value[:max_length]
        
        value = bleach.clean(
            value,
            tags=InputSanitizer.ALLOWED_TAGS,
            attributes=InputSanitizer.ALLOWED_ATTRIBUTES,
            strip=True
        )
        
        value = value.replace('\x00', '')
        value = unescape(value)
        
        return value.strip()

    @staticmethod
    def sanitize_email(email: str) -> str:
        if not isinstance(email, str):
            return ""
        
        email = email.strip().lower()
        email = re.sub(r'\s', '', email)
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return ""
        
        return email

    @staticmethod
    def sanitize_number(value: Any) -> float:
        try:
            num = float(value)
            if not (-1e10 < num < 1e10):
                return 0.0
            return num
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def sanitize_dict(data: Dict) -> Dict:
        if not isinstance(data, dict):
            return {}
        
        sanitized = {}
        for key, value in data.items():
            clean_key = InputSanitizer.sanitize_string(
                str(key), max_length=255
            )
            if isinstance(value, str):
                sanitized[clean_key] = InputSanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[clean_key] = InputSanitizer.sanitize_dict(value)
            elif isinstance(value, (int, float)):
                sanitized[clean_key] = InputSanitizer.sanitize_number(value)
            elif isinstance(value, list):
                sanitized[clean_key] = InputSanitizer.sanitize_list(value)
            elif isinstance(value, bool):
                sanitized[clean_key] = value
            elif value is None:
                sanitized[clean_key] = None
            else:
                sanitized[clean_key] = str(value)
        
        return sanitized

    @staticmethod
    def sanitize_list(data: list) -> list:
        if not isinstance(data, list):
            return []
        
        sanitized = []
        for item in data:
            if isinstance(item, str):
                sanitized.append(InputSanitizer.sanitize_string(item))
            elif isinstance(item, dict):
                sanitized.append(InputSanitizer.sanitize_dict(item))
            elif isinstance(item, list):
                sanitized.append(InputSanitizer.sanitize_list(item))
            elif isinstance(item, (int, float)):
                sanitized.append(InputSanitizer.sanitize_number(item))
            elif isinstance(item, bool):
                sanitized.append(item)
            elif item is None:
                sanitized.append(None)
            else:
                sanitized.append(str(item))
        
        return sanitized

    @staticmethod
    def sanitize_phone(phone: str) -> str:
        if not isinstance(phone, str):
            return ""
        
        phone = re.sub(r'[^\d\+\-\(\)\s]', '', phone)
        phone = phone.replace(' ', '')
        digits = re.sub(r'\D', '', phone)
        if len(digits) < 10 or len(digits) > 15:
            return ""
        
        return phone

    @staticmethod
    def sanitize_url(url: str) -> str:
        if not isinstance(url, str):
            return ""
        
        url = url.strip()
        
        if not url.startswith(('http://', 'https://', 'ws://', 'wss://')):
            return ""
        
        url = re.sub(r'[\x00-\x1f\x7f]', '', url)
        
        return url
