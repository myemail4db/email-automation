from src.text_exporter import save_email_to_text
from src.word_exporter import save_email_to_word
from src.error_handler import move_file_to_error
from src.config import PATHS, config
from src.gmail_client import GmailClient
from src.text_filter import clean_email_body
import shutil
import os

TEST_ERROR_MODE = os.getenv("TEST_ERROR_MODE") == "true"

def export_labeled_emails(format_type="text"):
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

            if format_type == "text":
                saved_file_path = save_email_to_text(
                    subject, sender, date, body, PATHS["jobs_to_review"]
                )
            elif format_type == "word":
                saved_file_path = save_email_to_word(
                    subject, sender, date, body, PATHS["jobs_to_review"]
                )
            else:
                raise ValueError(f"Unsupported format_type: {format_type}")

            print(f"Saved: {saved_file_path}")

            if TEST_ERROR_MODE:
                raise Exception("Test error - forcing failure path")

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
            else:
                print(f"[ERROR] No file was saved for message {msg_id}")

            # error label handling
            gmail.modify_labels(
                msg_id,
                add_label_ids=[label_map[error_label]],
                remove_label_ids=[label_map[input_label]],
            )

            print(f"[ERROR] {msg_id}: {e}")