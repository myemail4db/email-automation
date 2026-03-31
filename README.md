# Gmail to Document Automation

A Python-based automation tool that reads labeled emails from Gmail and exports them into structured files (Text or Word).

---

## 📚 Table of Contents

- [Gmail to Document Automation](#gmail-to-document-automation)
  - [📚 Table of Contents](#-table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Cost](#cost)
  - [AI-Assisted Development](#ai-assisted-development)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Create virtual environment](#2-create-virtual-environment)
    - [3. Install dependencies](#3-install-dependencies)
    - [Gmail API Setup (Required)](#gmail-api-setup-required)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Workflow](#workflow)
  - [Output](#output)
  - [Date Formatting (Cross-Platform)](#date-formatting-cross-platform)
  - [Testing Error Handling](#testing-error-handling)
  - [Troubleshooting](#troubleshooting)
    - [Missing module](#missing-module)
    - [Label not found](#label-not-found)
  - [Project Structure](#project-structure)
  - [Author](#author)

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
- Reads emails from a Gmail label  
- Extracts subject, sender, date, and body  
- Exports emails to:
  - `.txt`
  - `.docx`
- Moves processed emails automatically  
- Handles duplicate filenames safely  
- Supports error handling and retry workflows  

---

## Cost

This application uses the Gmail API and is **free to use**.

There are **no charges** for:
- Reading emails  
- Running locally  
- Regular usage  

**Cost = $0**

---

## AI-Assisted Development

This project was developed with the assistance of AI tools, including ChatGPT.

AI was used for:
- Debugging environment issues  
- API integration troubleshooting  
- Improving structure and design  

All final implementation decisions were validated manually.

---

## Prerequisites

- Python 3.10+
- Gmail account
- Google Cloud project

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd email-automation
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

---

### Gmail API Setup (Required)

1. Go to Google Cloud Console

    https://console.cloud.google.com/
    

2. Select or create a project

3. Enable Gmail API

    https://console.cloud.google.com/apis/library/gmail.googleapis.com

4. Configure OAuth Consent Screen
   - Type: External
   - Add yourself as test user

5. Create OAuth Client ID
   - Type: Desktop app

6. Download credentials

    Move to project:

    ```bash
    mv ~/Downloads/client_secret_*.json ./credentials.json
    ```

---

## Configuration

Edit:

```python
src/config.py
```

```python
"labels": {
    "source": "for_friend",
    "processed_review": "for_friend/processed_review",
    "error": "for_friend/error"
}
```

## Usage

Run:

```bash
python3 run.py --format text
```

or

```bash
python3 run.py --format word
```

---

## Workflow

```
Folder in Gmail.   Condition.  to Folder in Gmail
----------------   ---------   ------------------
for_friend       → export    → processed_review
for_friend       → failure   → error
```

---

## Output

Saved to:

```
processed_review/
```

Example:

```
Re New Remote Opportunity.txt
Re New Remote Opportunity_1.txt
Re New Remote Opportunity.docx
```

Duplicate files are automatically renamed.

---

## Date Formatting (Cross-Platform)

The application formats email timestamps into a human-readable format.

Example:
Tuesday, March 31, 2026, 10:16 AM

Note:
- macOS/Linux use "%-I" for hour formatting
- Windows uses "%#I"

This is handled automatically in the code using OS detection, so no manual changes are required.

---

## Testing Error Handling

```bash
TEST_ERROR_MODE=true python3 run.py --format text
```

- Email moves to error label
- File may or may not be saved depending on when error occurs

---

## Troubleshooting

### Missing module

```bash
python3 -m pip install -r requirements.txt
```

Authentication issue

```bash
rm -f token.json
python3 run.py
```

### Label not found

Ensure labels exist:
- for_friend
- for_friend/processed_review
- for_friend/error

---

## Project Structure

```
email-automation/
├── src/
├── processed_review/
├── requirements.txt
├── run.py
└── README.md
```

---

## Author

Dominick Benigno