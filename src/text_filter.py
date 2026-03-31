import html
import re


def clean_email_body(body: str) -> str:
    if not body:
        return ""

    # Decode HTML entities like &lt; and &#39;
    text = html.unescape(body)

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove common mailer noise
    noise_patterns = [
        r"^Sent from Yahoo Mail.*$",
        r"^Get Outlook for .*?$",
        r"^CAUTION:.*$",
    ]

    lines = text.split("\n")
    filtered_lines = []

    for line in lines:
        stripped = line.strip()

        skip = False
        for pattern in noise_patterns:
            if re.match(pattern, stripped, flags=re.IGNORECASE):
                skip = True
                break

        if not skip:
            filtered_lines.append(line)

    text = "\n".join(filtered_lines)

    # Stop at common reply-chain markers
    reply_markers = [
        r"\nOn .* wrote:\n",
        r"\nFrom: .*",
        r"\n-----Original Message-----",
    ]

    for marker in reply_markers:
        match = re.search(marker, text, flags=re.IGNORECASE)
        if match:
            text = text[:match.start()]
            break

    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()