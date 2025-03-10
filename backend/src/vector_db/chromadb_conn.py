import chromadb
import os
from chromadb.utils import embedding_functions
from .mock_medicine_data import MOCK_MEDICINES

# Define the path where ChromaDB should persist data
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../db/chromadb"))
os.makedirs(DB_PATH, exist_ok=True)  # Ensure the directory exists

# Sentence Transformer Embedding Function
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"  # Or your preferred model
)

def get_client():
    """
    Returns a singleton instance of the ChromaDB PersistentClient.
    Ensures all modules use the same ChromaDB instance.
    """
    return chromadb.PersistentClient(path=DB_PATH)

# Initialize ChromaDB client
chroma_client = get_client()

# Get or create the medicine collection
# medicine_collection = chroma_client.get_or_create_collection(name="medicines")


# 3.  Get or create the medicine collection and pass in embedding function
medicine_collection = chroma_client.get_or_create_collection(
    name="medicines", embedding_function=sentence_transformer_ef
)

def add_mock_medicines():
    """
    Adds mock medicines with symptoms & composition for similarity search.
    """
    # Delete existing documents in the collection with a valid filter
    medicine_collection.delete(where={"name": {"$ne": ""}})
    print("Existing documents deleted from ChromaDB.")

    # Insert mock data into ChromaDB
    for med in MOCK_MEDICINES:
        medicine_collection.add(
            ids=[med["id"]],
            documents=[med["name"]],  # Main search key, used for embedding
            metadatas=[{
                "composition": ", ".join(med["composition"]),
                "symptoms": ", ".join(med["symptoms"]),
                "manufacturer": med["manufacturer"],
                "form": med["form"]
            }]
        )

    print("Mock medicines added to ChromaDB!")



# Run this function once to populate ChromaDB
add_mock_medicines()

