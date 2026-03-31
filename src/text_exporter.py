import os

def save_email_to_text(subject, sender, date, body, output_dir):
    safe_subject = "".join(c for c in subject if c.isalnum() or c in (" ", "_")).strip()
    safe_subject = safe_subject[:80] or "email"

    base_filename = f"{safe_subject}.txt"
    file_path = os.path.join(output_dir, base_filename)

    counter = 1

    while os.path.exists(file_path):
        print(f"[DUPLICATE FILE] {file_path} exists, creating a new filename")
        file_path = os.path.join(output_dir, f"{safe_subject}_{counter}.txt")
        counter += 1

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"Subject: {subject}\n")
        f.write(f"From: {sender}\n")
        f.write(f"Date: {date}\n")
        f.write("\n" + "=" * 50 + "\n\n")
        f.write(body)

    return file_path