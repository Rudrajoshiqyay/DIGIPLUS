import os
import pandas as pd
from datasets import load_dataset

def download_and_clean_data(save_dir="data/raw"):
    """
    Downloads the mindweave/help-desk-tickets dataset, 
    cleans it, and saves it locally.
    """
    print("Loading dataset from Hugging Face...")
    # Load the tickets split
    dataset = load_dataset("mindweave/help-desk-tickets", name="tickets", split="train")
    
    # Convert to Pandas DataFrame
    df = dataset.to_pandas()
    print(f"Original shape: {df.shape}")
    
    # Basic cleaning: drop rows where all elements are null
    df = df.dropna(how='all')
    print(f"Shape after dropping entirely null rows: {df.shape}")
    
    # Ensure directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Save to CSV
    output_path = os.path.join(save_dir, "tickets.csv")
    df.to_csv(output_path, index=False)
    print(f"Data successfully saved to {output_path}")

if __name__ == "__main__":
    download_and_clean_data()
