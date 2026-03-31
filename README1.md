# Email Automation Pipeline

## Problem

Manually copying, cleaning, organizing, and sharing recruiter emails is time-consuming and often delayed. This leads to missed or stale opportunities and reduces the likelihood of timely responses.

Recruiters frequently encourage sharing roles with interested candidates, but the manual effort required creates friction and slows down the ability to act on those opportunities.

---

## Solution

This project introduces a human-in-the-loop automation pipeline that:

- Extracts emails from Gmail
- Cleans and normalizes content
- Generates structured local files
- Enables quick manual review and editing
- Packages and sends approved emails efficiently

---

## Key Benefit

This approach reduces manual effort while preserving human control, enabling faster turnaround on time-sensitive opportunities without sacrificing quality.

---

## Workflow

1. Emails are labeled in Gmail under `for_friend`
2. Script 1 processes emails into local files (`jobs_to_review`)
3. Files are reviewed and edited manually
4. Approved files are moved to `jobs_ready_to_send`
5. Script 2 zips and emails them
6. Emails are marked as `for_friend/emailed_jobs`

---

## Project Structure

```
email-automation/
├── credentials.json # OAuth credentials (from Google Cloud)
├── token.json # Generated after authentication
├── auth.py # Generates token.json
├── run.py # Main processing script
├── src/
├── jobs_to_review/
└── logs/
```

---

## Gmail API Setup (Required)

This application uses the Gmail API and requires OAuth credentials.

---

### 1. Open Google Cloud Console

Go to:

https://console.cloud.google.com/

---

### 2. Select a Google Cloud Project

At the top of the page, select your project.

Example:

`Item Catalog App`

If needed, create a new one.

---

### 3. Enable Gmail API

Go to:

https://console.cloud.google.com/apis/library/gmail.googleapis.com

Click:

```
Enable
```


---

### 4. Configure OAuth Consent Screen

Go to:

https://console.cloud.google.com/apis/credentials/consent

- Choose: **External**
- App name: `email-automation`
- User support email: *your Gmail*
- Developer contact email: *your Gmail*

Click through:

```
Save → Continue → Continue → Done
```


Then:

Add your email as a **Test User**

---

### 5. Create OAuth Client ID

Go to:

https://console.cloud.google.com/apis/credentials

Click:

```
CREATE CREDENTIALS → OAuth client ID
```

Select:

```
Application type: Desktop app
```

Name:

```
email-automation-client
```

Click:

```
Create
```


---

### 6. Download and Configure `credentials.json`

Click:

```
Download JSON
```


Move it into your project root:

```bash
mv ~/Downloads/client_secret_*.json ./credentials.json
```

#### Important

Do NOT use placeholder values like:

```bash
client_id: 1234567890-abc123xyz
client_secret: YOUR_CLIENT_SECRET
```

This will cause:

```bash
Error 401: invalid_client
```

You must use the real file downloaded from Google Cloud.

### 7. Generate token.json

Run:

```bash
python auth.py
```

This will:

- Open a browser
- Prompt you to log in
- Ask for Gmail permissions
- Generate:

```bash
token.json
```

### 8. Run the Application

```bash
python run.py
```

## Important Notes

- `credentials.json` → identifies your application
- `token.json` → stores your authenticated session

If authentication breaks:

```bash
rm token.json
python auth.py
```

## Troubleshooting

### Error: `invalid_client`

**Cause:**

- Using placeholder or incorrect `credentials.json`

**Fix:**

- Download a real OAuth client from Google Cloud

### Error: `JSONDecodeError`

**Cause:**

- Corrupted or empty `token.json`

**Fix:**

```bash
rm token.json
python auth.py
```

### Error: `Label not found`

Ensure these Gmail labels exist:

- `for_friend`
- `for_friend/processed_review`
- `for_friend/error`

### Python Warnings (3.9 / LibreSSL)

These warnings are safe to ignore for now.

Upgrade to Python 3.10+ later for long-term support.

# Summary

This project demonstrates:

- Gmail API integration (OAuth 2.0)
- Email parsing and processing
- File generation (Word documents)
- Automation pipeline design

# Author

Dominick Benigno