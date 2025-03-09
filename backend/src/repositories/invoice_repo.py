from sqlalchemy.orm import Session
from src.models.schema.medicine import MedicineUpdate
from src.models.db.invoice import Invoice, InvoiceItem
from src.models.db.medicine import Medicine
from src.repositories.medicine_repo import update_medicine 

class InvoiceRepository:
    """Handles all invoice-related database operations."""

    @staticmethod
    def create_invoice(db: Session, patient_name: str, doctor_name: str, clinic_name: str, medicines: dict, invoice_date):
        """
        Create a new invoice and add medicine items.
        medicines = {medicine_id: quantity}
        """
        total_amount = 0.0
        invoice = Invoice(
            patient_name=patient_name,
            doctor_name=doctor_name,
            clinic_name=clinic_name,
            invoice_date=invoice_date,
            total_amount=0.0  # Will be updated after calculating medicines
        )

        db.add(invoice)
        db.flush()  # Get the invoice ID before committing

        # Add medicines to invoice
        for medicine_id, quantity in medicines.items():
            medicine = db.get(Medicine, medicine_id)
            if not medicine:
                raise ValueError(f"Medicine ID {medicine_id} not found")

            price_per_unit = medicine.price  # Get price from Medicine table
            total_price = price_per_unit * quantity
            total_amount += total_price

            invoice_item = InvoiceItem(
                invoice_id=invoice.id,
                medicine_id=medicine_id,
                quantity=quantity,
                price_per_unit=price_per_unit,
                total_price=total_price
            )

            db.add(invoice_item)

            # Reduce the medicine stock
            updated_medicine = MedicineUpdate(quantity=medicine.quantity - quantity)
            update_medicine(db, medicine_id, updated_medicine)


        # Update invoice total amount
        invoice.total_amount = total_amount
        db.commit()
        db.refresh(invoice)

        return invoice

    @staticmethod
    def get_invoice(db: Session, invoice_id: int):
        """Retrieve an invoice by ID."""
        return db.get(Invoice, invoice_id)

    @staticmethod
    def get_all_invoices(db: Session):
        """Retrieve all invoices."""
        return db.query(Invoice).all()
    
    @staticmethod
    def delete_invoice(db: Session, invoice_id: int) -> bool:
        """Deletes an invoice by ID and returns True if deleted, False if not found."""
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            return False  # Invoice not found

        db.delete(invoice)
        db.commit()
        return True