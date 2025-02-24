'''
This file contains the pydantic schemas for the medicine table in the database.
'''

from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date
class MedicineCreate(BaseModel):
    name: str
    dosage: Optional[str] = None
    quantity: int
    price: float
    expiry_date: date

    @field_validator("expiry_date", mode="before")
    @classmethod
    def validate_expiry_date(cls, v):
        if isinstance(v, str):  # If expiry_date is a string, convert it to a date
            return date.fromisoformat(v)
        return v

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    expiry_date: Optional[date] = None

    @field_validator("expiry_date", mode="before")
    @classmethod
    def validate_expiry_date(cls, v):
        if isinstance(v, str):  # If expiry_date is a string, convert it to a date
            return date.fromisoformat(v)
        return v