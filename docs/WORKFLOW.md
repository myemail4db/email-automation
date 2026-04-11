# Workflow <!-- omit from toc -->

This is the actual flow the tool follows.

You don’t need to run everything at once.
Each step is separate on purpose.

---

## Table of Contents <!-- omit from toc -->

- [Step 0: Authenticate](#step-0-authenticate)
- [Step 1: Export](#step-1-export)
- [Step 2: Review](#step-2-review)
- [Step 3: Send](#step-3-send)

---

## Step 0: Authenticate

```bash
python -m src auth
```

Generates token.json for Gmail access.

---

## Step 1: Export

```bash
python -m src export --format text
```

- Reads emails from source label
- Exports files to processed_review/

--

## Step 2: Review

- Edit files if needed
- Validate content before sending

---

## Step 3: Send

```bash
python -m src send
```

- Creates zip archive
- Sends email
- Moves files to archive