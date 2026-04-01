import html
import re


REPLY_MARKER_PATTERNS = [
    r"^On .+ wrote:\s*$",
]

NOISE_LINE_PATTERNS = [
    r"^Sent from Yahoo Mail.*$",
    r"^Get Outlook for .*?$",
    r"^CAUTION:.*$",
    r"^WARNING:.*$",
    r"^-+Original Message-+$",
    r"^Begin forwarded message:\s*$",
    r"^-+\s*Forwarded Message\s*-+.*$",
    r"^From:\s+.*$",
    r"^Sent:\s+.*$",
    r"^To:\s+.*$",
    r"^Subject:\s+.*$",
    r"^Cc:\s+.*$",
    r"^Bcc:\s+.*$",
    r"^From my iPhone\s*$",
    r"^Sent from my iPhone\s*$",
    r"^External Email.*$",
    r"^Need help\?\s*Click for assistance\s*$",
    r"To unsubscribe.*?(?=\n\s*\n|\Z)"
    r"^Confidentiality Notice:\s*$",    
]
BLOCK_PATTERNS = [
    r"CONFIDENTIALITY NOTICE:.*?(?=\n\n|\Z)",
    r"How am I doing\?.*?(?=\n\n|\Z)",
    r"(CCPA|CCCPA)\s+Privacy Notice.*?(?=\n\n|\Z)",
    r"All qualified applicants will receive consideration for employment.*?(?=\n\n|\Z)",
    r"To unsubscribe.*?(?=\n\n|\Z)",
    r"unsubscribe.*?(?=\n\n|\Z)",
    r"(equal opportunity employer|reasonable accommodation|protected veteran|characteristic protected by law).*?(?=\n\n|\Z)",
    r"(confidentiality notice|privileged and confidential information).*?(?=\n\n|\Z)",
    r"(privacy notice|email confidentiality and privacy).*?(?=\n\n|\Z)",
    r"Confidentiality Notice:.*?(?=\n\n|\Z)",
    r"The information contained in this message may be privileged and confidential and protected from disclosure.*?(?=\n\n|\Z)",    
]


def matches_any_pattern(text: str, patterns: list[str]) -> bool:
    return any(re.match(pattern, text, re.IGNORECASE) for pattern in patterns)


def clean_email_body(body: str, trim_thread: bool = False) -> str:
    if not body:
        return ""

    text = html.unescape(body)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    lines = text.split("\n")
    cleaned_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Single-line reply marker
        if matches_any_pattern(stripped, REPLY_MARKER_PATTERNS):
            if trim_thread:
                break
            i += 1
            continue

        # Two-line reply marker:
        # On Monday, March 30, 2026, ...
        # wrote:
        if (
            re.match(r"^On .+$", stripped, re.IGNORECASE)
            and i + 1 < len(lines)
            and re.match(r"^wrote:\s*$", lines[i + 1].strip(), re.IGNORECASE)
        ):
            if trim_thread:
                break
            i += 2
            continue

        # Generic noise/header lines
        if matches_any_pattern(stripped, NOISE_LINE_PATTERNS):
            i += 1
            continue

        cleaned_lines.append(line)
        i += 1

    text = "\n".join(cleaned_lines)

    # Collapse large gaps before block cleanup
    text = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", text)

    # Remove multi-line footer/legal blocks
    for pattern in BLOCK_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)

    # Final spacing cleanup
    text = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", text)

    # Remove lines that do not contain visible character content,
    # and normalize spacing on lines that do.
    lines = text.split("\n")
    cleaned_lines = []
    previous_was_blank = False

    for line in lines:
        # Normalize odd spaces / invisible chars per line
        line = (
            line.replace("\u00A0", " ")
                .replace("\u2007", " ")
                .replace("\u202F", " ")
        )
        line = re.sub(r"[\u200B-\u200D\uFEFF]", "", line)

        # Collapse internal spaces/tabs
        normalized = re.sub(r"[ \t]+", " ", line).strip()

        # Remove leading pipe/table artifacts
        normalized = re.sub(r"^[\|\s]+", "", normalized)

        # Remove lines that are only formatting junk
        # Examples: |, ||, ----, ===, _
        if normalized and re.fullmatch(r"[|_\-=~ ]+", normalized):
            continue

        # Blank or non-visible line: keep at most one blank line
        if not normalized:
            if not previous_was_blank:
                cleaned_lines.append("")
                previous_was_blank = True
            continue

        cleaned_lines.append(normalized)
        previous_was_blank = False

    text = "\n".join(cleaned_lines)

    # Clean bullet indentation
    text = re.sub(r"\n\s*-\s*", "\n- ", text)

    # Final safety pass: at most one blank line between text blocks
    text = re.sub(r"\n(?:\s*\n)+", "\n\n", text)

    return text.strip()