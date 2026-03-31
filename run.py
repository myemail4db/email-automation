# from src.processor import export_labeled_emails

# EXPORT_FORMAT = "text"   # or "word"

# export_labeled_emails(format_type=EXPORT_FORMAT)

import argparse

from src.processor import export_labeled_emails


def main():
    parser = argparse.ArgumentParser(description="Export labeled Gmail emails to text or Word.")
    parser.add_argument(
        "--format",
        choices=["text", "word"],
        default="text",
        help="Output format: text or word",
    )

    args = parser.parse_args()
    export_labeled_emails(format_type=args.format)


if __name__ == "__main__":
    main()