"""Envío de correos con SMTP simulado (TK-011-2)."""
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", 1025))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
MAIL_FROM = os.getenv("MAIL_FROM", "no-reply@subsonicfest.com")

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "emails"


def render_template(name: str, context: dict) -> str:
    path = TEMPLATES_DIR / name
    if not path.exists():
        return str(context)
    html = path.read_text(encoding="utf-8")
    for key, value in context.items():
        html = html.replace("{{" + key + "}}", str(value))
    return html


def send_email(to: str, subject: str, html: str) -> bool:
    """Envía un correo. En desarrollo, si no hay SMTP, lo imprime por consola."""
    message = EmailMessage()
    message["From"] = MAIL_FROM
    message["To"] = to
    message["Subject"] = subject
    message.set_content("Este correo requiere un cliente compatible con HTML.")
    message.add_alternative(html, subtype="html")

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=5) as server:
            if SMTP_USER:
                server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
        return True
    except Exception as exc:
        print(f"[MAIL SIMULADO] Para: {to} | {subject} | {exc}")
        print(html)
        return False


def send_stock_alert(to: str, product_name: str, stock: int, min_stock: int) -> bool:
    html = render_template(
        "stock_alert.html",
        {"product_name": product_name, "stock": stock, "min_stock": min_stock},
    )
    return send_email(to, f"Stock bajo: {product_name}", html)
