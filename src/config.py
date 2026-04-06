from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import os

from dotenv import load_dotenv


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULTS = {
    "labels": {
        "source": "for_friend",
        "processed_review_child": "processed_review",
        "error_child": "error",
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
    "workflow": {
        "skip_manual_review": False,
    },
    "send": {
        "body_text": "Hello,\n\nAttached is the latest batch of reviewed job files.",
        "signature_name": "Email Automation",
    },
    "time": {
        "display_timezone": "America/Los_Angeles",
    },
    "logging": {
        "level": "INFO",
        "file": "email_automation.log",
        "max_bytes": 1048576,
        "backup_count": 10,
        "enable_console": True,
        "retention_enabled": True,
        "retention_max_batches": 100,
        "retention_max_days": 30,
    },
}


# ---------------------------
# Environment helpers
# ---------------------------
def clean_env(value: str | None, default: str = "") -> str:
    if value is None:
        return default

    value = value.strip()

    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        value = value[1:-1].strip()

    return value



def env_or_default(name: str, default: str) -> str:
    value = clean_env(os.getenv(name))
    return value if value else default



def parse_bool(name: str, default: bool) -> bool:
    raw = clean_env(os.getenv(name))
    if raw == "":
        return default

    normalized = raw.lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False

    raise RuntimeError(
        f"Invalid boolean value for {name}: {raw}. Use True or False."
    )



def parse_int(name: str, default: int, minimum: int | None = None) -> int:
    raw = clean_env(os.getenv(name))
    if raw == "":
        value = default
    else:
        try:
            value = int(raw)
        except ValueError as exc:
            raise RuntimeError(
                f"Invalid integer value for {name}: {raw}"
            ) from exc

    if minimum is not None and value < minimum:
        raise RuntimeError(f"{name} must be >= {minimum}, got {value}")

    return value



def normalize_env_text(value: str | None, default: str) -> str:
    raw = clean_env(value)
    text = raw if raw else default
    return text.replace("\\n", "\n")



def resolve_project_path(raw_value: str | None, default_name: str) -> Path:
    value = clean_env(raw_value)
    relative = Path(value) if value else Path(default_name)
    if relative.is_absolute():
        return relative
    return PROJECT_ROOT / relative



def build_gmail_label_path(root_label: str, child_label: str) -> str:
    root = root_label.strip("/")
    child = child_label.strip("/")
    return f"{root}/{child}" if child else root



def validate_child_label(name: str, value: str) -> str:
    cleaned = clean_env(value)
    if "/" in cleaned:
        raise RuntimeError(
            f"{name} should only contain the child label name, not the full path. "
            f"Example: processed_review instead of for_friend/processed_review"
        )
    return cleaned


# ---------------------------
# Build config from .env
# ---------------------------
source_label = env_or_default("GMAIL_LABEL_SOURCE", DEFAULTS["labels"]["source"])
processed_review_child = validate_child_label(
    "GMAIL_LABEL_PROCESSED_REVIEW",
    env_or_default(
        "GMAIL_LABEL_PROCESSED_REVIEW",
        DEFAULTS["labels"]["processed_review_child"],
    ),
)
error_child = validate_child_label(
    "GMAIL_LABEL_ERROR",
    env_or_default("GMAIL_LABEL_ERROR", DEFAULTS["labels"]["error_child"]),
)

processed_review_dir_name = env_or_default(
    "LOCAL_PROCESSED_REVIEW_DIR", DEFAULTS["local_folders"]["processed_review"]
)
ready_to_send_dir_name = env_or_default(
    "LOCAL_READY_TO_SEND_DIR", DEFAULTS["local_folders"]["ready_to_send"]
)
sent_archive_dir_name = env_or_default(
    "LOCAL_SENT_ARCHIVE_DIR", DEFAULTS["local_folders"]["sent_archive"]
)
error_dir_name = env_or_default(
    "LOCAL_ERROR_DIR", DEFAULTS["local_folders"]["error"]
)

config = {
    "provider": "gmail",
    "labels": {
        "source": source_label,
        "processed_review": build_gmail_label_path(source_label, processed_review_child),
        "error": build_gmail_label_path(source_label, error_child),
    },
    "local_folders": {
        "processed_review": processed_review_dir_name,
        "ready_to_send": ready_to_send_dir_name,
        "sent_archive": sent_archive_dir_name,
        "error": error_dir_name,
        "logs": DEFAULTS["local_folders"]["logs"],
    },
    "naming": {
        "fallback_prefix": env_or_default(
            "FALLBACK_PREFIX", DEFAULTS["naming"]["fallback_prefix"]
        ),
        "zip_prefix": env_or_default("ZIP_PREFIX", DEFAULTS["naming"]["zip_prefix"]),
        "max_filename_length": parse_int(
            "MAX_FILENAME_LENGTH",
            DEFAULTS["naming"]["max_filename_length"],
            minimum=10,
        ),
    },
    "safety": {
        "test_mode": parse_bool("TEST_MODE", DEFAULTS["safety"]["test_mode"]),
        "send_emails": parse_bool(
            "SEND_EMAILS", DEFAULTS["safety"]["send_emails"]
        ),
        "continue_on_error": parse_bool(
            "CONTINUE_ON_ERROR", DEFAULTS["safety"]["continue_on_error"]
        ),
    },
    "time": {
        "display_timezone": env_or_default(
            "DISPLAY_TIMEZONE", DEFAULTS["time"]["display_timezone"]
        ),
    },
    "send": {
        "body": {
            "text": normalize_env_text(
                os.getenv("SEND_BODY_TEXT"), DEFAULTS["send"]["body_text"]
            ),
        },
        "signature": {
            "name": env_or_default(
                "SEND_SIGNATURE_NAME", DEFAULTS["send"]["signature_name"]
            ),
        },
    },
    "workflow": {
        "skip_manual_review": parse_bool(
            "SKIP_MANUAL_REVIEW", DEFAULTS["workflow"]["skip_manual_review"]
        ),
    },
    "logging": {
        "level": env_or_default("LOG_LEVEL", DEFAULTS["logging"]["level"]).upper(),
        "dir": DEFAULTS["local_folders"]["logs"],
        "file": env_or_default("LOG_FILE", DEFAULTS["logging"]["file"]),
        "max_bytes": parse_int(
            "LOG_MAX_BYTES", DEFAULTS["logging"]["max_bytes"], minimum=1
        ),
        "backup_count": parse_int(
            "LOG_BACKUP_COUNT", DEFAULTS["logging"]["backup_count"], minimum=0
        ),
        "enable_console": parse_bool(
            "LOG_ENABLE_CONSOLE", DEFAULTS["logging"]["enable_console"]
        ),
        "retention_enabled": parse_bool(
            "LOG_RETENTION_ENABLED", DEFAULTS["logging"]["retention_enabled"]
        ),
        "retention_max_batches": parse_int(
            "LOG_RETENTION_MAX_BATCHES",
            DEFAULTS["logging"]["retention_max_batches"],
            minimum=1,
        ),
        "retention_max_days": parse_int(
            "LOG_RETENTION_MAX_DAYS",
            DEFAULTS["logging"]["retention_max_days"],
            minimum=1,
        ),
    },
}

PATHS = {
    "processed_review": resolve_project_path(
        os.getenv("LOCAL_PROCESSED_REVIEW_DIR"), processed_review_dir_name
    ),
    "ready_to_send": resolve_project_path(
        os.getenv("LOCAL_READY_TO_SEND_DIR"), ready_to_send_dir_name
    ),
    "sent_archive": resolve_project_path(
        os.getenv("LOCAL_SENT_ARCHIVE_DIR"), sent_archive_dir_name
    ),
    "error": resolve_project_path(os.getenv("LOCAL_ERROR_DIR"), error_dir_name),
    "logs": PROJECT_ROOT / config["logging"]["dir"],
}

SENDER_EMAIL = clean_env(os.getenv("SENDER_EMAIL"))
RECIPIENT_EMAIL = clean_env(os.getenv("RECIPIENT_EMAIL"))

GOOGLE_CREDENTIALS_FILE = resolve_project_path(
    os.getenv("GOOGLE_CREDENTIALS_FILE"), "credentials.json"
)
GOOGLE_TOKEN_FILE = resolve_project_path(os.getenv("GOOGLE_TOKEN_FILE"), "token.json")

SEND_EMAILS = config["safety"]["send_emails"]
TEST_MODE = config["safety"]["test_mode"]
CONTINUE_ON_ERROR = config["safety"]["continue_on_error"]


def get_path(name: str) -> Path:
    return PATHS[name]



def get_display_timezone() -> ZoneInfo:
    tz_name = config["time"]["display_timezone"]
    try:
        return ZoneInfo(tz_name)
    except ZoneInfoNotFoundError as exc:
        raise RuntimeError(f"Invalid DISPLAY_TIMEZONE value: {tz_name}") from exc



def ensure_required_directories() -> None:
    for path in PATHS.values():
        path.mkdir(parents=True, exist_ok=True)



def require_send_config() -> None:
    missing = []
    if not SENDER_EMAIL:
        missing.append("SENDER_EMAIL")
    if not RECIPIENT_EMAIL:
        missing.append("RECIPIENT_EMAIL")

    if missing:
        raise RuntimeError(
            "Missing required .env values for sending: " + ", ".join(missing)
        )



def get_runtime_summary() -> dict:
    return {
        "project_root": str(PROJECT_ROOT),
        "labels": config["labels"],
        "local_folders": {name: str(path) for name, path in PATHS.items()},
        "safety": config["safety"],
        "time": config["time"],
        "logging": config["logging"],
    }



def _validate_unique_local_paths() -> None:
    folders = {
        name: str(path.resolve())
        for name, path in PATHS.items()
        if name != "logs"
    }
    seen: dict[str, str] = {}
    for name, resolved in folders.items():
        if resolved in seen:
            raise RuntimeError(
                f"Duplicate local folder configuration detected: {name} and {seen[resolved]} both resolve to {resolved}"
            )
        seen[resolved] = name



def _validate_logging_file_name() -> None:
    log_file = config["logging"]["file"]
    if not log_file or Path(log_file).name != log_file:
        raise RuntimeError(
            "LOG_FILE must be a file name only, not a path. The logs directory is fixed automatically."
        )



def _validate_labels() -> None:
    source = config["labels"]["source"]
    if not source:
        raise RuntimeError("GMAIL_LABEL_SOURCE cannot be blank.")

    if config["labels"]["processed_review"] == source:
        raise RuntimeError("Processed review label cannot be the same as source label.")

    if config["labels"]["error"] == source:
        raise RuntimeError("Error label cannot be the same as source label.")


_validate_unique_local_paths()
_validate_logging_file_name()
_validate_labels()
ensure_required_directories()
