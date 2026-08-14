# Digiplus IT Support AI Copilot

This project is an AI-powered IT Support Copilot that uses **Retrieval-Augmented Generation (RAG)** to assist human engineers. It automatically tags tickets, searches a local database of past incidents, reads company SOPs, and prompts Llama 3 to draft an Investigation Playbook.

## Features
- **Deterministic Rule Engine**: Instantly tags tickets based on keywords to save LLM API costs.
- **Local Vector Database**: Uses ChromaDB to find similar past tickets.
- **Human-in-the-Loop AI**: Uses Groq (Llama 3) to generate actionable playbooks based on company policy, keeping the human engineer in control.

## How to Run Locally

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Add your API Key**:
   Copy the `.env.example` file and rename it to `.env`. Paste your Groq API key inside.
4. **Run the Dashboard**:
   ```bash
   streamlit run src/app.py
   ```

## Deployment (Render Ready)
This repository is pre-configured to be deployed easily on **Render**.
1. Connect this GitHub repo to Render as a "Web Service".
2. Render will automatically detect the `requirements.txt` and install Python dependencies.
3. Set the start command to: `streamlit run src/app.py --server.port $PORT`
4. Add your `GROQ_API_KEY` in the Render Environment Variables dashboard.
