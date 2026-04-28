import html
import re

# Patterns to identify reply markers, noise lines, and multi-line blocks to remove from email bodies
REPLY_MARKER_PATTERNS = [
    r"^On .+ wrote:\s*$",
]

# Lines that are common in email replies but don't necessarily indicate the start of a thread
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
    r"^Confidentiality Notice:\s*$",
]

# Multi-line blocks to remove
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

def remove_private_unicode(text: str) -> str:
    return re.sub(r"[\uE000-\uF8FF]", "", text)

def truncate(value, length=200):
    text = repr(value)
    return text[:length] + ("..." if len(text) > length else "")

def debug_log(before, after, reason):
    print("\n--- DEBUG ---")
    print(f"Reason: {reason}")
    print("BEFORE:")
    print(truncate(before))
    print("AFTER:")
    print(truncate(after))
    print("-------------\n")

def clean_email_body(body: str, trim_thread: bool = False) -> str:
    if not body:
        return ""

    text = html.unescape(body)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    text = text.replace("", "")
    text = remove_private_unicode(text)

    lines = text.split("\n")
    cleaned_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Reply marker
        if matches_any_pattern(stripped, REPLY_MARKER_PATTERNS):
            debug_log(line, "", "Removed reply marker")
            if trim_thread:
                break
            i += 1
            continue

        # Two-line reply marker
        if (
            re.match(r"^On .+$", stripped, re.IGNORECASE)
            and i + 1 < len(lines)
            and re.match(r"^wrote:\s*$", lines[i + 1].strip(), re.IGNORECASE)
        ):
            debug_log(line + "\n" + lines[i + 1], "", "Removed two-line reply marker")
            if trim_thread:
                break
            i += 2
            continue

        # Noise line
        if matches_any_pattern(stripped, NOISE_LINE_PATTERNS):
            debug_log(line, "", "Removed noise line")
            i += 1
            continue

        cleaned_lines.append(line)
        i += 1

    text = "\n".join(cleaned_lines)

    # Collapse multiple blank lines
    new_text = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", text)
    if new_text != text:
        debug_log(text, new_text, "Collapsed multiple blank lines")
    text = new_text

    # Remove multi-line blocks
    for pattern in BLOCK_PATTERNS:
        matches = list(re.finditer(pattern, text, flags=re.IGNORECASE | re.DOTALL))
        for m in matches:
            debug_log(m.group(0), "", f"Removed block pattern: {pattern}")

        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)

    # Collapse again
    new_text = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", text)
    if new_text != text:
        debug_log(text, new_text, "Collapsed blank lines after block removal")
    text = new_text

    lines = text.split("\n")
    cleaned_lines = []
    previous_was_blank = False

    for line in lines:
        original_line = line

        # The following replace clauses are all case-sensitive:
        line = (
            line.replace("\u00A0", " ")
                .replace("\u2007", " ")
                .replace("\u202F", " ")
                .replace("If you would like", "")
                .replace("   ", " ")
                .replace("+1", "")
                .replace(" :", ":")
                .replace(" ,", ",")
                .replace(",Iselin", ", Iselin")
                .replace("::", " ")
                .replace("͏­", "")
                .replace(" ", " ")
                .replace("/)", ")")
                .replace("!!", "!")
                .replace("&nbsp;"," ")
                .replace("privacy", "")
                .replace("MIssion", "Mission")
                .replace("(Onsite)","onsite")
                .replace(".ceipalmm.com", "")
                .replace(":-", ":")
                .replace("Job Title","Title")
                .replace("Job Location","Location")
                .replace("Job Type","Type")
                .replace("Skip to content","")
                .replace("United States","")
                .replace("USA","")
                .replace("Full stack","Full Stack")
                .replace("Best Regards", "Best regards")
                .replace("Your Email Title", "")
                .replace("Thanks & Regards", "\nThanks and regards")
                .replace(" in Massachusetts-*", "")
                .replace("intended solely for the addressee", "")
                .replace("Professional References:(Preferably Supervisory", "professional references (preferably supervisory")
        )
        line = re.sub(r"[\u200B-\u200D\uFEFF]", "", line)

        normalized = re.sub(r"[ \t]+", " ", line).strip()
        normalized = re.sub(r"^[\|\s]+", "", normalized)
        if (line != original_line):
            debug_log(original_line, normalized, "Normalized whitespace and unicode chars and leading formatting")

        # Remove formatting junk
        if normalized and re.fullmatch(r"[|_\-=~ ]+", normalized):
            debug_log(original_line, "", "Removed formatting junk line")
            continue

        if not normalized:
            if not previous_was_blank:
                cleaned_lines.append("")
                previous_was_blank = True
            else:
                debug_log(original_line, "", "Removed extra blank line")
            continue

        cleaned_lines.append(normalized)
        previous_was_blank = False

    text = "\n".join(cleaned_lines)

    new_text = re.sub(r"\n\s*-\s*", "\n- ", text)
    if new_text != text:
        debug_log(text, new_text, "Normalized bullet indentation")
    text = new_text

    new_text = re.sub(r"\n(?:\s*\n)+", "\n\n", text)
    if new_text != text:
        debug_log(text, new_text, "Final blank line normalization")
    text = new_text

    return text.strip()
