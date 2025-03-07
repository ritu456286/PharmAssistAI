from sqlalchemy.orm import Session
from src.models.db.alert import StockAlert
from src.models.db.medicine import Medicine
from src.repositories import alert_repo, medicine_repo
import logging

logging.basicConfig(level=logging.INFO)

DEFAULT_ALERT_QUANTITY = 15

def trigger_alert_if_needed(db: Session, medicine_id: int):
    """
    Create or resolve stock alerts based on current stock and alert threshold.
    """
   
    medicine = medicine_repo.get_medicine_by_id(db, medicine_id)
    
    if not medicine:
        logging.warning(f"[ALERT] Medicine ID {medicine_id} not found.")
        return

    alert = alert_repo.get_alert_by_medicine_id(db, medicine_id)

    if not alert:
        if medicine.quantity <= DEFAULT_ALERT_QUANTITY: 
            logging.info(f"[ALERT] Creating alert for {medicine.id}")
            alert_repo.create_alert(db, medicine_id, medicine.quantity)
        else: 
            alert_repo.create_alert(db, medicine_id, DEFAULT_ALERT_QUANTITY)
        return
    
    if medicine.quantity > alert.alert_quantity and alert.status == "Active":
        logging.info(f"[ALERT] Resolving alert for {medicine.id}")
        alert_repo.resolve_alert(db, medicine_id)
    
    # elif medicine.quantity <= alert.alert_quantity and alert.status != "Resolved":
    #     logging.info(f"[ALERT] Alert already active for {medicine.id}")

    elif medicine.quantity <= alert.alert_quantity and alert.status == "Resolved":
        logging.info(f"[ALERT] Creating alert for {medicine.id}")
        alert_repo.create_alert(db, medicine_id, medicine.quantity)
        

