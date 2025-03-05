from src.vector_db.chromadb_conn import medicine_collection

def index_medicine(medicine_name: str, metadata: dict):
    """
    Add a new medicine to ChromaDB with metadata.
    metadata can include composition, manufacturer, etc.
    """
    medicine_collection.add(
        ids=[medicine_name], 
        metadatas=[metadata]
    )

    
def find_similar_medicines(medicine_name: str, top_k=4):
    """
    Finds top_k similar medicines based on vector similarity.
    Excludes the queried medicine from the results.
    """
    try:
        results = medicine_collection.query(
            query_texts=[medicine_name], 
            n_results=top_k + 2  # Fetch extra in case the same medicine is included
        )

        if not results or "documents" not in results or not results["documents"][0]:
            return []  # No alternatives found

        print(f"\nRaw ChromaDB response for {medicine_name}: {results}\n")  # Debugging

        # Extract document names
        retrieved_medicines = results["documents"][0]
        retrieved_ids = results["ids"][0]
        retrieved_distances = results["distances"][0]

        # Exclude exact match (i.e., if the document name matches the queried medicine)
        alternatives = [
            {"name": med, "score": score}
            for med, score in zip(retrieved_medicines, retrieved_distances)
            if med.lower().strip() != medicine_name.lower().strip()  # Stricter check
        ]

        print(f"\nFiltered alternatives for {medicine_name}: {alternatives}\n")  # Debugging

        # Limit results to top_k after filtering
        return alternatives[:top_k]

    except Exception as e:
        print(f"Error querying ChromaDB: {e}")
        return []
