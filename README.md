# Gemini Chatbot

A simple Streamlit chat app that sends prompts to Google's Gemini API and keeps
conversation history for the current Streamlit session.

## Requirements

- Python 3.10 or later
- A Google Gemini API key

## Setup

Create and activate a virtual environment from the project directory:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
venv\Scripts\Activate.ps1
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

Set your API key as an environment variable named `GEMINI_API_KEY`. You can
also create a `.env` file in the project directory:

```text
GEMINI_API_KEY=your_api_key_here
```

Keep your API key private. Do not commit the `.env` file or share it publicly.

## Run the app

With the virtual environment activated, run:

```bash
streamlit run app.py
```

Streamlit opens the app in your browser. Enter a message in the chat box and
press Enter or click the send button.

## Files

- `app.py` — Streamlit chat interface and Gemini API integration.
- `basic_code.py` — Command-line example of sending prompts to Gemini.
- `requirements.txt` — Python package dependencies.
