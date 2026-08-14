import os
import json
from groq import Groq
from dotenv import load_dotenv

# Ensure we can import from src directory
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.rule_engine import apply_rules
from src.vector_store import find_similar_tickets

# Load .env
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Check for API key
api_key = os.environ.get("GROQ_API_KEY")
if not api_key or api_key == "your_api_key_here":
    print("ERROR: Please add a valid GROQ_API_KEY to the .env file!")
    sys.exit(1)

client = Groq(api_key=api_key)

def load_knowledge_base():
    kb_path = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_base.md")
    with open(kb_path, "r", encoding="utf-8") as f:
        return f.read()

def check_cache(summary):
    """Checks the Learning History for an exact match to skip the API call."""
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "resolved_tickets.csv")
    if os.path.exists(csv_path):
        try:
            import pandas as pd
            df = pd.read_csv(csv_path)
            match = df[df['summary'] == summary]
            if not match.empty:
                return match.iloc[-1]['playbook']
        except Exception:
            pass
    return None

def generate_playbook(ticket_summary, ticket_description):
    # 0. Check Cache First!
    cached_playbook = check_cache(ticket_summary)
    if cached_playbook:
        print("Returning cached playbook...")
        return f"**[⚡ CACHED RESOLUTION - NO AI COST]**\n\n{cached_playbook}"

    # 1. Run through Rule Engine
    tags = apply_rules(f"{ticket_summary} {ticket_description}")
    
    # 2. Find Similar Incidents
    try:
        similar_data = find_similar_tickets(f"{ticket_summary} {ticket_description}", n_results=2)
        similar_texts = similar_data["documents"][0] if similar_data["documents"] else []
    except Exception as e:
        print("Warning: Vector store not built yet. Generating without similar incidents.")
        similar_texts = []
        
    # 3. Load Knowledge Base
    kb_content = load_knowledge_base()
    
    # 4. Prompt LLM
    system_prompt = f"""
    You are an expert IT Support Engineer AI. Your job is to analyze incoming tickets and create an "Investigation Playbook" for the human engineer.
    
    [COMPANY KNOWLEDGE BASE]
    {kb_content}
    
    [SIMILAR PAST TICKETS]
    {json.dumps(similar_texts, indent=2)}
    
    Format your response cleanly:
    1. **Predicted Priority**: (e.g. P1, P2, P3, P4)
    2. **Probable Cause**: Brief explanation based on context.
    3. **Investigation Playbook**: 3 clear troubleshooting steps based on the knowledge base and similar tickets.
    4. **Draft Response**: A polite message for the user.
    """
    
    user_prompt = f"Ticket Summary: {ticket_summary}\nTicket Description: {ticket_description}\nAuto-Tags: {tags}"
    
    print("Requesting Playbook from Groq API...")
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":
    # Test Ticket
    test_summary = "VPN keeps disconnecting at the hotel"
    test_desc = "Hi, I am travelling for work and using the hotel wifi. The VPN drops every 10 minutes."
    
    print("--- NEW TICKET RECEIVED ---")
    print(f"Summary: {test_summary}\n")
    
    try:
        playbook = generate_playbook(test_summary, test_desc)
        print("--- LLM INVESTIGATION PLAYBOOK ---")
        print(playbook)
    except Exception as e:
        print(f"Error: {e}")
