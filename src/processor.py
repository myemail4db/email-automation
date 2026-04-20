from pathlib import Path
import os
import base64
from bs4 import BeautifulSoup
import re

from src.config import CONTINUE_ON_ERROR, PATHS, config
from src.error_handler import move_file_to_error
from src.gmail_client import GmailClient
from src.text_exporter import save_email_to_text
from src.utils.batch_utils import format_item_block, format_run_end, format_run_start
from src.utils.error_utils import create_error_report
from src.word_exporter import save_email_to_word

TEST_ERROR_MODE = os.getenv("TEST_ERROR_MODE", "").lower() == "true"

def print_export_summary(results):
    if not results:
        print("\nNo files processed.\n")
        return

    col1 = "Email Status"
    col2 = "Local File"

    width1 = max(len(col1), *(len(item["status"]) for item in results))
    width2 = max(len(col2), *(len(item["path"]) for item in results))

    border = f"+-{'-' * width1}-+-{'-' * width2}-+"

    print("\nExport Summary:\n")
    print(border)
    print(f"| {col1:<{width1}} | {col2:<{width2}} |")
    print(border)

    for item in results:
        print(f"| {item['status']:<{width1}} | {item['path']:<{width2}} |")

    print(border)
    print()

def categorize_export_error(exc: Exception) -> str:
    if isinstance(exc, ValueError):
        return "validation_error"
    if isinstance(exc, FileNotFoundError):
        return "file_access_error"
    if isinstance(exc, PermissionError):
        return "file_access_error"
    return "unexpected_error"

def decode_gmail_data(data: str) -> str:
    if not data:
        return ""
    padded = data + "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(padded).decode("utf-8", errors="replace")

def extract_gmail_body_from_payload(payload: dict) -> str:
    if not isinstance(payload, dict):
        return ""

    mime_type = payload.get("mimeType", "")
    body_data = payload.get("body", {}).get("data")

    # Non-multipart message with direct body data
    if body_data and mime_type in ("text/html", "text/plain"):
        return decode_gmail_data(body_data)

    parts = payload.get("parts", [])
    if not isinstance(parts, list):
        parts = []

    # Prefer text/html first
    for part in parts:
        if not isinstance(part, dict):
            continue
        if part.get("mimeType") == "text/html":
            part_data = part.get("body", {}).get("data")
            if part_data:
                return decode_gmail_data(part_data)

    # Fallback to text/plain
    for part in parts:
        if not isinstance(part, dict):
            continue
        if part.get("mimeType") == "text/plain":
            part_data = part.get("body", {}).get("data")
            if part_data:
                return decode_gmail_data(part_data)

    # Recursive search for nested multipart structures
    for part in parts:
        if not isinstance(part, dict):
            continue
        nested = extract_gmail_body_from_payload(part)
        if nested:
            return nested

    return ""

def extract_body_text(raw_email) -> str:
    if raw_email is None:
        return ""

    # Case 1: full Gmail raw_message dict
    if isinstance(raw_email, dict) and "payload" in raw_email:
        extracted = extract_gmail_body_from_payload(raw_email.get("payload", {}))
        if extracted:
            print("Extracted Gmail payload body from raw_message, length is", len(extracted))
            raw_email = extracted
        else:
            raw_email = ""

    # Case 2: already-processed email_data dict
    elif isinstance(raw_email, dict):
        body_value = raw_email.get("body", "")
        print("Extracted body from dict, length of body is", len(body_value) if body_value else 0)
        raw_email = body_value or ""

    # By this point, raw_email should be a string. Just to make sure:
    if not isinstance(raw_email, str):
        raw_email = str(raw_email)

    soup = BeautifulSoup(raw_email, "lxml")

    content = (
        (soup.body.decode_contents() if soup.body else None)
        or (soup.div.decode_contents() if soup.div else None)
        or re.split(r"\r?\n\r?\n", raw_email, maxsplit=1)[-1]
    )

    return BeautifulSoup(content, "lxml").get_text("\n", strip=True)

