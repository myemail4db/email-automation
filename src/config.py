from pathlib import Path
from dotenv import load_dotenv
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from datetime import datetime
import os

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()

# ---------------------------
# Project root (portable)
# ---------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------
# Core config
# ---------------------------

def normalize_env_text(value: str | None, default: str) -> str:
    raw = value if value is not None else default
    return raw.replace("\\n", "\n")



config = {
    "provider": "gmail",
    "labels": {
        "source": "for_friend",
        "processed_review": "for_friend/processed_review",
        "error": "for_friend/error",
    },
    "local_folders": {
        "processed_review": "processed_review",
        "ready_to_send": "ready_to_send",
        "sent_archive": "sent_archive",
        "error": "error",
        "logs": "logs",
    },
    "naming": {
        "fallback_prefix": "job_email",
        "zip_prefix": "job_batch",
        "max_filename_length": 100,
    },
    "safety": {
        "test_mode": True,
        "send_emails": False,
        "continue_on_error": True,
    },
    "time": {
        "display_timezone": os.getenv("DISPLAY_TIMEZONE", "").strip() or None,
    },
    "send": {
        "body": {
            "text": normalize_env_text(
                os.getenv("SEND_BODY_TEXT"),
                "Hello,\n\nAttached is the latest batch of reviewed job files."
            ),
        },
        "signature": {
            "name": os.getenv("SEND_SIGNATURE_NAME", "Email Automation"),
        },
    },
    "workflow": {
        "skip_manual_review": os.getenv("SKIP_MANUAL_REVIEW", "False").strip().lower() == "true",
    },
}

# ---------------------------
# Derived paths
# ---------------------------
PATHS = {
    name: PROJECT_ROOT / folder
    for name, folder in config["local_folders"].items()
}

# ---------------------------
# Environment (private values)
# ---------------------------
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")
GOOGLE_TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE")

if GOOGLE_CREDENTIALS_FILE:
    GOOGLE_CREDENTIALS_FILE = Path(GOOGLE_CREDENTIALS_FILE)

if GOOGLE_TOKEN_FILE:
    GOOGLE_TOKEN_FILE = Path(GOOGLE_TOKEN_FILE)

# ---------------------------
# Email sending config
# ---------------------------
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# ---------------------------
# Flags
# ---------------------------
SEND_EMAILS = os.getenv("SEND_EMAILS", "False").strip().lower() == "true"
TEST_MODE = os.getenv("TEST_MODE", "True").strip().lower() == "true"

# ---------------------------
# Helpers
# ---------------------------
def get_path(name: str) -> Path:
    return PATHS[name]

def get_display_timezone():
    """
    Return the configured display timezone if provided.
    Otherwise return the system's local timezone.
    """
    tz_name = config["time"]["display_timezone"]

    if tz_name:
        try:
            return ZoneInfo(tz_name)
        except ZoneInfoNotFoundError as exc:
            raise RuntimeError(
                f"Invalid DISPLAY_TIMEZONE value: {tz_name}"
            ) from exc

    return datetime.now().astimezone().tzinfo