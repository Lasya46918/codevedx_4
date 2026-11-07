# Project 4 — AI Chatbot for Internal Helpdesk

## Objective
Provide FAQ-based responses through a simple Flask web application, with an admin-only form for adding FAQs.

## Features
- Web chat interface.
- Intent/category labels for FAQs.
- TF-IDF and cosine-similarity matching.
- Unknown-question fallback.
- Admin FAQ update protected by a password stored in an environment variable.
- JSON FAQ storage.

## Run
```bash
pip install -r ../requirements.txt
```
Set an admin password before starting:
- Windows PowerShell: `$env:HELPDESK_ADMIN_PASSWORD="choose-a-strong-local-password"`
- macOS/Linux: `export HELPDESK_ADMIN_PASSWORD="choose-a-strong-local-password"`

Then run `python app.py` and open `http://127.0.0.1:5000`.

This is a local educational app. Before public deployment, add HTTPS, rate limiting, CSRF protection, secure secret management, and production-grade authentication.
