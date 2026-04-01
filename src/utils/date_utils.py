from datetime import datetime
import os


def format_email_date(date_str):
    if not date_str:
        return "Unknown Date"

    try:
        dt = datetime.fromisoformat(date_str)

        if os.name == "nt":
            hour_format = "%#I"
        else:
            hour_format = "%-I"

        formatted = dt.strftime(f"%A, %B %d, %Y, {hour_format}:%M %p")

        tz_name = dt.tzname()
        if tz_name:
            formatted = f"{formatted} {tz_name}"

        return formatted

    except Exception:
        return date_str