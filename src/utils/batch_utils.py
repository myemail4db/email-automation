from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional


LOCAL_TZ = ZoneInfo("America/Los_Angeles")


def local_timestamp() -> str:
    return datetime.now(LOCAL_TZ).strftime("%Y-%m-%d %H:%M:%S")


def generate_batch_id(prefix: str = "job_batch") -> str:
    return f"{prefix}_{datetime.now(LOCAL_TZ).strftime('%Y%m%d_%H%M%S')}"


def _line(width: int = 60, char: str = "=") -> str:
    return char * width


@dataclass
class LogContext:
    batch_id: str
    stage: str


def format_run_start(batch_id: str, stage: str, total_items: int) -> str:
    return "\n".join([
        _line(),
        f"[RUN START][{batch_id}] {stage}",
        f"Timestamp (Local): {local_timestamp()}",
        f"Total Items       : {total_items}",
        _line(),
    ])


def format_run_end(
    batch_id: str,
    stage: str,
    processed: int,
    success: int,
    failed: int,
) -> str:
    return "\n".join([
        _line(),
        f"[RUN END][{batch_id}] {stage}",
        f"Timestamp (Local): {local_timestamp()}",
        f"Processed         : {processed}",
        f"Success           : {success}",
        f"Failed            : {failed}",
        _line(),
    ])


def format_item_block(
    status: str,
    batch_id: str,
    stage: str,
    index: int,
    total: int,
    subject: Optional[str] = None,
    filename: Optional[str] = None,
    result: Optional[str] = None,
    error_category: Optional[str] = None,
    error_message: Optional[str] = None,
) -> str:
    lines = [
        _line(char="-"),
        f"[{status.upper()}][{batch_id}] {stage} ({index}/{total})",
        f"Timestamp (Local): {local_timestamp()}",
        f"Subject          : {subject or 'N/A'}",
        f"Filename         : {filename or 'N/A'}",
        f"Processing Stage : {stage}",
        f"Result           : {result or 'N/A'}",
    ]

    if error_category:
        lines.append(f"Error Category   : {error_category}")

    if error_message:
        lines.append(f"Error Message    : {error_message}")

    lines.append(_line(char="-"))
    return "\n".join(lines)