from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.repositories import medicine_repo
from src.utils.text_cleaning import extract_medicines_and_dosages
from src.vector_db.chromadb_client import find_similar_medicines

def check_medicine_availability(prescription_text: str, db: Session):
    """
    1. Extract medicines from the prescription.
    2. Check if they are available in SQLite3 inventory.
    3. If unavailable, query ChromaDB for top 3 alternatives.
    4. Only return alternatives that are in stock.
    """
    medicines, dosages = extract_medicines_and_dosages(prescription_text)

    if not medicines:
        raise HTTPException(status_code=400, detail="No valid medicines found.")

    available_medicines = []
    unavailable_medicines = []
    alternative_medicines = {}

    for med in medicines:
        db_med_list = medicine_repo.get_medicine_by_name(db, med)  # Check inventory

        if db_med_list:  # If any dosage exists in inventory
            available_medicines.append({
                "name": med,
                "dosages": [
                    {
                        "id": db_med.id,
                        "quantity": db_med.quantity,
                        "dosage": db_med.dosage
                    }
                    for db_med in db_med_list if db_med.quantity > 0  # Only add if in stock
                ]
            })
        else:
            unavailable_medicines.append(med)

    # Find alternatives only for unavailable medicines
    if unavailable_medicines:
        for med in unavailable_medicines:
            alternatives = find_similar_medicines(med)  # Get top 3 alternatives from ChromaDB
            available_alternatives = []
            for alt in alternatives:
                db_alt_list = medicine_repo.get_medicine_by_name(db, alt["name"])
                
                # Check if any alternative dosage is available
                if db_alt_list:
                    filtered_dosages = [
                        {
                            "id": db_alt.id,
                            "quantity": db_alt.quantity,
                            "strength": db_alt.strength
                        }
                        for db_alt in db_alt_list if db_alt.quantity > 0
                    ]

                    if filtered_dosages:
                        available_alternatives.append({
                            "name": alt["name"],
                            "dosages": filtered_dosages
                        })

            alternative_medicines[med] = available_alternatives

            # for alt in alternatives:
            #     db_alt_list = medicine_repo.get_medicine_by_name(db, alt["name"])
                
            #     # Check if any alternative dosage is available
            #     if any(db_alt.quantity > 0 for db_alt in db_alt_list):
            #         available_alternatives.append(alt)

            # alternative_medicines[med] = available_alternatives

    return {
        "extracted_medicines": medicines,
        "available": available_medicines,
        "unavailable": unavailable_medicines,
        "alternatives": alternative_medicines
    }
