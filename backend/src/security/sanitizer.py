"""Saneado de entradas contra XSS e inyección (TK-016-2)."""
import html
import re
from typing import Any

SCRIPT_PATTERN = re.compile(r"<\s*script\b[^>]*>.*?<\s*/\s*script\b[^>]*>", re.IGNORECASE | re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
SQLI_PATTERN = re.compile(
    r"(\b(union\s+select|drop\s+table|insert\s+into|delete\s+from)\b)|('\s*or\s*'?\d+'?\s*=\s*'?\d+)|(--\s)|(/\*.*?\*/)",
    re.IGNORECASE | re.DOTALL,
)
MAX_TEXT_LENGTH = 2000


def sanitize_text(value: str) -> str:
    """Elimina etiquetas y escapa entidades HTML."""
    text = SCRIPT_PATTERN.sub("", str(value))
    text = TAG_PATTERN.sub("", text)
    text = html.escape(text, quote=True)
    return text[:MAX_TEXT_LENGTH]


def is_dangerous(value: str) -> bool:
    text = str(value)
    return bool(SCRIPT_PATTERN.search(text) or SQLI_PATTERN.search(text))


def sanitize_payload(payload: Any) -> Any:
    """Recorre diccionarios y listas saneando todas las cadenas."""
    if isinstance(payload, dict):
        return {sanitize_text(key): sanitize_payload(value) for key, value in payload.items()}
    if isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]
    if isinstance(payload, str):
        return sanitize_text(payload)
    return payload


def contains_dangerous_payload(payload: Any) -> bool:
    if isinstance(payload, dict):
        return any(contains_dangerous_payload(key) or contains_dangerous_payload(value) for key, value in payload.items())
    if isinstance(payload, list):
        return any(contains_dangerous_payload(item) for item in payload)
    if isinstance(payload, str):
        return is_dangerous(payload)
    return False
