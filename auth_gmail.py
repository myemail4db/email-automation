from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

from src.config import GOOGLE_CREDENTIALS_FILE, GOOGLE_TOKEN_FILE

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
]



def main():
    if not GOOGLE_CREDENTIALS_FILE:
        raise RuntimeError("Missing GOOGLE_CREDENTIALS_FILE in environment.")

    if not GOOGLE_TOKEN_FILE:
        raise RuntimeError("Missing GOOGLE_TOKEN_FILE in environment.")

    if not Path(GOOGLE_CREDENTIALS_FILE).exists():
        raise RuntimeError(
            f"Credentials file not found: {GOOGLE_CREDENTIALS_FILE}"
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        str(GOOGLE_CREDENTIALS_FILE),
        SCOPES,
    )

    creds = flow.run_local_server(port=0)

    Path(GOOGLE_TOKEN_FILE).write_text(creds.to_json(), encoding="utf-8")
    print(f"[AUTH] token.json created at: {GOOGLE_TOKEN_FILE}")


if __name__ == "__main__":
    main()
