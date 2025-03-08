from pydantic import BaseModel
from datetime import date
from typing import Dict


class InvoiceCreate(BaseModel):
    """Schema for creating an invoice."""
    patient_name: str
    doctor_name: str
    clinic_name: str
    medicines: Dict[str, int]  # {medicine_id: quantity}
    invoice_date: date


class InvoiceResponse(BaseModel):
    """Schema for returning invoice details."""
    id: int
    patient_name: str
    doctor_name: str
    clinic_name: str
    total_amount: float
    invoice_date: date

    class Config:
        from_attributes = True  # Enables ORM compatibility
