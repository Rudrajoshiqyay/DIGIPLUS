import pandas as pd
import os
from datetime import datetime

def ensure_dir(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def save_new_incident(summary, description):
    """Persists a newly submitted ticket to a CSV file."""
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "submitted_tickets.csv")
    ensure_dir(file_path)
    
    new_data = pd.DataFrame([{
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "description": description,
        "status": "open"
    }])
    
    if not os.path.isfile(file_path):
        new_data.to_csv(file_path, index=False)
    else:
        new_data.to_csv(file_path, mode='a', header=False, index=False)

def save_resolution(summary, description, playbook):
    """Persists the resolved ticket and its AI playbook to a CSV file."""
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "resolved_tickets.csv")
    ensure_dir(file_path)
    
    new_data = pd.DataFrame([{
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "description": description,
        "playbook": playbook,
        "status": "resolved"
    }])
    
    if not os.path.isfile(file_path):
        new_data.to_csv(file_path, index=False)
    else:
        new_data.to_csv(file_path, mode='a', header=False, index=False)
