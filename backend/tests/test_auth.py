"""TK-001-3: pruebas unitarias de autorización y contraseñas."""
import pytest

from security.password import hash_password, is_strong_password, verify_password
from security.tokens import create_access_token, decode_access_token, revoke_token


def test_hash_password_is_not_plain_text():
    hashed = hash_password("Festival2026!")
    assert hashed != "Festival2026!"
    assert hashed.startswith("$2")


def test_verify_password_ok_and_ko():
    hashed = hash_password("Festival2026!")
    assert verify_password("Festival2026!", hashed) is True
    assert verify_password("festival2026", hashed) is False


@pytest.mark.parametrize(
    "password,expected",
    [
        ("Festival2026!", True),
        ("festival2026", False),
        ("FESTIVAL!", False),
        ("Ab1", False),
        ("", False),
    ],
)
def test_password_strength(password, expected):
    assert is_strong_password(password) is expected


def test_jwt_contains_role_and_email():
    token = create_access_token("uid-123", "gestor", "gestor@example.com")
    claims = decode_access_token(token)
    assert claims["uid"] == "uid-123"
    assert claims["role"] == "gestor"
    assert claims["email"] == "gestor@example.com"


def test_revoked_token_is_rejected():
    token = create_access_token("uid-456", "cliente", "cliente@example.com")
    revoke_token(token)
    with pytest.raises(Exception):
        decode_access_token(token)
