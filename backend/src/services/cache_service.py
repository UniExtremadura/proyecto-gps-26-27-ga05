"""Caché en memoria con TTL para consultas de catálogo (TK-007-1)."""
import time
from threading import Lock
from typing import Any, Callable, Dict, Tuple

DEFAULT_TTL_SECONDS = 60


class TTLCache:
    def __init__(self, ttl: int = DEFAULT_TTL_SECONDS):
        self.ttl = ttl
        self._store: Dict[str, Tuple[float, Any]] = {}
        self._lock = Lock()
        self.hits = 0
        self.misses = 0

    def get(self, key: str):
        now = time.time()
        with self._lock:
            entry = self._store.get(key)
            if not entry:
                self.misses += 1
                return None
            expires_at, value = entry
            if expires_at < now:
                self._store.pop(key, None)
                self.misses += 1
                return None
            self.hits += 1
            return value

    def set(self, key: str, value: Any, ttl: int | None = None):
        with self._lock:
            self._store[key] = (time.time() + (ttl or self.ttl), value)

    def get_or_set(self, key: str, factory: Callable[[], Any], ttl: int | None = None):
        cached = self.get(key)
        if cached is not None:
            return cached
        value = factory()
        self.set(key, value, ttl)
        return value

    def invalidate(self, prefix: str = ""):
        with self._lock:
            if not prefix:
                self._store.clear()
                return
            for key in [key for key in self._store if key.startswith(prefix)]:
                self._store.pop(key, None)

    def stats(self) -> Dict[str, Any]:
        return {"keys": len(self._store), "hits": self.hits, "misses": self.misses, "ttl": self.ttl}


catalog_cache = TTLCache()
