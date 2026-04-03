from src.zip_service import create_zip_from_processed, archive_processed_files
from src.email_service import send_batch_email


def main():
    print("[SEND_BATCH] Starting batch process...")

    zip_path, files = create_zip_from_processed()

    if not zip_path:
        print("[SEND_BATCH] No files to process. Exiting.")
        return

    print(f"[SEND_BATCH] Zip created: {zip_path}")

    email_sent = send_batch_email(zip_path)

    if email_sent:
        archive_processed_files(files)
        print("[SEND_BATCH] Batch process completed.")
    else:
        print("[SEND_BATCH] Email failed or dry run mode enabled. Files were not archived.")


if __name__ == "__main__":
    main()