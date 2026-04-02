from src.zip_service import create_zip_from_processed, archive_processed_files


def main():
    print("[SEND_BATCH] Starting batch process...")

    zip_path, files = create_zip_from_processed()

    if not zip_path:
        print("[SEND_BATCH] No files to process. Exiting.")
        return

    print(f"[SEND_BATCH] Zip created: {zip_path}")

    # For now, skip email sending
    print("[SEND_BATCH] Email sending is currently disabled.")

    archive_processed_files(files)

    print("[SEND_BATCH] Batch process completed.")


if __name__ == "__main__":
    main()