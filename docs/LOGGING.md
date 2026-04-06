# Logging <!-- omit from toc -->

## Table of Contents <!-- omit from toc -->

- [Overview](#overview)
- [Run Structure](#run-structure)
- [Item Tracking](#item-tracking)
- [Error Handling](#error-handling)

---

## Overview

Each run is tracked using a unique batch ID.

Logs are designed to answer:

"What happened during this run?"

---

## Run Structure

Each batch includes:

- Run start  
- Per-item logs  
- Run end summary  

---

## Item Tracking

Each item records:

- status (SUCCESS / ERROR / SENT)  
- subject or filename  
- processing stage  
- timestamp  

---

## Error Handling

Errors are:

- logged with category  
- isolated from successful items  
- stored for review  

Processing continues when possible.