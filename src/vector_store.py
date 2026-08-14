import pandas as pd
import chromadb
import os

# Initialize ChromaDB client (local persistent storage)
db_path = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
client = chromadb.PersistentClient(path=db_path)

def build_vector_store():
    print("Building Vector Store...")
    
    # Try to get collection, create if it doesn't exist
    collection = client.get_or_create_collection(name="tickets")
    
    # Check if we already have items to avoid rebuilding every time
    if collection.count() > 0:
        print(f"Vector Store already built with {collection.count()} tickets.")
        return

    # Load tickets
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "tickets.csv")
    df = pd.read_csv(csv_path)
    
    # Using first 500 tickets for speed in this demo
    df = df.head(500)
    
    documents = []
    metadatas = []
    ids = []
    
    for idx, row in df.iterrows():
        text = f"Summary: {row['summary']} | Description: {row['description']}"
        documents.append(text)
        
        metadatas.append({
            "ticket_id": row["ticket_id"],
            "resolution_status": row["status"],
            "priority": row["priority"]
        })
        
        ids.append(str(row["ticket_id"]))
        
    print(f"Adding {len(documents)} tickets to ChromaDB... this might take a moment.")
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print("Vector Store built successfully!")

def find_similar_tickets(query_text, n_results=3):
    collection = client.get_collection(name="tickets")
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results

if __name__ == "__main__":
    build_vector_store()
