from pathlib import Path

from dotenv import load_dotenv

from src.email_service import send_batch_email
from src.logging_config import setup_logging
from src.utils.batch_utils import (
    format_item_block,
    format_run_end,
    format_run_start,
    generate_batch_id,
)
from src.zip_service import archive_processed_files, create_zip_from_processed


def main():
    load_dotenv()

    logger = setup_logging()
    batch_id = generate_batch_id()

    stage = "send"
    total = 1

    logger.info(format_run_start(batch_id=batch_id, stage=stage, total_items=total))
    print("[SEND_BATCH] Starting batch process...")

    processed_count = 0
    success_count = 0
    failed_count = 0

    zip_path = None
    files = []

    try:
        zip_path, files = create_zip_from_processed()

        if not zip_path:
            processed_count = 1
            failed_count = 1

            logger.error(
                format_item_block(
                    status="ERROR",
                    batch_id=batch_id,
                    stage=stage,
                    index=1,
                    total=1,
                    filename=None,
                    result="failed",
                    error_category="validation_error",
                    error_message="No files found to zip and send",
                )
            )

            print("[SEND_BATCH] No files to process. Exiting.")
            logger.info(
                format_run_end(
                    batch_id=batch_id,
                    stage=stage,
                    processed=processed_count,
                    success=success_count,
                    failed=failed_count,
                )
            )
            return

        print(f"[SEND_BATCH] Zip created: {zip_path}")

        email_sent = send_batch_email(zip_path)

        processed_count = 1

        if email_sent:
            archive_processed_files(files)
            success_count = 1

            logger.info(
                format_item_block(
                    status="SENT",
                    batch_id=batch_id,
                    stage=stage,
                    index=1,
                    total=1,
                    filename=Path(zip_path).name,
                    result="zip emailed and source files archived",
                )
            )

            print("[SEND_BATCH] Batch process completed.")
        else:
            failed_count = 1

            logger.error(
                format_item_block(
                    status="ERROR",
                    batch_id=batch_id,
                    stage=stage,
                    index=1,
                    total=1,
                    filename=Path(zip_path).name if zip_path else None,
                    result="failed",
                    error_category="gmail_send_failure",
                    error_message="Email failed or dry run mode enabled. Files were not archived.",
                )
            )

            print("[SEND_BATCH] Email failed or dry run mode enabled. Files were not archived.")

    except Exception as exc:
        processed_count = 1
        failed_count = 1

        logger.exception(
            format_item_block(
                status="ERROR",
                batch_id=batch_id,
                stage=stage,
                index=1,
                total=1,
                filename=Path(zip_path).name if zip_path else None,
                result="failed",
                error_category="unexpected_error",
                error_message=str(exc),
            )
        )

        print(f"[SEND_BATCH] Unexpected error: {exc}")

    finally:
        logger.info(
            format_run_end(
                batch_id=batch_id,
                stage=stage,
                processed=processed_count,
                success=success_count,
                failed=failed_count,
            )
        )


if __name__ == "__main__":
    main()