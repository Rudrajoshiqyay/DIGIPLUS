# Digiplus IT Support AI Copilot

This project is an AI-powered IT Support Copilot that uses **Retrieval-Augmented Generation (RAG)** to assist human engineers. It automatically tags tickets, searches a local database of past incidents, reads company SOPs, and prompts Llama 3 to draft an Investigation Playbook. 🧑‍💻🤖

## Features
- **Conversational Triage Agent**: A Level-1 Support chatbot that attempts to solve basic employee issues before autonomously escalating complex tickets.
- **Deterministic Rule Engine**: Instantly tags tickets based on keywords to save LLM API costs.
- **Local Vector Database**: Uses ChromaDB to find similar past tickets.
- **Human-in-the-Loop AI**: Uses Groq (Llama 3) to generate actionable playbooks based on company policy, keeping the human engineer in control.
- **Semantic Caching**: ⚡ Bypasses the LLM entirely if the exact same ticket has been solved before, saving tokens and time!
- **Analytics Dashboard**: 📊 Visualizes ticket volume and resolution history.

## Setup & Run Instructions
1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Dashboard**:
   ```bash
   streamlit run src/app.py
   ```

## AI Configuration
- **Model**: `llama-3.1-8b-instant` via Groq.
- **Data Flow**: Ticket ➡️ Rule Engine ➡️ Vector Store (ChromaDB) ➡️ Prompt Injection ➡️ Llama 3 ➡️ Output.
- **Vector Store**: ChromaDB (with SentenceTransformers embeddings).

## Explanation of Approach
Instead of building a fully autonomous Multi-Agent system (which carries high security risks and latency in Enterprise IT), I chose a **Human-in-the-Loop RAG Copilot**. The AI does the heavy lifting of researching the Knowledge Base and past incidents, but the final execution is left to the human engineer. 

## Assumptions
- The `tickets.csv` dataset accurately represents incoming support requests.
- The company prefers human oversight for critical IT infrastructure changes.

## Known Limitations
- **Vector Search Accuracy**: Semantic search isn't perfect; occasionally it may pull a loosely related ticket if keywords overlap significantly.
- **Context Limits**: If the Knowledge Base grows too large, we would need to implement a chunking strategy to avoid exceeding the LLM's token limit.
- **Lack of Autonomy**: The AI cannot *execute* the fixes (e.g., it cannot reset a password itself), it only advises the engineer.

## Deployment (Render Ready)
This repository is pre-configured to be deployed easily on **Render**.
1. Connect this GitHub repo to Render as a "Web Service".
2. Set the start command to: `streamlit run src/app.py --server.port $PORT`
3. Add your `GROQ_API_KEY` in the Render Environment Variables dashboard.
