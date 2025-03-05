from sqlalchemy.orm import Session
from src.models.db.medicine import Medicine
from src.models.schema.medicine import MedicineCreate, MedicineUpdate
from datetime import date


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

def get_medicine_by_name(db: Session, medicine_name: str):
    return db.query(Medicine).filter(Medicine.name == medicine_name).all()

def get_medicine_by_name_and_dosage(db: Session, 
medicine_name: str, dosage: str):
    """
        Return a list of matched medicines by name and dosages, a list because, they might have been purchased in batches, with different prices or expiry_date
    """
    return db.query(Medicine).filter(
        Medicine.name == medicine_name,
        Medicine.dosage.ilike(dosage)  # Case insensitive search
    ).all()

def get_expired_or_unavailable_medicines(db: Session):
    "Returns medicines that should be deleted, expired or unavailable"
    return db.query(Medicine).filter(
            (Medicine.expiry_date < date.today()) | (Medicine.quantity == 0)
        ).all()