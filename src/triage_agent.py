import os
import sys
from groq import Groq
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.llm_agent import load_knowledge_base

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def chat_with_triage_agent(messages):
    """
    Takes a list of message dicts [{"role": "user/assistant", "content": "..."}]
    and returns the Agent's response.
    """
    kb_content = load_knowledge_base()
    
    system_prompt = f"""
You are the Digiplus IT Triage Agent, the first point of contact for employees facing IT issues.
Your goal is to help them solve basic problems by asking troubleshooting questions based on the [KNOWLEDGE BASE].

[KNOWLEDGE BASE]
{kb_content}

Instructions for Linear Troubleshooting:
You MUST follow this exact 3-step linear process. Do not skip steps. Ask only ONE question at a time.

STEP 1 (Identification): Ask the user to clearly identify their device (e.g., Windows laptop, Mac, Phone) and the specific app/system causing the issue.
STEP 2 (Symptom Check): Once you know the device, ask them for the exact error message or specific symptom they are experiencing.
STEP 3 (Resolution or Escalation): Once you have the device and symptom, consult the [KNOWLEDGE BASE]. 
  - If you find a fix, suggest it. If they confirm it worked, output "[RESOLVED]" and thank them.
  - If you cannot find a fix, or if it requires physical repair/admin rights, you MUST output the "[ESCALATE]" tag.

TO ESCALATE, your output MUST begin with exactly the tag [ESCALATE]. After that tag, you MUST provide a generated Summary and Description of their issue based on your chat history, formatted exactly like this:
[ESCALATE]
Summary: User's laptop won't turn on
Description: The user tried plugging it in, but there are no lights. Suspect hardware failure.
"""
    
    # Prepend the system prompt to the message history
    api_messages = [{"role": "system", "content": system_prompt}] + messages
    
    try:
        completion = client.chat.completions.create(
            model="qwen/qwen3.6-27b",
            messages=api_messages,
            temperature=0.3,
            max_tokens=500,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error communicating with Groq API: {e}"
