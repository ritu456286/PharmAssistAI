from mock_medicine_data import MOCK_MEDICINES
from src.vector_db.chromadb_conn import medicine_collection

def add_mock_medicines():
    """
    Adds mock medicines with symptoms & composition for similarity search.
    """
    
    # Insert mock data into ChromaDB
    for med in MOCK_MEDICINES:
        medicine_collection.add(
            ids=[med["id"]],
            documents=[med["name"]],  # Main search key
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