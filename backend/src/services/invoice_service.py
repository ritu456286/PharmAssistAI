from sqlalchemy.orm import Session
from src.repositories.invoice_repo import InvoiceRepository
from src.models.schema.invoice import InvoiceCreate, InvoiceResponse


class InvoiceService:
    """Handles business logic for invoices."""

    @staticmethod
    def create_invoice(db: Session, invoice_data: InvoiceCreate):
        """Creates an invoice using the repository."""
        medicines = {int(k): v for k, v in invoice_data.medicines.items()}  # Convert str keys to int
        invoice = InvoiceRepository.create_invoice(
            db=db,
            patient_name=invoice_data.patient_name,
            doctor_name=invoice_data.doctor_name,
            clinic_name=invoice_data.clinic_name,
            medicines=medicines,
            invoice_date=invoice_data.invoice_date
        )
        return InvoiceResponse.from_orm(invoice)

    @staticmethod
    def get_invoice(db: Session, invoice_id: int):
        """Retrieves an invoice by ID."""
        invoice = InvoiceRepository.get_invoice(db, invoice_id)
        if not invoice:
            return None
        return InvoiceResponse.from_orm(invoice)
