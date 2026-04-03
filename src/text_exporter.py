from src.text_filter import clean_email_body
from src.utils.date_utils import format_email_date
import os
from pathlib import Path
from datetime import datetime
   
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


def save_email_to_text(subject, sender, date, body, output_dir, status="processed_review", format_type="text"):
    safe_subject = "".join(c for c in subject if c.isalnum() or c in (" ", "_")).strip()
    safe_subject = safe_subject[:80] or "email"

    base_filename = f"{safe_subject}.txt"
    file_path = os.path.join(output_dir, base_filename)

    counter = 1

    while os.path.exists(file_path):
        file_path = os.path.join(output_dir, f"{safe_subject}_{counter}.txt")
        counter += 1

    file_name = Path(file_path).name

    cleaned_body = clean_email_body(body)

    header = build_email_header(
        subject=subject,
        sender=sender,
        date=date,
        status=status,
        format_type=format_type,
        file_name=file_name
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(cleaned_body)

    return file_path