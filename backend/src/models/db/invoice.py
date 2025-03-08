'''
This file contains the ORM model for the invoices table.
'''

from sqlalchemy import Integer, Float, ForeignKey, Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import List
from .medicine import Medicine
from .database import Base
from sqlalchemy.orm.session import Session


class Invoice(Base):
    __tablename__ = "invoices"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_name: Mapped[str] = mapped_column(String, nullable=False)
    doctor_name: Mapped[str] = mapped_column(String, nullable=False)
    clinic_name: Mapped[str] = mapped_column(String, nullable=False)
    invoice_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # One Invoice can have many InvoiceItems
    medicines: Mapped[List["InvoiceItem"]] = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Invoice(id={self.id}, patient_name={self.patient_name}, doctor_name={self.doctor_name}, clinic_name={self.clinic_name}, total_amount={self.total_amount})"


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"), nullable=False)
    medicine_id: Mapped[int] = mapped_column(ForeignKey("medicines.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=False)  # Fetched from medicines
    total_price: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="medicines")
    medicine: Mapped["Medicine"] = relationship("Medicine")

    def __repr__(self):
        return f"InvoiceItem(invoice_id={self.invoice_id}, medicine={self.medicine.name}, quantity={self.quantity}, total_price={self.total_price})"

    @classmethod
    def create(cls, session: Session, invoice_id: int, medicine_id: int, quantity: int):
        """Creates an InvoiceItem by fetching the price from the Medicine table."""
        medicine = session.get(Medicine, medicine_id)
        if not medicine:
            raise ValueError("Medicine not found")

        price_per_unit = medicine.price  # Fetching price from Medicine
        total_price = price_per_unit * quantity

        return cls(invoice_id=invoice_id, medicine_id=medicine_id, quantity=quantity,
                   price_per_unit=price_per_unit, total_price=total_price)
