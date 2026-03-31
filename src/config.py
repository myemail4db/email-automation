from pathlib import Path
from dotenv import load_dotenv
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
# Core config (your structure)
# ---------------------------
config = {
    "provider": "gmail",
    "labels": {
        "source": "for_friend",
        "processed_review": "for_friend/processed_review",
        "error": "for_friend/error",
    },
    "local_folders": {
        "input": "input",
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
}

# ---------------------------
# Derived paths (VERY useful)
# ---------------------------
PATHS = {
    name: PROJECT_ROOT / folder
    for name, folder in config["local_folders"].items()
}

# Example usage:
# PATHS["jobs_to_review"] → full path object

# ---------------------------
# Environment (private values)
# ---------------------------
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")
GOOGLE_TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE")

# Convert to Path if present
if GOOGLE_CREDENTIALS_FILE:
    GOOGLE_CREDENTIALS_FILE = Path(GOOGLE_CREDENTIALS_FILE)

if GOOGLE_TOKEN_FILE:
    GOOGLE_TOKEN_FILE = Path(GOOGLE_TOKEN_FILE)

# ---------------------------
# Helper (nice convenience)
# ---------------------------
def get_path(name: str) -> Path:
    return PATHS[name]