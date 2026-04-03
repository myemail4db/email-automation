from src.text_filter import clean_email_body
from src.utils.date_utils import format_email_date
from docx import Document
from docx.shared import Pt
from pathlib import Path
import os
from datetime import datetime

def add_separator(doc, char="=", length=60):
    doc.add_paragraph(char * length)


def add_header_field(doc, label, value):
    p = doc.add_paragraph()
    run_label = p.add_run(f"{label:<18}: ")
    run_label.bold = True
    p.add_run(str(value))


def save_email_to_word(subject, sender, date, body, output_dir, status="processed_review", format_type="word"):
    safe_subject = "".join(c for c in subject if c.isalnum() or c in (" ", "_")).strip()
    safe_subject = safe_subject[:80] or "email"

    base_filename = f"{safe_subject}.docx"
    file_path = os.path.join(output_dir, base_filename)

    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(output_dir, f"{safe_subject}_{counter}.docx")
        counter += 1

    file_name = Path(file_path).name
    cleaned_body = clean_email_body(body)

    doc = Document()

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    add_separator(doc)

    title = doc.add_paragraph()
    title_run = title.add_run("EMAIL DETAILS")
    title_run.bold = True
    title_run.font.size = Pt(12)

    add_separator(doc)

    add_header_field(doc, "Subject", subject or "No Subject")
    add_header_field(doc, "From", sender or "Unknown Sender")
    add_header_field(doc, "Date", format_email_date(date))
    add_header_field(doc, "Workflow Status", status)
    add_header_field(doc, "Export Format", format_type)
    add_header_field(doc, "File Name", file_name)

    add_separator(doc)
    doc.add_paragraph()

    for line in cleaned_body.split("\n"):
        doc.add_paragraph(line)

    doc.save(file_path)
    return file_path