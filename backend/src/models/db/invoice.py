'''
This file contains the ORM model for the invoices table.
'''

from sqlalchemy import Integer, Float, ForeignKey, Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from .medicine import Medicine, Base


class Invoice(Base):
    __tablename__ = "invoices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(String, nullable=False)
    invoice_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Optional Relationship (One Invoice - Many Medicines)
    medicines = relationship("InvoiceItem", back_populates="invoice")

    def __repr__(self):
        return f"Invoice(id={self.id}, customer_name={self.customer_name}, total_amount={self.total_amount})"


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"), nullable=False)
    medicine_id: Mapped[int] = mapped_column(ForeignKey("medicines.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    invoice = relationship("Invoice", back_populates="medicines")
    medicine = relationship("Medicine")

    def __repr__(self):
        return f"InvoiceItem(invoice_id={self.invoice_id}, medicine={self.medicine.name}, quantity={self.quantity}, total_amount={self.total_amount})"
