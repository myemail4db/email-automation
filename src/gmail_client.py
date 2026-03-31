import base64
import os
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Dict, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


class GmailClient:
    def __init__(self, token_file: str = "token.json"):
        self.token_file = token_file
        self.service = self._build_service()

    def _build_service(self):
        creds = None

        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise RuntimeError(
                    "Missing or invalid token.json. Run your Gmail auth step first."
                )

            with open(self.token_file, "w") as token:
                token.write(creds.to_json())

        return build("gmail", "v1", credentials=creds)

    def get_label_map(self) -> Dict[str, str]:
        results = self.service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])
        return {label["name"]: label["id"] for label in labels}

    def list_message_ids_by_label(self, label_name: str, max_results: int = 25) -> List[str]:
        label_map = self.get_label_map()
        label_id = label_map.get(label_name)

        if not label_id:
            raise ValueError(f"Label not found in Gmail: {label_name}")

        response = (
            self.service.users()
            .messages()
            .list(userId="me", labelIds=[label_id], maxResults=max_results)
            .execute()
        )

        messages = response.get("messages", [])
        return [msg["id"] for msg in messages]

    def get_message(self, message_id: str) -> dict:
        return (
            self.service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )

    def modify_labels(
        self,
        message_id: str,
        add_label_ids: Optional[List[str]] = None,
        remove_label_ids: Optional[List[str]] = None,
    ) -> dict:
        body = {
            "addLabelIds": add_label_ids or [],
            "removeLabelIds": remove_label_ids or [],
        }

        return (
            self.service.users()
            .messages()
            .modify(userId="me", id=message_id, body=body)
            .execute()
        )

    @staticmethod
    def _decode_base64(data: str) -> str:
        if not data:
            return ""
        padded = data + "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode(padded).decode("utf-8", errors="replace")

    def extract_message_data(self, message: dict) -> Dict[str, str]:
        payload = message.get("payload", {})
        headers = payload.get("headers", [])

        header_map = {h["name"].lower(): h["value"] for h in headers}

        subject = header_map.get("subject", "(no subject)")
        sender = header_map.get("from", "")
        to = header_map.get("to", "")
        date_raw = header_map.get("date", "")

        body_text = self._extract_body(payload)

        try:
            parsed_date = parsedate_to_datetime(date_raw).isoformat()
        except Exception:
            parsed_date = date_raw

        return {
            "id": message.get("id", ""),
            "thread_id": message.get("threadId", ""),
            "subject": subject,
            "from": sender,
            "to": to,
            "date": parsed_date,
            "snippet": message.get("snippet", ""),
            "body": body_text,
        }

    def _extract_body(self, payload: dict) -> str:
        mime_type = payload.get("mimeType", "")
        body = payload.get("body", {})
        data = body.get("data")

        if mime_type == "text/plain" and data:
            return self._decode_base64(data)

        parts = payload.get("parts", [])
        for part in parts:
            part_mime = part.get("mimeType", "")
            part_body = part.get("body", {})
            part_data = part_body.get("data")

            if part_mime == "text/plain" and part_data:
                return self._decode_base64(part_data)

        for part in parts:
            nested_parts = part.get("parts", [])
            for nested in nested_parts:
                nested_mime = nested.get("mimeType", "")
                nested_data = nested.get("body", {}).get("data")
                if nested_mime == "text/plain" and nested_data:
                    return self._decode_base64(nested_data)

        if data:
            return self._decode_base64(data)

        return ""