import argparse
from src.processor import export_labeled_emails


def main():
    parser = argparse.ArgumentParser(description="Export labeled Gmail messages.")
    parser.add_argument(
        "--format",
        choices=["text", "word"],
        default="text",
        help="Export format"
    )
    args = parser.parse_args()

    export_labeled_emails(format_type=args.format)


if __name__ == "__main__":
    main()