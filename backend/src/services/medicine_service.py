from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.configs.db_con import SessionLocal
from src.repositories import medicine_repo
from src.utils.text_cleaning import extract_medicines
from src.vector_db.chromadb_client import find_similar_medicines


def find_alternatives(unavailable_medicines: list, db: Session) -> dict:
    """
    Finds top 5 alternatives from ChromaDB with full medicine structure
    """
    alternative_medicines = {}
    if unavailable_medicines:
        for med_name in unavailable_medicines:
            alternatives = find_similar_medicines(med_name)  # Get top k alternatives from ChromaDB
            available_alternatives = []
            for alt_med_name in alternatives:
                medicines_found_list = medicine_repo.get_medicine_by_name(db, alt_med_name["name"])

                if medicines_found_list:
                    for alt_med in medicines_found_list:
                        available_alternatives.append({
                            "name": alt_med.name,
                            "dosage": alt_med.dosage,
                            "quantity": alt_med.quantity,
                            "expiry_date": alt_med.expiry_date,
                            "price": alt_med.price
                        })
                if available_alternatives:
                    alternative_medicines[med_name] = available_alternatives[:5] 
        return alternative_medicines


def check_medicine_availability(prescription_text: str, db: Session):
    """
    1. Extract medicines from the prescription.
    2. Check if they are available in SQLite3 inventory.
    3. If unavailable, query ChromaDB for top 3 alternatives.
    4. Only return alternatives that are in stock.
    """
    # medicine_data = extract_medicines_and_dosages(prescription_text)
    medicines_list = extract_medicines(prescription_text)

    if not medicines_list:
        raise HTTPException(status_code=400, detail="No valid medicines found.")

    available_medicines = []
    unavailable_medicines = []
    alternative_medicines = {}
    # Iterate medicines with zip_longest to handle missing dosages
    from itertools import zip_longest

    for med_name in medicines_list:
        db_med_list = medicine_repo.get_medicine_by_name(db, med_name)
        if db_med_list:
            available_medicines.extend(db_med_list)  
        else:
            unavailable_medicines.append(med_name)
    if unavailable_medicines:
        alternative_medicines = find_alternatives(unavailable_medicines, db)

    return {
        "extracted_medicines": medicines_list,
        "available": available_medicines,
        "unavailable": unavailable_medicines,
        "alternatives": alternative_medicines
    }

