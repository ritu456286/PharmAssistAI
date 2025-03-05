from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.configs.db_con import SessionLocal
from src.repositories import medicine_repo
from src.utils.text_cleaning import extract_medicines_and_dosages
from src.vector_db.chromadb_client import find_similar_medicines
import logging


def find_alternatives(unavailable_medicines: list, db: Session) -> dict:
    """
    Finds top 5 alternatives from ChromaDB with full medicine structure
    """
    alternative_medicines = {}
    if unavailable_medicines:
        for med in unavailable_medicines:
            alternatives = find_similar_medicines(med["name"])  # Get top k alternatives from ChromaDB
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
                    alternative_medicines[med["name"]] = available_alternatives[:5] 
        return alternative_medicines


def check_medicine_availability(prescription_text: str, db: Session):
    """
    1. Extract medicines from the prescription.
    2. Check if they are available in SQLite3 inventory.
    3. If unavailable, query ChromaDB for top 3 alternatives.
    4. Only return alternatives that are in stock.
    """
    medicine_data = extract_medicines_and_dosages(prescription_text)

    if not medicine_data:
        raise HTTPException(status_code=400, detail="No valid medicines found.")

    available_medicines = []
    unavailable_medicines = []
    alternative_medicines = {}
    # Iterate medicines with zip_longest to handle missing dosages
    from itertools import zip_longest

    for med_data in medicine_data:
        if med_data["dosage"]:  # If dosage is present
            db_med_list = medicine_repo.get_medicine_by_name_and_dosage(db, med_data["name"], med_data["dosage"])
            print("HELLO TO DB_MED__LIST")
            print(db_med_list)
    
        else:  # If dosage is missing due to OCR error or in general, check only by name and find all dosages
            
            db_med_list = medicine_repo.get_medicine_by_name(db, med_data["name"])

            print("HELLO TO DB_MED__LIST")
            print(db_med_list)
    
        if db_med_list:
            available_medicines.extend(db_med_list)  # Append all matched medicines
        else:
            unavailable_medicines.append({
                "name": med_data["name"],
                "dosage": med_data["dosage"] if med_data["dosage"] else None
            })
    if unavailable_medicines:
        alternative_medicines = find_alternatives(unavailable_medicines, db)

    return {
        "extracted_medicines": medicine_data,
        "available": available_medicines,
        "unavailable": unavailable_medicines,
        "alternatives": alternative_medicines
    }

# To cleanup the medicines if expired, use Background Scheduler to schedule the cleanup
def cleanup_expired_medicines():
    db: Session = SessionLocal()  # Create session locally inside the function
    try:
        expired_meds = medicine_repo.get_expired_or_unavailable_medicines(db)
        if expired_meds:
            logging.info(f"[CLEANUP] Found {len(expired_meds)} expired or out-of-stock medicines")
            for med in expired_meds:
                logging.info(f"[DELETE] {med.name} - {med.dosage} - Expiry: {med.expiry_date} - Qty: {med.quantity}")
                deleted_med = medicine_repo.delete_medicine(db, med.id)
            logging.info("[CLEANUP] Medicines cleanup completed successfully")
        else:
            logging.info("[CLEANUP] No expired or out-of-stock medicines found")
    
    except Exception as e:
        logging.error(f"[CLEANUP ERROR] {e}")
        db.rollback()
    finally:
        db.close()
        logging.info("[CLEANUP] Database connection closed")