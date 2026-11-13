
"""Pruebas del limitador de peticiones (TK-016-1)."""
from security.rate_limiter import SlidingWindowLimiter, limit_for_path


def test_auth_limit_is_stricter_than_global_limit():
    assert limit_for_path("/api/auth/local/login") == 10
    assert limit_for_path("/api/products") == 100


def test_limiter_blocks_after_limit():
    limiter = SlidingWindowLimiter(window_seconds=60)
    for _ in range(3):
        allowed, _ = limiter.allow("127.0.0.1", 3)
        assert allowed is True

    allowed, retry_after = limiter.allow("127.0.0.1", 3)
    assert allowed is False
    assert retry_after >= 1
