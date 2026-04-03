# Email Automation Tool

A command-line batch processing pipeline that transforms Gmail messages into structured, traceable outputs.

## Problem → Solution

### The Problem

Processing job-related emails manually is inefficient, inconsistent, and difficult to track at scale.

In a typical workflow:
- Emails are reviewed one by one
- Content is manually copied and saved
- File naming is inconsistent
- Errors (missed emails, duplicates, failed saves) go unnoticed
- There is no reliable way to track what was processed or when

As volume increases, the process becomes slower, more error-prone, and harder to audit.

There is no clear answer to:
> “What happened during this batch of work?”

---

### The Impact

Without structure:
- Important emails can be skipped or duplicated
- File organization becomes inconsistent
- Troubleshooting requires manual investigation
- Re-running the process introduces more risk
- There is no audit trail or accountability

---

### The Solution

This project replaces the manual workflow with a structured, batch-based automation pipeline.

It introduces:

- Controlled input using Gmail labels
- Consistent file export (text or Word)
- Batch-based execution with unique batch IDs
- Structured, human-readable logging
- Per-item tracking for success and failure
- Error isolation and recovery handling

---

### Why This Matters

This project transforms the workflow from:

**Manual and unreliable**
- no tracking
- inconsistent output
- difficult to debug

to:

**Automated and traceable**
- repeatable execution
- consistent results
- full visibility into each run

---

### Design Principle

This project was built around one core question:

> “What happened during this run, and can I trust the result?”

Every design decision supports that:
- Batch IDs → traceability  
- Structured logs → readability  
- Run boundaries → clarity  
- Error categories → faster diagnosis  
- Controlled logging → signal over noise  

---

## Who This Is For

This tool is designed for users who:

- Process large volumes of structured emails (e.g., job opportunities, alerts, notifications)
- Need consistent, repeatable output
- Want visibility into what succeeded and failed during a run
- Prefer automation over manual copy/paste workflows
- Need a lightweight, local solution without external dependencies

---

## When to Use This

Use this tool when:
- Email processing is repetitive and time-consuming
- You need consistent formatting of extracted content
- You want a clear audit trail of each batch

Do not use this tool when:
- You only process a few emails occasionally
- You do not need structured output or tracking
- You prefer manual review without automation

---

## 📚 Table of Contents

## Contents

