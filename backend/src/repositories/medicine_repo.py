from sqlalchemy.orm import Session
from src.models.db.medicine import Medicine
from src.models.schema.medicine import MedicineCreate, MedicineUpdate
from datetime import date
from src.models.db.alert import StockAlert
from src.repositories import alert_repo
## Creating a new medicine
def create_medicine(db: Session, medicine: MedicineCreate):
    med = Medicine(**medicine.model_dump()) # unpacking the dictionary to orm model
    db.add(med)
    db.commit()
    db.refresh(med)

    # Automatically Create Default Alert
    alert_repo.create_alert(db, med.id)

    return med


def get_medicines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Medicine).offset(skip).limit(limit).all()

def get_all_medicines(db: Session):
    return db.query(Medicine).all()

def get_medicines_count(db: Session):
    return db.query(Medicine).count()

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

    # Trigger alert check after update
    from src.services.alert_service import trigger_alert_if_needed
   
    trigger_alert_if_needed(db, medicine_id)
    
    return med

#DELETE complete medicine row data by id
def delete_medicine(db: Session, medicine_id: int):
    med = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not med:
        return None
    db.delete(med)
    db.commit() 
    return med

def get_medicine_by_name(db: Session, medicine_name: str):
    return db.query(Medicine).filter(Medicine.name == medicine_name).first()

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

def get_medicines_below_threshold(db: Session):
    "Returns medicines that have a quantity less than or equal to the alert quantity in stock alerts table"
    result = (
        db.query(Medicine)
        .join(StockAlert, Medicine.id == StockAlert.medicine_id)
        .filter(
            
            Medicine.quantity <= StockAlert.alert_quantity,
            
        )
        .all()
    )
    return result