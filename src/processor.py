from src.text_exporter import save_email_to_text
from src.word_exporter import save_email_to_word
from src.error_handler import move_file_to_error
from src.config import PATHS, config
from src.gmail_client import GmailClient
from pathlib import Path
import shutil
import os

TEST_ERROR_MODE = os.getenv("TEST_ERROR_MODE") == "true"

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

def export_labeled_emails(format_type="text"):
    # Output results for summary table
    # example: [{"status": "Success", "path": "/path/to/file.txt"}, 
    #           {"status": "Error: <error message>", "path": "/path/to/error_file.txt"}]
    results = []

    labels = config["labels"]

    input_label = labels["source"]
    processed_label = labels["processed_review"]
    error_label = labels["error"]

    gmail = GmailClient()
    label_map = gmail.get_label_map()

    message_ids = gmail.list_message_ids_by_label(input_label)
    print(f"Found {len(message_ids)} email(s) under label '{input_label}'")

    for msg_id in message_ids:
        saved_file_path = None

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
                    PATHS["processed_review"],
                    status="processed_review",
                    format_type="text"
                )
            elif format_type == "word":
                saved_file_path = save_email_to_word(
                    subject,
                    sender,
                    date,
                    body,
                    PATHS["processed_review"],
                    status="processed_review",
                    format_type="word"
                )
            else:
                raise ValueError(f"Unsupported format_type: {format_type}")

            print(f"Saved: {saved_file_path}")
            results.append({
                "status": "processed_review",
                "path": str(saved_file_path)
            })

            # success label handling
            gmail.modify_labels(
                msg_id,
                add_label_ids=[label_map[processed_label]],
                remove_label_ids=[label_map[input_label]],
            )

            print(f"[SUCCESS] {subject} → processed_review")

        except Exception as e:
            print(f"Error processing message {msg_id}: {e}")

            if saved_file_path and os.path.exists(saved_file_path):
                error_file_path = move_file_to_error(saved_file_path, PATHS["error"])
                print(f"[ERROR] File moved to: {error_file_path}")
                results.append({
                    "status": "Error",
                    "path": str(error_file_path)
                })
            else:
                print(f"[ERROR] No file was saved for message {msg_id}")

            # error label handling
            gmail.modify_labels(
                msg_id,
                add_label_ids=[label_map[error_label]],
                remove_label_ids=[label_map[input_label]],
            )

            print(f"[ERROR] {msg_id}: {e}")

    # ALWAYS print summary after processing all emails
    print_export_summary(results)