"""
Sends email notifications using a Gmail account + App Password.
Credentials come from environment variables (see app/config.py).
"""

import smtplib
from email.mime.text import MIMEText

from app.config import settings


def send_email(to_address: str, subject: str, body: str) -> bool:
    if not settings.email_username or not settings.email_password:
        print("Email not configured (missing EMAIL_USERNAME/EMAIL_PASSWORD) — skipping send.")
        return False

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.email_from_address or settings.email_username
    msg["To"] = to_address

    try:
        with smtplib.SMTP_SSL(settings.email_smtp_server, settings.email_smtp_port) as server:
            server.login(settings.email_username, settings.email_password)
            server.sendmail(msg["From"], [to_address], msg.as_string())
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False