import argparse

from src.auth_gmail import main as auth_main
from src.run import main as export_main
from src.send_batch import main as send_main


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Email automation command-line interface."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    auth_parser = subparsers.add_parser(
        "auth",
        help="Authenticate Gmail and generate token.json",
    )
    auth_parser.set_defaults(func=lambda args: auth_main())

    export_parser = subparsers.add_parser(
        "export",
        help="Export labeled Gmail messages to text or Word files",
    )
    export_parser.add_argument(
        "--format",
        choices=["text", "word"],
        default="text",
        help="Export format",
    )
    export_parser.set_defaults(func=lambda args: export_main(format_type=args.format))

    send_parser = subparsers.add_parser(
        "send",
        help="Zip processed files and send the batch email",
    )
    send_parser.set_defaults(func=lambda args: send_main())

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()