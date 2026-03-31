from docx import Document
import os

def save_email_to_word(subject, sender, date, body, output_dir):
    safe_subject = "".join(c for c in subject if c.isalnum() or c in (" ", "_")).rstrip()
    safe_subject = safe_subject[:80] or "email"

    filename = f"{safe_subject}.docx"
    file_path = os.path.join(output_dir, filename)

    counter = 1

    while os.path.exists(file_path):
        print(f"[DUPLICATE FILE] {file_path} exists, creating a new filename")
        file_path = os.path.join(output_dir, f"{safe_subject}_{counter}.docx")
        counter += 1

    doc = Document()
    doc.add_heading(subject, level=1)
    doc.add_paragraph(f"From: {sender}")
    doc.add_paragraph(f"Date: {date}")
    doc.add_paragraph("\n" + "=" * 50 + "\n")
    doc.add_paragraph(body)

    doc.save(file_path)

    return file_path