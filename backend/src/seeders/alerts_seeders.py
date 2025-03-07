from src.models.db.alert import StockAlert
from src.models.db.medicine import Medicine
import random

THRESHOLD_RANGES = {
    "Paracetamol": (20, 30),
    "Amoxicillin": (10, 20),
    "Azithromycin": (5, 15),
    "Ciprofloxacin": (20, 30),
    "Doxycycline": (15, 25),
    "Ibuprofen": (20, 30),
    "Aspirin": (25, 35),
    "Diazepam": (5, 10),
    "Lorazepam": (5, 10),
    "Clonazepam": (5, 10),
    "Alprazolam": (5, 10),
}


def get_random_threshold(medicine_name):
    if medicine_name in THRESHOLD_RANGES:
        return random.randint(*THRESHOLD_RANGES[medicine_name])
    return random.randint(5, 15)  # Default threshold range


def seed_alerts(session):
    medicines = session.query(Medicine).all()
    alerts = []

    for medicine in medicines:
        threshold = get_random_threshold(medicine.name)
        status = "Active" if medicine.quantity <= threshold else "Resolved"
        alert = StockAlert(medicine_id=medicine.id, alert_quantity=threshold, status=status)
        alerts.append(alert)

    # Optional: Delete Existing Alerts Before Seeding
    session.query(StockAlert).delete()

    session.add_all(alerts)
    session.commit()
    session.close()