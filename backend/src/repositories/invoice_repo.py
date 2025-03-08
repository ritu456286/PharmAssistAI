from sqlalchemy.orm import Session
from src.models.db.invoice import Invoice, InvoiceItem
from src.models.db.medicine import Medicine


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

        # Update invoice total amount
        invoice.total_amount = total_amount
        db.commit()
        db.refresh(invoice)

        return invoice

    @staticmethod
    def get_invoice(db: Session, invoice_id: int):
        """Retrieve an invoice by ID."""
        return db.get(Invoice, invoice_id)
