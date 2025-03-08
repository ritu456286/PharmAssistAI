from sqlalchemy.orm import Session
from src.models.db.alert import StockAlert
from src.models.db.medicine import Medicine

DEFAULT_THRESHOLD_VALUE = 15  # Default Alert Quantity Threshold

def create_alert(db: Session, medicine_id: int, alert_quantity: int = DEFAULT_THRESHOLD_VALUE):
    """
    Create new stock alert, will be active
    """
    new_alert = StockAlert(medicine_id=medicine_id, alert_quantity=alert_quantity, status="Active")
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return new_alert


def resolve_alert(db: Session, medicine_id: int):
    """
    Resolve active alert
    """
    alert = (
        db.query(StockAlert)
        .filter(StockAlert.medicine_id == medicine_id, StockAlert.status == "Active")
        .first()
    )
    if alert:
        alert.status = "Resolved"
        db.commit()
        return alert
    return None

def get_active_alerts(db: Session):
    return (
        db.query(StockAlert)
        .filter(StockAlert.status == "Active")
        .all()
    )

def get_all_alerts(db: Session):
    """
    Get all alerts with medicine name to display in frontend
    """
    alerts = (
        db.query(StockAlert.id, StockAlert.medicine_id, StockAlert.alert_quantity, StockAlert.status, Medicine.name.label("medicine_name"))
        .join(Medicine, Medicine.id == StockAlert.medicine_id)
        .all()
    )
    print("ALERTS>>>>>")
    return [{"id": alert.id, "medicine_id": alert.medicine_id, "medicine_name": alert.medicine_name, "alert_quantity": alert.alert_quantity, "status": alert.status} for alert in alerts]


def get_alert_by_medicine_id(db: Session, medicine_id: int):
    return db.query(StockAlert).filter(StockAlert.medicine_id == medicine_id).first()


def update_alert(db: Session, medicine_id: int, new_threshold: int):
    """
    Update alert threshold by Medicine ID
    Automatically updates status based on new quantity vs threshold
    """
    alert = (
        db.query(StockAlert)
        .filter(StockAlert.medicine_id == medicine_id)
        .first()
    )

    if not alert:
        return None
    # Update alert quantity
    alert.alert_quantity = new_threshold

    # Fetch the linked medicine
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()

    if medicine:
        # Auto-update status based on new threshold
        print("MEDICINE" , medicine)
        if medicine.quantity <= new_threshold:
            alert.status = "Active"
        else:
            alert.status = "Resolved"

    db.commit()
    db.refresh(alert)
    return alert