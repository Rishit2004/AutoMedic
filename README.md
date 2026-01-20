# AutoMedic - AI Car Diagnostician 🚗🔧

AutoMedic is an intelligent agent that helps you diagnose car issues by analyzing symptoms. Built with **Pydantic AI**, **FastAPI**, and **Vue.js**.

## Features
- 🗣️ **Natural Language Intake**: Describe problems in plain English.
- 🧠 **Structured Diagnosis**: Returns confidence scores, severity ratings, and DIY feasibility.
- 🎨 **Modern Dashboard**: Dark-mode automotive aesthetic.

## Setup

1.  **Install Dependencies**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r backend/requirements.txt
    ```

2.  **Environment Variables**:
    - Rename `.env.example` (or create `.env`)
    - Add your `OPENAI_API_KEY=...`

3.  **Run Locally**:
    ```bash
    # Run the server from the root directory
    uvicorn backend.main:app --reload
    ```

4.  **Usage**:
    - Open `http://localhost:8000/static/index.html`
    - Enter car details and symptoms.
    - View the diagnostic report.

## Tech Stack
- **Backend**: Python 3.x, FastAPI, Pydantic AI
- **Frontend**: HTML5, TailwindCSS, Vue.js (CDN)
- **AI Model**: GPT-4o (or compatible) via OpenAI/OpenRouter
