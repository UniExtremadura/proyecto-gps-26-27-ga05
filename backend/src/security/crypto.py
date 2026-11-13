"""Cifrado AES-256 de campos sensibles en reposo (TK-017-1)."""
import base64
import hashlib
import hmac
import os
from typing import Any

try:  # AES-256-GCM real cuando la dependencia está disponible.
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:  # pragma: no cover - fallback para entornos mínimos.
    AESGCM = None

ENCRYPTED_PREFIX = "enc:v1:"
DEFAULT_SECRET = "subsonic-dev-field-key-change-me"


def _secret() -> bytes:
    return hashlib.sha256(os.getenv("FIELD_ENCRYPTION_KEY", DEFAULT_SECRET).encode("utf-8")).digest()


def _keystream(length: int, nonce: bytes) -> bytes:
    """Deriva un keystream determinista a partir de HMAC-SHA256 (fallback)."""
    secret = _secret()
    output = bytearray()
    counter = 0
    while len(output) < length:
        block = hmac.new(secret, nonce + counter.to_bytes(4, "big"), hashlib.sha256).digest()
        output.extend(block)
        counter += 1
    return bytes(output[:length])


def encrypt_field(value: Any) -> str:
    """Cifra un campo de texto y devuelve un valor con prefijo enc:v1:."""
    text = "" if value is None else str(value)
    if not text or text.startswith(ENCRYPTED_PREFIX):
        return text
    nonce = os.urandom(12 if AESGCM else 16)
    raw = text.encode("utf-8")
    if AESGCM:
        cipher = AESGCM(_secret()).encrypt(nonce, raw, None)
    else:
        cipher = bytes(a ^ b for a, b in zip(raw, _keystream(len(raw), nonce)))
    payload = nonce + cipher
    return ENCRYPTED_PREFIX + base64.urlsafe_b64encode(payload).decode("ascii")


def decrypt_field(value: Any) -> str:
    """Descifra un campo previamente cifrado. Los valores sin prefijo se devuelven igual."""
    text = "" if value is None else str(value)
    if not text.startswith(ENCRYPTED_PREFIX):
        return text
    try:
        payload = base64.urlsafe_b64decode(text[len(ENCRYPTED_PREFIX):].encode("ascii"))
        nonce_len = 12 if AESGCM else 16
        nonce, cipher = payload[:nonce_len], payload[nonce_len:]
        if AESGCM:
            raw = AESGCM(_secret()).decrypt(nonce, cipher, None)
        else:
            raw = bytes(a ^ b for a, b in zip(cipher, _keystream(len(cipher), nonce)))
        return raw.decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return ""


def mask_sensitive(value: Any) -> str:
    """Enmascara valores sensibles para logs y respuestas públicas."""
    text = "" if value is None else str(value)
    if len(text) <= 4:
        return "***"
    return text[:2] + "***" + text[-2:]
