from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.configs.db_con import SessionLocal
from src.services.invoice_service import InvoiceService
from src.models.schema.invoice import InvoiceCreate, InvoiceResponse

router = APIRouter()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=InvoiceResponse)
def create_invoice(invoice_data: InvoiceCreate, db: Session = Depends(get_db)):
    """
    Create a new invoice with medicine details.
    """
    try:
        invoice = InvoiceService.create_invoice(db, invoice_data)
        return invoice
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an invoice by ID.
    """
    invoice = InvoiceService.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.get("/", response_model=List[InvoiceResponse])
def get_all_invoices(db: Session = Depends(get_db)):
    """
    Retrieve all invoices.
    """
    invoices = InvoiceService.get_all_invoices(db)
    return invoices
     
    
@router.delete("/{invoice_id}", status_code=204)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """
    Delete an invoice by ID.
    """
    deleted = InvoiceService.delete_invoice(db, invoice_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"message": "Invoice deleted successfully"}