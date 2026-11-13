"""TK-002-3: pruebas de acceso permitido/denegado por rol."""
import pytest
from fastapi import HTTPException
from starlette.requests import Request

from model.roles import has_permission, normalize_role, role_permissions
from security.rbac import require_permission, require_roles
from security.tokens import create_access_token


def _request_with_token(token: str) -> Request:
    return Request({"type": "http", "headers": [(b"authorization", f"Bearer {token}".encode())]})


def test_normalize_role_and_alias():
    assert normalize_role("ORGANIZADOR") == "gestor"
    assert normalize_role("desconocido") == "cliente"


def test_permissions_by_role():
    assert has_permission("admin", "anything")
    assert has_permission("gestor", "events:manage")
    assert not has_permission("cliente", "events:manage")


def test_require_roles_allows_and_denies():
    token = create_access_token("u1", "gestor", "g@example.com")
    request = _request_with_token(token)

    dependency = require_roles("gestor")
    assert dependency(request)["role"] == "gestor"

    with pytest.raises(HTTPException) as exc:
        require_roles("admin")(request)
    assert exc.value.status_code == 403


def test_require_permission_denies_client():
    token = create_access_token("u2", "cliente", "c@example.com")
    with pytest.raises(HTTPException) as exc:
        require_permission("events:manage")(_request_with_token(token))
    assert exc.value.status_code == 403
