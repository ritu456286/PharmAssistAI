from chromadb_conn import medicine_collection

def index_medicine(medicine_name: str, metadata: dict):
    """
    Add a new medicine to ChromaDB with metadata.
    metadata can include composition, manufacturer, etc.
    """
    medicine_collection.add(
        ids=[medicine_name], 
        metadatas=[metadata]
    )

def find_similar_medicines(medicine_name: str, top_k=3):
    """
    Finds top_k similar medicines based on vector similarity.
    """
    try:
        results = medicine_collection.query(
            query_texts=[medicine_name], 
            n_results=top_k
        )

        if not results or "ids" not in results or not results["ids"][0]:
            return []  # No alternatives found
        
        print("From chroma client:", results)
        
        return [
            {"name": res, "score": score} 
            for res, score in zip(results["ids"][0], results["distances"][0])
        ]

    except Exception as e:
        print(f"Error querying ChromaDB: {e}")
        return []