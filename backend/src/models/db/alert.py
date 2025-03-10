'''
This file contains the ORM model for the stock alerts table.
'''

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class StockAlert(Base):
    __tablename__ = "stock_alerts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    medicine_id: Mapped[int] = mapped_column(ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False)
    alert_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    status: Mapped[str] = mapped_column(String, default="Active")  # Active, Resolved

    def __repr__(self):
        return f"StockAlert(medicine_id={self.medicine_id}, alert_quantity={self.alert_quantity})"
