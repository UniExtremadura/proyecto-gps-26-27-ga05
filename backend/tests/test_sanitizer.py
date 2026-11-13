
"""Pruebas de saneado de entradas (TK-016-2)."""
from security.sanitizer import contains_dangerous_payload, sanitize_text


def test_script_tags_are_removed():
    cleaned = sanitize_text("<script>alert('xss')</script>Hola")
    assert "<script" not in cleaned
    assert "Hola" in cleaned


def test_sqli_payload_is_detected():
    assert contains_dangerous_payload({"email": "admin' OR 1=1 --"}) is True


def test_clean_payload_is_allowed():
    assert contains_dangerous_payload({"email": "cliente@subsonicfest.com"}) is False
