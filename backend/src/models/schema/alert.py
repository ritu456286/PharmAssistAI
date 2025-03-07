from pydantic import BaseModel

class ThresholdUpdate(BaseModel):
    new_threshold: int