'''
This file contains the ORM model for the medicine table in the database.
'''

from sqlalchemy import Integer, String, Float, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from .database import Base
from sqlalchemy.event import listens_for
from .alert import StockAlert
from sqlalchemy.orm import Session

#This is an orm model for the medicine table, and not a pydantic model
class Medicine(Base):
    __tablename__ = "medicines"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    dosage: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    expiry_date: Mapped[str] = mapped_column(Date, nullable=False)

    stock_alerts = relationship("StockAlert", backref="medicine", cascade="all, delete-orphan")

    def __repr__(self):
        return f"{self.name} - {self.dosage} - {self.quantity} - {self.price} - {self.expiry_date}"
    
# Event listener to create a StockAlert after a Medicine is inserted
# @listens_for(Medicine, "after_insert")
# def create_stock_alert(mapper, connection, target):
#     session = Session.object_session(target)  # Get the session
#     if session:
#         stock_alert = StockAlert(medicine_id=target.id, alert_quantity=10)  # Default alert quantity = 10
#         session.add(stock_alert)
#         # session.commit()
#         # session.flush() 