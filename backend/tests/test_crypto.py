
"""Pruebas del cifrado de campos (TK-017-1)."""
from security.crypto import decrypt_field, encrypt_field, mask_sensitive


def test_encrypt_and_decrypt_roundtrip():
    original = "Calle Falsa 123"
    encrypted = encrypt_field(original)
    assert encrypted.startswith("enc:v1:")
    assert encrypted != original
    assert decrypt_field(encrypted) == original


def test_encrypt_is_idempotent_for_encrypted_values():
    encrypted = encrypt_field("600123456")
    assert encrypt_field(encrypted) == encrypted


def test_mask_sensitive_hides_middle_characters():
    assert mask_sensitive("600123456") == "60***56"
