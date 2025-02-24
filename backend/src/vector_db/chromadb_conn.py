import chromadb
import os

# Define the path where ChromaDB should persist data
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../db/chromadb"))
os.makedirs(DB_PATH, exist_ok=True)  # Ensure the directory exists

def get_client():
    """
    Returns a singleton instance of the ChromaDB PersistentClient.
    Ensures all modules use the same ChromaDB instance.
    """
    return chromadb.PersistentClient(path=DB_PATH)

# Initialize ChromaDB client
chroma_client = get_client()

# Get or create the medicine collection
medicine_collection = chroma_client.get_or_create_collection(name="medicines")
