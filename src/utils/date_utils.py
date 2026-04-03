from datetime import datetime
import os

from src.config import get_display_timezone


def format_email_date(date_str: str) -> str:
    if not date_str:
        return "Unknown Date"

    try:
        dt = datetime.fromisoformat(date_str)

        # Convert to configured or system timezone
        target_tz = get_display_timezone()

        if dt.tzinfo is None:
            # Assume already local if no tz info
            dt = dt.replace(tzinfo=target_tz)
        else:
            dt = dt.astimezone(target_tz)

        # Cross-platform hour formatting
        if os.name == "nt":
            hour_format = "%#I"   # Windows
        else:
            hour_format = "%-I"   # macOS/Linux

        formatted = dt.strftime(f"%A, %B %d, %Y, {hour_format}:%M %p %Z")

        return formatted

    except Exception:
        return date_str