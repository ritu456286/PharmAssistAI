from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.repositories import medicine_repo
from src.configs.db_con import SessionLocal
from src.models.schema.medicine import MedicineCreate, MedicineUpdate
from src.services.medicine_service import check_medicine_availability
import logging
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#POST /medicines
@router.post("/")
def create_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    return medicine_repo.create_medicine(db, medicine)

#GET /medicines
@router.get("/")
def get_medicines(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return medicine_repo.get_medicines(db, skip, limit)


@router.get("/below-threshold", summary="Get Medicines Below Threshold")
def get_medicines_below_threshold(db: Session = Depends(get_db)):
    """
    Fetch medicines whose stock is below the alert quantity threshold
    """
    try:
        medicines = medicine_repo.get_medicines_below_threshold(db)
        return {"medicines": medicines}
    except Exception as e:
        logging.error(f"[API ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

#POST /medicines/check-availability
@router.post("/check-availability")
def check_availability_endpoint(medicines: dict, db: Session = Depends(get_db)):
    """
    Check the availability of medicines in the database.

    This endpoint accepts a JSON object containing a list of medicine names
    and returns their availability status. The response includes:
    - `available`: A list of medicines that are in stock, with details like dosage, quantity, expiry date, and price.
    - `unavailable`: A list of medicines that are not found in the database.
    - `alternatives`: Suggested alternative medicines for the unavailable ones.

    Parameters:
    - medicines (dict): A JSON object containing a key `"medicines"` with a list of medicine names.
    - db (Session): Database session dependency.

    Returns:
    - JSON object containing `available`, `unavailable`, and `alternatives` lists.
    
    """
    try:
        if "medicines" not in medicines or not isinstance(medicines["medicines"], list):
            raise HTTPException(status_code=400, detail="Invalid request format. Expected a list under 'medicines' key.")

        return check_medicine_availability(medicines["medicines"], db)
    
    except HTTPException as http_exc:
        raise http_exc  # Re-raise FastAPI's HTTP exception
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# POST /medicines/check-availability
# @router.post("/check-availability")
# def check_availability_endpoint(prescription_text: str, db: Session = Depends(get_db)):
#     return check_medicine_availability(prescription_text, db)


#GET /medicines/{medicine_name}
@router.get("/{medicine_name}")
def get_medicine_by_name(medicine_name: str, db: Session = Depends(get_db)):
    med = medicine_repo.get_medicine_by_name(db, medicine_name)
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return med


#GET /medicines/{medicine_id}
@router.get("/{medicine_id}")
def get_medicine_by_id(medicine_id: int, db: Session = Depends(get_db)):
    med = medicine_repo.get_medicine_by_id(db, medicine_id)
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return med


#PUT /medicines/{medicine_id}
@router.patch("/{medicine_id}")
def update_medicine(medicine_id: int, medicine: MedicineUpdate, db: Session = Depends(get_db)):
    print(f"Received update request for medicine_id={medicine_id}: {medicine.model_dump(exclude_unset=True)}")  # Debug print
    med = medicine_repo.update_medicine(db, medicine_id, medicine)
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return med

#DELETE /medicines/{medicine_id}
@router.delete("/{medicine_id}")
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    med = medicine_repo.delete_medicine(db, medicine_id)
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return med




