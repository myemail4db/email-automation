from pathlib import Path


def create_error_report(
    msg_id,
    subject,
    sender,
    date,
    format_type,
    error_message,
    error_dir
):
    safe_subject = "".join(
        c for c in (subject or "email") if c.isalnum() or c in (" ", "_")
    ).strip()

    safe_subject = safe_subject[:80] or "email"

    file_path = Path(error_dir) / f"{safe_subject}_ERROR.txt"

    counter = 1
    while file_path.exists():
        file_path = Path(error_dir) / f"{safe_subject}_ERROR_{counter}.txt"
        counter += 1

    content = "\n".join([
        "=" * 60,
        "ERROR EMAIL DETAILS",
        "=" * 60,
        f"Subject           : {subject or 'No Subject'}",
        f"From              : {sender or 'Unknown Sender'}",
        f"Date              : {date or 'Unknown Date'}",
        f"Workflow Status   : error",
        f"Export Format     : {format_type}",
        f"Message ID        : {msg_id}",
        f"Error             : {error_message}",
        "=" * 60,
        "",
    ])

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return str(file_path)