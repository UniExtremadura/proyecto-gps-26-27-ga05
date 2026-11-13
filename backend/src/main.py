import uvicorn
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.config import HOST, PORT, RELOAD, DEBUG

if __name__ == "__main__":
    print("=" * 50)
    print("Subsonic Festival API - Servidor Principal")
    print(f"Host: {HOST} | Puerto: {PORT} | Debug: {DEBUG}")
    print("=" * 50)
    
    uvicorn.run(
        "controller.controller:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        log_level="info"
    )