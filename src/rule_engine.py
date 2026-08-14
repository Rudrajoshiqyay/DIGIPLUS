import pandas as pd
import re

RULES = {
    "Network": ["vpn", "wi-fi", "internet", "disconnects", "network", "offline"],
    "Hardware": ["printer", "zebra", "webcam", "laptop", "mouse", "keyboard", "monitor"],
    "Access": ["password", "login", "locked", "reset", "ad", "active directory", "authentication"],
    "Software": ["outlook", "excel", "saas", "application", "crashing", "software", "business-apps"]
}

def apply_rules(text):
    """
    Scans the input text (summary + description) against predefined keywords.
    Returns a list of matched categories.
    """
    if not isinstance(text, str):
        return []
        
    text_lower = text.lower()
    matched_categories = set()
    
    for category, keywords in RULES.items():
        for keyword in keywords:
            # Word boundary regex to prevent partial matches
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                matched_categories.add(category)
                break 
                
    return list(matched_categories)

if __name__ == "__main__":
    # Test script to verify the rule engine
    try:
        # Assuming script is run from the project root
        df = pd.read_csv("data/raw/tickets.csv")
        print("--- Testing Rule Engine on 5 Sample Tickets ---")
        for idx, row in df.head(5).iterrows():
            text_to_analyze = f"{row['summary']} {row['description']}"
            tags = apply_rules(text_to_analyze)
            print(f"Ticket #{row['ticket_id']} | Tags: {tags} | Summary: {row['summary']}")
    except FileNotFoundError:
        print("Data not found. Please ensure you are running from the project root.")
