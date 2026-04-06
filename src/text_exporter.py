from pathlib import Path

from src.config import config
from src.text_filter import clean_email_body
from src.utils.date_utils import format_email_date



def build_email_header(subject, sender, date, status, format_type, file_name):
    line = "=" * 60

    fields = [
        ("Subject", subject or "No Subject"),
        ("From", sender or "Unknown Sender"),
        ("Date", format_email_date(date)),
        ("Workflow Status", status),
        ("Export Format", format_type),
        ("File Name", file_name),
    ]

    header_lines = [line, "EMAIL DETAILS", line]

    for label, value in fields:
        header_lines.append(f"{label:<18}: {value}")

    header_lines.append(line)
    header_lines.append("")

    return "\n".join(header_lines)



def build_safe_stem(subject: str) -> str:
    fallback_prefix = config["naming"]["fallback_prefix"]
    max_length = config["naming"]["max_filename_length"]

    safe_subject = "".join(c for c in subject if c.isalnum() or c in (" ", "_")).strip()
    safe_subject = safe_subject[:max_length].strip()
    return safe_subject or fallback_prefix



def save_email_to_text(subject, sender, date, body, output_dir, status="processed_review", format_type="text"):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_stem = build_safe_stem(subject or "")
    file_path = output_dir / f"{safe_stem}.txt"

    counter = 1
    while file_path.exists():
        file_path = output_dir / f"{safe_stem}_{counter}.txt"
        counter += 1

    cleaned_body = clean_email_body(body)

    header = build_email_header(
        subject=subject,
        sender=sender,
        date=date,
        status=status,
        format_type=format_type,
        file_name=file_path.name,
    )

    file_path.write_text(header + cleaned_body, encoding="utf-8")
    return str(file_path)