- [Problem → Solution](#problem--solution)
- [System Flow](#system-flow)
- [System Overview](#system-overview)
- [Quick Start](#quick-start)
- [Core Features](#core-features)
- [Setup](#setup)
- [Workflow](#workflow)
- Logging & Output
- [Operational Impact](#operational-impact)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)


--- 

## System Overview

This is a command-line batch processing tool.

It reads emails from Gmail labels, transforms them into structured local files, and tracks execution through structured logging.

There is no user interface. All interaction happens through:
- command-line execution
- local file output
- log inspection

---

## Output Model

This application does not provide a graphical interface.

All output is generated as:

- Local files (exported emails)
- Structured logs (batch execution tracking)

### File Output

Processed emails are saved to:

- `processed_review/` → successfully exported emails  
- `error/` → failed exports and error reports  

### Log Output

Each run generates structured log entries that include:

- batch ID
- processing stage (export/send)
- success/failure status
- error details (if applicable)

Logs are designed to answer:

> “What happened during this run?”

---

## System Flow

```
Gmail → Export → Review → Zip → Send → Archive → Logs
```

This represents the full lifecycle of a batch run.

Each stage is tracked and logged for traceability.

---

## Quick Start

This is a command-line workflow. Results are written to local folders and logs, not displayed in a UI.

1. Run Part 1 to export emails:

```
python -m src.run --format text
```

2. Review and edit files in `processed_review/`

3. Run Part 2 to send batch:

```
python -m src.send_batch
```

---

## Core Capabilities

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

- Python 3.10–3.12 recommended
- Gmail account
- Google Cloud project

**Note:**
Python 3.14 may cause compatibility issues with Google authentication and cryptography dependencies.

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd email-automation
```

---

### 2. Create virtual environment

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows (Command Prompt)

```bash 
python -m venv .venv
.venv\Scripts\activate
```

#### Windows (PowerShell)

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

#### macOS / Linux

```bash
python3 -m pip install -r requirements.txt
```

#### Windows

```bash
python -m pip install -r requirements.txt
```

---

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

### Part 0: Authenticate Gmail (Generate token.json)

Before running the application, you must authenticate with Gmail once to generate a `token.json` file.

This file stores OAuth credentials and allows the application to access Gmail without prompting for login each time.

---

#### Run the authentication step

##### macOS / Linux

```bash
python3 -m src.auth_gmail
```

##### Windows

```bash
python -m src.auth_gmail
```

---

#### What happens during authentication

1. A browser window will open
2. You will be prompted to choose your Google account
3. Google may show a warning:

```
Google hasn’t verified this app
```

4. Click:

- Advanced
- Go to <your app name> (unsafe)

5. Click Continue to grant permissions
6. After successful authentication, you will see:

```
The authentication flow has completed. You may close this window.
```

7. A file named token.json will be created in the project root

---

#### Required Permissions

The application requests the following Gmail API permissions:

- Read and modify emails
  https://www.googleapis.com/auth/gmail.modify

- Send emails
  https://www.googleapis.com/auth/gmail.send

---

#### When to regenerate token.json

Delete and recreate the token if:
- You change Gmail API scopes
- You switch Google accounts
- You encounter authentication errors

##### macOS / Linux

```
rm -f token.json
```

##### Windows

```
del token.json
```

Then rerun the authentication step.

---

#### Notes
- token.json is created automatically after authentication
- Do not commit token.json to version control
- Add it to .gitignore:

```bash
echo "token.json" >> .gitignore
```

---

---

### Gmail API Send Permissions

If email sending fails due to insufficient permissions:

- Ensure the Gmail API scope includes:
  https://www.googleapis.com/auth/gmail.send

- Delete the existing token file and re-authenticate:

#### macOS / Linux
```bash
rm -f token.json
python3 -m src.run
```

#### Windows

```bash
del token.json
python -m src.run
```

This prevents a very common failure.

---

## Part 1: Running the Application to convert emails to local word or text documents

Run the application from the project root:

#### macOS / Linux

```bash
python3 -m src.run --format text
```

or

```bash
python3 -m src.run --format word
```

#### Windows

```
python -m src.run --format text
```

or

```
python -m src.run --format word
```

**Notes**
- Do not use python run.py
- Do not include .py when using -m

## Part 2: Running the Application to zip files and send emails

After reviewing and editing exported files, run the batch process:

### macOS / Linux

```bash
python3 -m src.send_batch
```

### Windows

```bash
python -m src.send_batch
```

This will:
- Create a zip archive from files in processed_review/
- Save the zip to ready_to_send/
- Send the zip via Gmail API
- Move processed files to sent_archive/

```markdown
### Dry Run Mode

The application supports a safe testing mode.

When enabled:

- Emails are not sent
- Files are not archived
- The process simulates execution

Controlled via `.env`:

```bash
SEND_EMAILS=False
TEST_MODE=True
```

To enable real sending:

```
SEND_EMAILS=True
TEST_MODE=False
```

This makes your tool safe to use immediately

---

## Environment Variables

This application uses a `.env` file to store configuration values such as email settings and Google API credentials.

---

### Create a `.env` file

#### macOS / Linux

```bash
touch .env
```

#### Windows (File Explorer)

1. Open the project folder in File Explorer
2. Right-click → New → Text Document
3. Rename the file to:

```bash
.env
```

4. If prompted about changing the file extension, click **Yes**.

**Important (Windows Only)**

If you do not see file extensions:
1. In File Explorer, click **View**
2. Enable File name extensions
3. Then rename the file to `.env`
Otherwise, you may accidentally create:

```
.env.txt    (This is incorrect)
```

Instead of:

```
.env        (This is correct)
```

---

**Why this matters**

This tiny detail prevents one of the most common issues:

> “Why isn’t my `.env` being loaded?”

Because Windows quietly created:

```
.env.txt
```

…and your app is looking for:

```
.env
```

Invisible bug. Very common. Very annoying.

---

#### Mental model about OAth

Think:

```
credentials.json → OAuth authorization → token.json → reuse
```

That’s exactly how OAuth works.

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

---

## Workflow

The application follows a two-step workflow with a manual review stage in between.

---

### Step 0: Authenticate Gmail

```
credentials.json → OAuth authorization → token.json
```

Now your workflow becomes:

Step 0 → Authenticate
Step 1 → Export
Step 2 → Zip + Send
That’s a complete lifecycle.

---

### Step 1: Export Emails

```text
Gmail → processed_review/
```

- Emails are read from the configured Gmail label
- Content is cleaned and structured
- Files are exported to the local `processed_review/` directory
At this stage, files are ready for manual review and editing.

Gmail emails are moved to respective Gmail labels accordingly:

```
Gmail Source Label   Condition                             Gmail Destination Label
------------------   ----------------------------------    -----------------------
for_friend         → read and exported into local files  → processed_review
for_friend         → any errors                          → error
```

Local files are saved accordingly:

```
Local folder         Description
-----------------    ------------------------------------------------
processed_review/    email has been exported and ready to be reviewed
error/               email could not be exported locally
```


Emails are read, cleaned (removing headers, disclaimers, and noise), and exported into structured documents.

---

### Manual Review

Users can:
- Open and edit exported files
- Rename files if needed
- Remove or adjust content
- Prepare final versions before sending
This step ensures quality and accuracy before distribution.

### Step 2: Zip and Send Batch

- All files in `processed_review/` are packaged into a zip archive
- A zip archive is created in `ready_to_send/`
- The zip file is sent via Gmail API
- After successful sending, files are moved to `sent_archive/`

Local files are saved accoredingly:
```
Local folder         Description
--------------    -----------------------------------
ready_to_send/    files prepared for zipping/emailing
sent_archive/     files that have already been sent
```

### Notes
- If email sending fails, files remain in `processed_review/`
- Emails are sent first before moving to `sent_archive/`
- Dry run mode allows testing without sending emails or archiving files
- This separation provides a safe and controlled workflow

---

### High-Level Flow

```
Gmail → Export → Manual Review → Zip → Send → Archive
```

## Status

- Gmail Integration  
- Text Export  
- Word Export  
- Zip Packaging
- Email Sending (In Progress)

---

## Internal Processing Flow

The application is structured as a modular pipeline:

- gmail_client.py → retrieves labeled emails
- text_filter.py → cleans email content
- processor.py → orchestrates processing
- exporters:
  - text_exporter.py → writes .txt files
  - word_exporter.py → writes .docx files
- error_handler.py → handles failures and reporting

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

## Logging & Output

This application uses structured, batch-based logging to track every execution.

Each run generates a unique batch ID that is included in all log entries.

### Log Design

Logs are designed to be:
- human-readable
- easy to search
- consistent across all stages

Each log entry includes:
- Timestamp (Local)
- Batch ID
- Processing stage (export / send)
- Status (SUCCESS, SENT, ERROR)
- Subject or filename
- Error category and message (if applicable)

---

### Run-Level Logging

Each batch is clearly defined with a start and end block:

```
============================================================
[RUN START][job_batch_20260403_211500] export
Timestamp (Local): 2026-04-03 21:15:00
Total Items : 2
```

```
============================================================
[RUN END][job_batch_20260403_211500] export
Timestamp (Local): 2026-04-03 21:15:09
Processed : 2
Success : 1
Failed : 1
```

---

### Per-Item Logging

Each item is tracked individually:

```
[SUCCESS][job_batch_20260403_211500] export (1/2)
Timestamp (Local): 2026-04-03 21:15:05
Subject : Fw: Java Developer
Filename : Fw Java Developer.docx
Processing Stage : export
Result : exported to processed_review
```

---

### Error Logging

Failures include structured error details:

```
[ERROR][job_batch_20260403_211500] export (2/2)
Timestamp (Local): 2026-04-03 21:15:08
Subject : Fw: Python Developer
Filename : error_report_123.txt
Processing Stage : export
Result : failed
Error Category : unexpected_error
Error Message : Test error - forcing failure path
```

---

### Why This Matters

The logging system ensures that:

- every batch is traceable using a single ID
- successes and failures are clearly separated
- debugging does not require digging through raw output
- the system can be trusted to run repeatedly without ambiguity

It directly supports the core design goal:

> “What happened during this run?”

---

## Operational Impact

This tool reduces manual effort and introduces consistency into a repetitive workflow.

Key improvements:
- eliminates manual email handling
- ensures consistent file output
- provides full traceability per batch
- isolates failures without stopping execution
- enables fast debugging using structured logs

---

## File Output

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

### 3. Testing Error Handling

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

Note:
All folders are relative to the project root directory.

Example (macOS/Linux):
/Users/<your-user>/Projects/email-automation/processed_review/

### pip not working inside virtual environment

If you see:

No module named pip.__main__

Fix:

```bash
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
```

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

## Final Note

This project is designed to make a simple question easy to answer:

“What happened during this run?”

And to answer it with clarity, consistency, and confidence.

---

## Author

Dominick Benigno