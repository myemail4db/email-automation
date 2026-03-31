import html
import re


def clean_email_body(body: str) -> str:
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

        # --- CASE 1: Single-line reply marker ---
        if re.match(r"^On .+ wrote:\s*$", stripped, re.IGNORECASE):
            i += 1
            continue

        # --- CASE 2: Two-line reply marker ---
        if (
            re.match(r"^On .+$", stripped, re.IGNORECASE)
            and i + 1 < len(lines)
            and re.match(r"^wrote:\s*$", lines[i + 1].strip(), re.IGNORECASE)
        ):
            i += 2
            continue

        # --- Existing filters ---
        if re.match(r"^Sent from Yahoo Mail.*$", stripped, re.IGNORECASE):
            i += 1
            continue
        if re.match(r"^Get Outlook for .*?$", stripped, re.IGNORECASE):
            i += 1
            continue
        if re.match(r"^CAUTION:.*$", stripped, re.IGNORECASE):
            i += 1
            continue
        if re.match(r"^WARNING:.*$", stripped, re.IGNORECASE):
            i += 1
            continue

        cleaned_lines.append(line)
        i += 1

    text = "\n".join(cleaned_lines)

    # Remove extra blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # --- Remove Collabera-style confidentiality blocks ---
    text = re.sub(
        r"CONFIDENTIALITY NOTICE:.*?(?=\n\n|\Z)",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    # --- Remove feedback + privacy footer spam ---
    text = re.sub(
        r"How am I doing\?.*?(?=\n\n|\Z)",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    # --- Remove repeated CCPA / privacy notice clutter ---
    text = re.sub(
        r"(C)*P?A Privacy Notice.*?(?=\n\n|\Z)",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    # --- Clean up extra spacing again after removals ---
    text = re.sub(r"\n{3,}", "\n\n", text)

    # --- Remove CyberCoders / Equal Opportunity employment block ---
    text = re.sub(
        r"All qualified applicants will receive consideration for employment.*?(?=\n\n|\Z)",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    return text.strip()