def export_labeled_emails(format_type="text", logger=None, batch_id=None):
    results = []
    labels = config["labels"]
    input_label = labels["source"]
    processed_label = labels["processed_review"]
    error_label = labels["error"]
    processed_review_dir = PATHS["processed_review"]
    error_dir = PATHS["error"]
    gmail = GmailClient()
    label_map = gmail.get_label_map()
    message_ids = gmail.list_message_ids_by_label(input_label)
    total = len(message_ids)
    print(f"Found {total} email(s) under label '{input_label}'")
    if logger and batch_id:
        logger.info(format_run_start(batch_id=batch_id, stage="export", total_items=total))
    processed_count = 0
    success_count = 0
    failed_count = 0

    for index, msg_id in enumerate(message_ids, start=1):
        saved_file_path = None
        subject = "Unknown Subject"
        sender = "Unknown Sender"
        date = ""
        body = ""
        try:
            raw_message = gmail.get_message(msg_id)   # raw_message is a dictionary.
            email_data = gmail.extract_message_data(raw_message)   # email_data is a dictionary.
            subject = email_data.get("subject", "No Subject")
            sender = email_data.get("from", "Unknown Sender")
            date = email_data.get("date", "")
            print("Email_data is ", email_data)

            # Use raw_message so multipart Gmail payloads can be decoded correctly.
            # This still works for non-multipart messages too.
            body = extract_body_text(raw_message)

            print("Processor says 1st look. The subject is ", subject)
            print("And the body length is ", len(body) if body else 0)

            if TEST_ERROR_MODE:
                raise Exception("Test error - forcing failure path")

            if format_type == "text":
                saved_file_path = save_email_to_text(
                    subject,
                    sender,
                    date,
                    body,
                    processed_review_dir,
                    status=config["local_folders"]["processed_review"],
                    format_type="text",
                )
            elif format_type == "word":
                saved_file_path = save_email_to_word(
                    subject,
                    sender,
                    date,
                    body,
                    processed_review_dir,
                    status=config["local_folders"]["processed_review"],
                    format_type="word",
                )
            else:
                raise ValueError(f"Unsupported format_type: {format_type}")

            print(f"Saved: {saved_file_path}")

            results.append({
                "status": config["local_folders"]["processed_review"],
                "path": str(saved_file_path),
            })

            gmail.modify_labels(
                msg_id,
                add_label_ids=[label_map[processed_label]],
                remove_label_ids=[label_map[input_label]],
            )

            print(f"[SUCCESS] {subject} → {config['local_folders']['processed_review']}")

            processed_count += 1
            success_count += 1

            if logger and batch_id:
                logger.info(
                    format_item_block(
                        status="SUCCESS",
                        batch_id=batch_id,
                        stage="export",
                        index=index,
                        total=total,
                        subject=subject,
                        filename=Path(saved_file_path).name if saved_file_path else None,
                        result=f"exported to {config['local_folders']['processed_review']}",
                    )
                )

        except Exception as exc:
            print(f"Error processing message {msg_id}: {exc}")

            if saved_file_path and os.path.exists(saved_file_path):
                error_file_path = move_file_to_error(saved_file_path, error_dir)
                print(f"[ERROR] File moved to: {error_file_path}")
            else:
                error_file_path = create_error_report(
                    msg_id=msg_id,
                    subject=subject,
                    sender=sender,
                    date=date,
                    format_type=format_type,
                    error_message=str(exc),
                    error_dir=error_dir,
                )
                print(f"[ERROR] Error report created: {error_file_path}")

            results.append({"status": "Error", "path": str(error_file_path)})

            gmail.modify_labels(
                msg_id,
                add_label_ids=[label_map[error_label]],
                remove_label_ids=[label_map[input_label]],
            )

            print(f"[ERROR] {msg_id}: {exc}")

            processed_count += 1
            failed_count += 1

            if logger and batch_id:
                logger.error(
                    format_item_block(
                        status="ERROR",
                        batch_id=batch_id,
                        stage="export",
                        index=index,
                        total=total,
                        subject=subject,
                        filename=Path(error_file_path).name if error_file_path else None,
                        result="failed",
                        error_category=categorize_export_error(exc),
                        error_message=str(exc),
                    )
                )

            if not CONTINUE_ON_ERROR:
                break

    if logger and batch_id:
        logger.info(
            format_run_end(
                batch_id=batch_id,
                stage="export",
                processed=processed_count,
                success=success_count,
                failed=failed_count,
            )
        )

    print_export_summary(results)
