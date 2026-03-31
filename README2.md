# Gmail to Document Automation

A Python-based automation tool that reads labeled emails from Gmail and exports them into structured documents (Text or Word).

---

## 📚 Table of Contents

- [Gmail to Document Automation](#gmail-to-document-automation)
  - [📚 Table of Contents](#-table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Cost](#cost)
    - [Important Notes:](#important-notes)
    - [Summary:](#summary)
  - [AI-Assisted Development](#ai-assisted-development)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Create and activate virtual environment](#2-create-and-activate-virtual-environment)
    - [3. Install dependencies](#3-install-dependencies)
    - [4. Add credentials](#4-add-credentials)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Change Output Format](#change-output-format)
- [Output](#output)
  - [Workflow](#workflow)
  - [Troubleshooting](#troubleshooting)
    - [Module not found](#module-not-found)
    - [Gmail API 403 error](#gmail-api-403-error)
    - [Authentication issues](#authentication-issues)
  - [Testing Error Handling](#testing-error-handling)
  - [Why this is the right next step](#why-this-is-the-right-next-step)
  - [One important improvement (high-value)](#one-important-improvement-high-value)
- [then save file](#then-save-file)
  - [Project Structure](#project-structure)

---

## Overview

This application connects to Gmail using the Gmail API, retrieves emails from a specific label, and exports them into structured files for review.

Designed for:
- Job tracking
- Email organization
- Automation workflows

---

## Features

- Connects to Gmail via OAuth authentication  
- Filters emails by label  
- Parses email content (subject, sender, date, body)  
- Exports emails to:
  - `.txt` (plain text)
  - `.docx` (Word document)  
- Configurable labels and output directories  
- Modular design (processor + exporters)  

---

## Cost

This application uses the Gmail API and is **free to use** for normal personal usage.

There are **no charges** for:
- Reading emails  
- Listing labels  
- Running the script locally  
- Weekly or daily usage  

### Important Notes:

- You must enable the Gmail API in your Google Cloud project (free)
- You must authenticate using your Google account (free)
- No billing is required unless you use additional Google Cloud services

### Summary:

Cost = **$0**

---

## AI-Assisted Development

This project was developed with the assistance of AI tools, including ChatGPT, as part of an iterative development process.

AI was used to:
- Troubleshoot environment and dependency issues  
- Assist with debugging API integration  
- Explore design patterns and improve code structure  
- Refine documentation and usability  

All implementation, testing, and final design decisions were reviewed and validated to ensure correctness and maintainability.

---

## Prerequisites

- Python 3.x (recommended: 3.11+)
- Gmail account
- Google Cloud project with Gmail API enabled

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd email-automation
```

### 2. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 4. Add credentials

- Download `credentials.json` from Google Cloud Console
- Place it in the project root directory
- Run authentication flow to generate `token.json`

---

## Configuration

Edit `src/config.py`:

```bash
"labels": {
    "source": "for_friend",
    "processed_review": "for_friend/processed_review",
    "error": "for_friend/error"
}
```

Ensure these labels exist in your Gmail account.

---

## Usage

Run the application:

```bash
python3 run.py
```

## Change Output Format
In `run.py`:

```bash
EXPORT_FORMAT = "text"   # or "word"

export_labeled_emails(format_type=EXPORT_FORMAT)
```

---

# Output

Processed emails are saved to:

```bash
jobs_to_review/
```

Example files:
- `Re New Remote Opportunity.txt`
- `Re New Remote Opportunity.docx`

---

## Workflow

Gmail Label → Fetch Emails → Parse → Export → Move to Processed / Error

## Troubleshooting

### Module not found

```bash
python3 -m pip install -r requirements.txt
```

### Gmail API 403 error
- Enable Gmail API in Google Cloud Console

### Authentication issues

```bash
rm -f token.json
python3 run.py
```

## Testing Error Handling

To test the error workflow intentionally:

```bash
TEST_ERROR_MODE=true python3 run.py
```

This forces the script to send matching emails to the error label instead of the processed label.
Turn off test mode for normal use.

## Why this is the right next step

It gives you:
- a safe troubleshooting method
- no need to edit code every time
- documented behavior for your friend

After that, the next move is:
**freeze dependencies with `python3 -m pip freeze > requirements.txt`**

---

## One important improvement (high-value)

Right now your forced error happens **after saving the file**, so you get:

- file saved
- email marked as error

That’s confusing.

Move the test error **before export**:

```python
if TEST_ERROR_MODE:
    raise Exception("Test error - forcing failure path")
```

# then save file

Now behavior is consistent:
- no file saved
- email goes to error

---

## Project Structure

```
email-automation/
│
├── src/
│   ├── processor.py
│   ├── gmail_client.py
│   ├── text_exporter.py
│   ├── word_exporter.py
│   └── config.py
│
├── jobs_to_review/
├── requirements.txt
├── run.py
└── README.md
```
