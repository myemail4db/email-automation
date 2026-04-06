from pathlib import Path
import os

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
            raw_message = gmail.get_message(msg_id)
            email_data = gmail.extract_message_data(raw_message)

            subject = email_data.get("subject", "No Subject")
            sender = email_data.get("from", "Unknown Sender")
            date = email_data.get("date", "")
            body = email_data.get("body", "")

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
