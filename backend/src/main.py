"""Punto de entrada del backend.

Uso:
    python backend/src/main.py

También se puede arrancar con uvicorn desde ``backend/src``:
    uvicorn controller.controller:app --reload
"""
from __future__ import annotations

import sys
from pathlib import Path

# Permite ejecutar el archivo directamente desde cualquier directorio.
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import uvicorn  # noqa: E402

from config.config import HOST, PORT, RELOAD  # noqa: E402


def main() -> None:
    uvicorn.run(
        "controller.controller:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        log_level="info",
    )


if __name__ == "__main__":
    main()
