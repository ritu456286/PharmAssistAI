from datetime import datetime
from src.models.db.medicine import Medicine

def seed_medicines(session):
    medicines = [
        Medicine(name="Paracetamol", dosage="500mg", quantity=100, price=2.5, expiry_date=datetime.strptime("2025-12-12", "%Y-%m-%d").date()),
        Medicine(name="Amoxicillin", dosage="250mg", quantity=50, price=3.5, expiry_date=datetime.strptime("2025-12-12", "%Y-%m-%d").date()),
        Medicine(name="Azithromycin", dosage="500mg", quantity=30, price=5.5, expiry_date=datetime.strptime("2025-12-12", "%Y-%m-%d").date()),
        Medicine(name="Ciprofloxacin", dosage="250mg", quantity=70, price=4.5, expiry_date=datetime.strptime("2025-12-12", "%Y-%m-%d").date()),
        Medicine(name="Doxycycline", dosage="100mg", quantity=80, price=6.5, expiry_date=datetime.strptime("2025-12-12", "%Y-%m-%d").date()),
        Medicine(name="Ibuprofen", dosage="200mg", quantity=100, price=2.5, expiry_date=datetime.strptime("2025-12-12", "%Y-%m-%d").date()),
        Medicine(name="Aspirin", dosage="100mg", quantity=100, price=2.5, expiry_date=datetime.strptime("2025-12-14", "%Y-%m-%d").date()),
        Medicine(name="Diazepam", dosage="5mg", quantity=100, price=2.5, expiry_date=datetime.strptime("2025-12-14", "%Y-%m-%d").date()),
        Medicine(name="Lorazepam", dosage="2mg", quantity=100, price=2.5, expiry_date=datetime.strptime("2025-12-12", "%Y-%m-%d").date()),
        Medicine(name="Clonazepam", dosage="1mg", quantity=100, price=2.5, expiry_date=datetime.strptime("2025-12-12", "%Y-%m-%d").date()),
        Medicine(name="Alprazolam", dosage="0.5mg", quantity=100, price=2.5, expiry_date=datetime.strptime("2025-12-12", "%Y-%m-%d").date()),
    ]
   
    
    # Optional: Delete Existing Alerts Before Seeding
    session.query(Medicine).delete()

    session.add_all(medicines)
    session.commit()
    session.close()
