'''
This file contains the ORM model for the medicine table in the database.
'''

from sqlalchemy import Integer, String, Float, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional


class Base(DeclarativeBase):
    pass


#This is an orm model for the medicine table, and not a pydantic model
class Medicine(Base):
    __tablename__ = "medicines"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    dosage: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    expiry_date: Mapped[str] = mapped_column(Date, nullable=False)

    def __repr__(self):
        return f"{self.name} - {self.dosage} - {self.quantity} - {self.price} - {self.expiry_date}"