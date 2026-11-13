"""Minificador básico de assets para producción (TK-007-2).

Uso:
    python frontend/build/minify.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist"


def minify_css(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"\s+", " ", text)
    return re.sub(r"\s*([{}:;,])\s*", r"\1", text).strip()


def minify_js(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    lines = [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("//")]
    return "\n".join(lines)


def main():
    OUTPUT.mkdir(exist_ok=True)
    for folder, suffix, minifier in (("css", ".css", minify_css), ("js", ".js", minify_js)):
        target = OUTPUT / folder
        target.mkdir(exist_ok=True)
        for path in (ROOT / folder).glob(f"*{suffix}"):
            minified = minifier(path.read_text(encoding="utf-8"))
            (target / path.name).write_text(minified, encoding="utf-8")
    print(f"Assets minificados en {OUTPUT}")


if __name__ == "__main__":
    main()
