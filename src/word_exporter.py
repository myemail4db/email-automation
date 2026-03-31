from docx import Document
import os
from src.text_filter import clean_email_body

def save_email_to_word(subject, sender, date, body, output_dir):
    safe_subject = "".join(c for c in subject if c.isalnum() or c in (" ", "_")).strip()
    safe_subject = safe_subject[:80] or "email"

    base_filename = f"{safe_subject}.docx"
    file_path = os.path.join(output_dir, base_filename)

    counter = 1
    while os.path.exists(file_path):
        print(f"[DUPLICATE FILE] {file_path} exists, creating a new filename")
        file_path = os.path.join(output_dir, f"{safe_subject}_{counter}.docx")
        counter += 1

    cleaned_body = clean_email_body(body)

    doc = Document()
    doc.add_heading(subject, level=1)
    doc.add_paragraph(f"From: {sender}")
    doc.add_paragraph(f"Date: {date}")
    doc.add_paragraph("=" * 50)
    doc.add_paragraph(cleaned_body)

    doc.save(file_path)
    return file_path