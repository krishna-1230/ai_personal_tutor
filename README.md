# Multi-Modal Personal Tutor (Gemini, Streamlit)

A real AI tutor that accepts math/physics questions as images or PDFs, understands them using Gemini, and provides answers. Keeps a Q&A history for your session.

## Features
- Upload images or PDFs of questions
- Ask follow-up questions in text
- Uses Gemini (Google) for OCR and LLM
- Session Q&A history
- Streamlit UI with two pages

## Setup

1. **Clone the repo and enter the directory**
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set your Gemini API key:**
   - Create a `.streamlit/secrets.toml` file:
     ```toml
     GEMINI_API_KEY = "your-gemini-api-key"
     ```

## Run the App
```bash
streamlit run app.py
```

## Usage
- Go to "Ask Tutor" to upload a question or type one.
- View your session's Q&A in "Session History".

---
**Note:**
- No audio input/output in this version.
- No authentication (personal/local use). "# ai_personal_tutor" 
