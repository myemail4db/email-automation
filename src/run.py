import argparse
from dotenv import load_dotenv

from src.logging_config import setup_logging
from src.utils.batch_utils import generate_batch_id
from src.processor import export_labeled_emails


def main():
    load_dotenv()

    logger = setup_logging()
    batch_id = generate_batch_id()

    parser = argparse.ArgumentParser(description="Export labeled Gmail messages.")
    parser.add_argument(
        "--format",
        choices=["text", "word"],
        default="text",
        help="Export format"
    )
    args = parser.parse_args()

    export_labeled_emails(
        format_type=args.format,
        logger=logger,
        batch_id=batch_id
    )


if __name__ == "__main__":
    main()