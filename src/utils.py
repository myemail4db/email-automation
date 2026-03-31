import re
from pathlib import Path


def sanitize_filename(name: str, max_length: int = 100) -> str:
    if not name:
        name = "job_email"

    name = re.sub(r'[<>:"/\\|?*\n\r\t]+', "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    name = name[:max_length].rstrip(" .")

    return name or "job_email"


def ensure_folder(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def clean_text(value: str) -> str:
    if not value:
        return ""
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()