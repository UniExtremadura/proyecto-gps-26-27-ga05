"""Rate limiting por IP con ventana deslizante (TK-016-1)."""
import time
from collections import defaultdict, deque
from threading import Lock
from typing import Deque, Dict, Tuple

AUTH_PATH_PREFIX = "/api/auth"
AUTH_LIMIT = 10
GLOBAL_LIMIT = 100
WINDOW_SECONDS = 60


class SlidingWindowLimiter:
    def __init__(self, window_seconds: int = WINDOW_SECONDS):
        self.window_seconds = window_seconds
        self._hits: Dict[str, Deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def _prune(self, key: str, now: float) -> Deque[float]:
        hits = self._hits[key]
        while hits and now - hits[0] > self.window_seconds:
            hits.popleft()
        return hits

    def allow(self, key: str, limit: int) -> Tuple[bool, int]:
        now = time.time()
        with self._lock:
            hits = self._prune(key, now)
            if len(hits) >= limit:
                retry_after = max(1, int(self.window_seconds - (now - hits[0])))
                return False, retry_after
            hits.append(now)
            return True, 0

    def reset(self):
        with self._lock:
            self._hits.clear()


limiter = SlidingWindowLimiter()


def limit_for_path(path: str) -> int:
    return AUTH_LIMIT if path.startswith(AUTH_PATH_PREFIX) else GLOBAL_LIMIT


def client_ip(request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return getattr(request.client, "host", "unknown") or "unknown"
