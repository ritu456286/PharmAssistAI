from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.repositories import medicine_repo
from src.configs.db_con import SessionLocal
from src.models.schema.medicine import MedicineCreate, MedicineUpdate

router = APIRouter(prefix="/medicines", tags=["medicines"])

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

#GET /medicines/{medicine_id}
@router.get("/{medicine_id}")
def get_medicine_by_id(medicine_id: int, db: Session = Depends(get_db)):
    med = medicine_repo.get_medicine_by_id(db, medicine_id)
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return med

#PUT /medicines/{medicine_id}
@router.put("/{medicine_id}")
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