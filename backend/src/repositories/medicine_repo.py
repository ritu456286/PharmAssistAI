from sqlalchemy.orm import Session
from src.models.db.medicine import Medicine
from src.models.schema.medicine import MedicineCreate, MedicineUpdate

def create_medicine(db: Session, medicine: MedicineCreate):
    med = Medicine(**medicine.model_dump()) # unpacking the dictionary to orm model
    db.add(med)
    db.commit()
    db.refresh(med)
    return med


def get_medicines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Medicine).offset(skip).limit(limit).all()


def get_medicine_by_id(db: Session, medicine_id: int):
    return db.query(Medicine).filter(Medicine.id == medicine_id).first()


def update_medicine(db: Session, medicine_id: int, medicine: MedicineUpdate):
    med = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not med:
        return None
    
    for key, value in medicine.model_dump(exclude_unset=True).items():
        setattr(med, key, value)
   
    db.commit()
    db.refresh(med)
    return med


def delete_medicine(db: Session, medicine_id: int):
    med = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not med:
        return None
    db.delete(med)
    db.commit()
    return med