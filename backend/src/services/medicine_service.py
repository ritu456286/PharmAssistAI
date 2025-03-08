from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.configs.db_con import SessionLocal
from src.repositories import medicine_repo
from src.utils.text_cleaning import extract_medicines
from src.vector_db.chromadb_client import find_similar_medicines


def find_alternatives(unavailable_medicines: list, db: Session) -> dict:
    """
    Finds top 5 alternatives from ChromaDB with full medicine structure, and returns max 2 available alternatives for each medicine
    """
    available_alternative_medicines = []
    if unavailable_medicines:
        for med_name in unavailable_medicines:
            count = 0
            alternatives = find_similar_medicines(med_name)  # Get top k alternatives from ChromaDB
            for alt_med in alternatives:
                medicine_found = medicine_repo.get_medicine_by_name(db, alt_med["name"])

                if medicine_found:
                    count +=1
                    available_alternative_medicines.append({
                            "for_medicine": med_name,
                            "id": medicine_found.id,
                            "name": medicine_found.name,
                            "dosage": medicine_found.dosage,
                            "quantity": medicine_found.quantity,
                            "expiry_date": medicine_found.expiry_date,
                            "price": medicine_found.price
                        })
                if count > 2:
                    break
        
        return available_alternative_medicines

def check_medicine_availability(medicines: List[str], db: Session):
    if not medicines:
        raise HTTPException(status_code=400, detail="No valid medicines given.")
    available_medicines = []
    unavailable_medicines = []
    alternative_medicines = []
    for med_name in medicines:
        db_med = medicine_repo.get_medicine_by_name(db, med_name)
       
        if db_med:
         
            available_medicines.append({
                "id": db_med.id,
                "name": db_med.name,
                "dosage": db_med.dosage,
                "quantity": db_med.quantity,
                "expiry_date": db_med.expiry_date,
                "price": db_med.price
            })  
        else:
          
            unavailable_medicines.append(med_name)

    #Find alternatives
    print("UNAVAILABLE: ", unavailable_medicines)
    print("AVAILABLE: ", available_medicines)
    if unavailable_medicines:
        alternative_medicines = find_alternatives(unavailable_medicines, db)
    
    return {
        "available": available_medicines,
        "unavailable": unavailable_medicines,
        "alternatives": alternative_medicines
    }


