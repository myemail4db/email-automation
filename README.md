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
    - [Gmail Labels](#gmail-labels)
    - [Local Folders](#local-folders)
    - [Naming](#naming)
    - [Safety Settings](#safety-settings)
  - [Running the Application](#running-the-application)
  - [Workflow](#workflow)
  - [Email Cleaning Logic](#email-cleaning-logic)
  - [Output](#output)
    - [File Format](#file-format)
    - [Example Output](#example-output)
  - [Example Runs](#example-runs)
    - [1. Export Emails to Word](#1-export-emails-to-word)
    - [2. Export Email to Text](#2-export-email-to-text)
  - [3. Testing Error Handling](#3-testing-error-handling)
    - [Test Error Handling with Text Format](#test-error-handling-with-text-format)
    - [Test Error Handling with Word Format](#test-error-handling-with-word-format)
  - [Date Formatting (Cross-Platform)](#date-formatting-cross-platform)
  - [Troubleshooting](#troubleshooting)
    - [Missing module](#missing-module)
    - [Label not found](#label-not-found)
  - [Project Structure](#project-structure)
  - [Future Enhancements](#future-enhancements)
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

### Gmail Labels

```python
"labels": {
    "source": "for_friend",
    "processed_review": "for_friend/processed_review",
    "error": "for_friend/error",
}
```

### Local Folders

```
"local_folders": {
    "input": "input",
    "processed_review": "processed_review",
    "ready_to_send": "ready_to_send",
    "sent_archive": "sent_archive",
    "error": "error",
    "logs": "logs",
}
```

### Naming

```
"naming": {
    "fallback_prefix": "job_email",
    "zip_prefix": "job_batch",
    "max_filename_length": 100,
}
```

### Safety Settings

```
"safety": {
    "test_mode": True,
    "send_emails": False,
    "continue_on_error": True,
}
```

## Running the Application

Run the application from the project root using package mode:

```bash
python3 -m src.run --format text
```

or

```bash
python3 -m src.run --format word
```

This runs the application as a Python package and ensures all `src.*` imports are resolved correctly.

Note:
- Do not use `python3 run.py`
- Do not include `.py` when using `-m`

---

## Workflow

```
Gmail Source Label   Condition   Gmail Destination Label
------------------   ---------   -----------------------
for_friend         → export    → processed_review
for_friend         → failure   → error
```

Emails are read, cleaned (removing headers, disclaimers, and noise), and exported into structured documents.

Additional folders used in extended workflows:

- ready_to_send/ → files prepared for zipping/emailing
- sent_archive/ → files that have already been sent

---

## Email Cleaning Logic

The application processes and cleans email content before export.

Cleaning includes:

- Removing reply chains (e.g., "On ... wrote:")
- Removing email headers (From, Sent, To, Subject)
- Removing known noise lines (mobile signatures, warnings)
- Removing legal disclaimers and unsubscribe blocks
- Removing formatting artifacts (e.g., "|", table fragments)
- Normalizing whitespace and invisible characters
- Ensuring at most one blank line between text blocks

Important:
- All visible text content is preserved
- Only non-visible or noise content is removed

---

## Output

Processed emails are saved locally to:

```bash
processed_review/
```

Error reports are saved to:

```bash
error/
```

### File Format

Each email is exported with the following structure:

```
Subject: <email subject>
From: <sender>
Date: <timestamp>
==================================================
<cleaned email content>
```

The email body is automatically cleaned to improve readability:
- Removes reply wrapper lines (e.g., "On Monday... wrote:")
- Removes Gmail UI noise (e.g., "Using Gmail with screen readers")
- Removes common warning and footer lines
- Preserves the original job description and relevant content

### Example Output

```
============================================================
EMAIL DETAILS
============================================================
Subject           : Fw: Web & Python Developer || San Francisco, CA 94103 || Contract
From              : Dominick Benigno <dominickbenigno@yahoo.com>
Date              : Wednesday, April 01, 2026, 1:57 AM UTC
Workflow Status   : processed_review
Export Format     : text
File Name         : Fw Web  Python Developer  San Francisco CA 94103  Contract.txt
============================================================
Hi,

This is Jane Doe from Company. We are global IT services and workforce solution firm based in Atlanta, Georgia.

I came across your profile on Job Portal and thought you’d be the right fit for position Web & Python Developer we are currently looking to hire in San Francisco, CA 94103. I have the Job description below and would like to discuss further if this interests you

Role: Web & Python Developer

Location: San Francisco, CA 94103

Duration: Contract

Key Responsibilities:
- Design and develop responsive web applications and hybrid mobile apps using modern frameworks (React, Next.js, Angular, Vue, React Native).
- Develop Python-based backend services and RESTful APIs
- Implement scalable and reusable components for web and mobile platforms.
- Utilize AI-assisted coding tools (“vibe coding”) such as GitHub Copilot, ChatGPT, or similar tools to accelerate development workflows.
- Integrate intelligent features such as AI-driven search, automation, analytics, or personalization where applicable.
- Collaborate with stakeholders to gather requirements and translate them into technical solutions.
- Develop wireframes and prototypes using Figma or similar design tools.
- Deploy and manage applications in Microsoft Azure environments, including CI/CD pipelines.
- Troubleshoot and maintain existing applications and support production environments.

Required Qualifications:
- 8+ years of experience developing modern web applications.
- Strong experience with JavaScript / TypeScript frameworks such as React, Next.js, Angular, or Vue.
- 3+ years of Python development experience building APIs or backend services.
- Experience developing cross-platform mobile applications (React Native, Flutter, or similar frameworks).
- Experience working with REST APIs and backend integrations.
- Familiarity with AWS, Azure cloud services, and DevOps pipelines.
- Experience with Git-based development workflows.
- Strong analytical, troubleshooting, and problem-solving skills.
- Ability to collaborate effectively with both technical and non-technical stakeholders.

Preferred Qualifications:
- Experience with Docker and Kubernetes.
- Experience with Salesforce Mobile SDK or Service Cloud integration.
- Experience with MuleSoft or enterprise integration platforms.
- Experience integrating AI services or LLM APIs (OpenAI, Azure OpenAI, etc.).

Jane Doe
Lead Recruiter

P: (123) 456-7890 / 1234

E: jane.doe@company.com
```


## Example Runs

These examples show real execution output of the application in different scenarios.

### 1. Export Emails to Word

In the bash terminal, this is what is seen:

```bash
python3 -m src.run --format word
```

```
Found 2 email(s) under label 'for_friend'
[DUPLICATE FILE] processed_review/Fw Web  Python Developer  San Francisco CA 94103  Contract.docx exists, creating a new filename
Saved: processed_review/Fw Web  Python Developer  San Francisco CA 94103  Contract_1.docx
[SUCCESS] Fw: Web & Python Developer || San Francisco, CA 94103 || Contract → processed_review
[DUPLICATE FILE] processed_review/Fw 100 Remote role Technical Engineer needed.docx exists, creating a new filename
Saved: processed_review/Fw 100 Remote role Technical Engineer needed_1.docx
[SUCCESS] Fw: 100% Remote role! Technical Engineer needed → processed_review

Export Summary:

+------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| Email Status     | Local File                                                                                                                            |
+------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| processed_review | processed_review/Fw Web  Python Developer  San Francisco CA 94103  Contract_1.docx |
| processed_review | processed_review/Fw 100 Remote role Technical Engineer needed_1.docx               |
+------------------+---------------------------------------------------------------------------------------------------------------------------------------+
```

### 2. Export Email to Text

In the bash terminal, this is what is seen:

```bash
python3 -m src.run --format text                     
```

```
Found 2 email(s) under label 'for_friend'
[DUPLICATE FILE] processed_review/Fw Web  Python Developer  San Francisco CA 94103  Contract.txt exists, creating a new filename
Saved: processed_review/Fw Web  Python Developer  San Francisco CA 94103  Contract_1.txt
[SUCCESS] Fw: Web & Python Developer || San Francisco, CA 94103 || Contract → processed_review
[DUPLICATE FILE] processed_review/Fw 100 Remote role Technical Engineer needed.txt exists, creating a new filename
Saved: processed_review/Fw 100 Remote role Technical Engineer needed_1.txt
[SUCCESS] Fw: 100% Remote role! Technical Engineer needed → processed_review

Export Summary:

+------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| Email Status     | Local File                                                                                                                           |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| processed_review | email-automation/processed_review/Fw Web  Python Developer  San Francisco CA 94103  Contract_1.txt |
| processed_review | email-automation/processed_review/Fw 100 Remote role Technical Engineer needed_1.txt               |
+------------------+--------------------------------------------------------------------------------------------------------------------------------------+
```

## 3. Testing Error Handling

To simulate failures and verify error handling behavior:

When test error mode is enabled:
- emails are routed to the Gmail error label
- structured error report files are created in the local `error/` folder
- the export summary displays the generated error report paths

### Test Error Handling with Text Format

In the bash terminal, this is what is seen:

```bash
TEST_ERROR_MODE=true python3 -m src.run --format text
```

```
Found 2 email(s) under label 'for_friend'
Error processing message 19d46c2669b19b6f: Test error - forcing failure path
[ERROR] Error report created: error/Fw Web  Python Developer  San Francisco CA 94103  Contract_ERROR.txt
[ERROR] 19d46c2669b19b6f: Test error - forcing failure path
Error processing message 19d46b78db99b309: Test error - forcing failure path
[ERROR] Error report created: error/Fw 100 Remote role Technical Engineer needed_ERROR.txt
[ERROR] 19d46b78db99b309: Test error - forcing failure path

Export Summary:

+--------------+-------------------------------------------------------------------------------------------------------------------------------+
| Email Status | Local File                                                                                                                    |
+--------------+-------------------------------------------------------------------------------------------------------------------------------+
| Error        | error/Fw Web  Python Developer  San Francisco CA 94103  Contract_ERROR.txt |
| Error        | error/Fw 100 Remote role Technical Engineer needed_ERROR.txt               |
+--------------+-------------------------------------------------------------------------------------------------------------------------------+
```

### Test Error Handling with Word Format

In the bash terminal, this is what is seen:

```bash
TEST_ERROR_MODE=true python3 -m src.run --format word
```

```
Found 2 email(s) under label 'for_friend'
Error processing message 19d46c2669b19b6f: Test error - forcing failure path
[ERROR] Error report created: error/Fw Web  Python Developer  San Francisco CA 94103  Contract_ERROR_1.txt
[ERROR] 19d46c2669b19b6f: Test error - forcing failure path
Error processing message 19d46b78db99b309: Test error - forcing failure path
[ERROR] Error report created: error/Fw 100 Remote role Technical Engineer needed_ERROR_1.txt
[ERROR] 19d46b78db99b309: Test error - forcing failure path

Export Summary:

+--------------+---------------------------------------------------------------------------------------------------------------------------------+
| Email Status | Local File                                                                                                                      |
+--------------+---------------------------------------------------------------------------------------------------------------------------------+
| Error        | error/Fw Web  Python Developer  San Francisco CA 94103  Contract_ERROR_1.txt |
| Error        | error/Fw 100 Remote role Technical Engineer needed_ERROR_1.txt               |
+--------------+---------------------------------------------------------------------------------------------------------------------------------+
```

---

## Date Formatting (Cross-Platform)

The application formats email timestamps into a human-readable format.

Example:
```
Tuesday, March 31, 2026, 10:16 AM PDT
```

If timezone information is available, it will be included (e.g., PDT or UTC offset).

Note:
- macOS/Linux use "%-I" for hour formatting
- Windows uses "%#I"

This is handled automatically in the code using OS detection, so no manual changes are required.

---

## Troubleshooting

### Missing module

```bash
python3 -m pip install -r requirements.txt
```

Authentication issue

```bash
rm -f token.json
python3 -m src.run
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
│   ├── __init__.py
│   ├── run.py
│   ├── processor.py
│   ├── text_exporter.py
│   ├── word_exporter.py
│   ├── text_filter.py
│   ├── gmail_client.py
│   ├── error_handler.py
│   ├── config.py
│   └── utils/
│       ├── __init__.py
│       └── date_utils.py
│       └── error_utils.py
├── processed_review/
├── error/
├── requirements.txt
└── README.md
```

## Future Enhancements

- Zip exported files into batch archives
- Send email notifications with attachments
- Archive processed batches after sending

---

## Author

Dominick Benigno