from pydantic import BaseModel
from typing import Optional


class EnvironmentalDataSchema(BaseModel):
    date: str
    region: str
    temperature: float
    humidity: float
    rainfall: float
    aqi: float

    class Config:
        from_attributes = True


class PredictRequest(BaseModel):
    temperature: float
    humidity: float
    rainfall: float


class PredictResponse(BaseModel):
    predicted_aqi: float
    warning: Optional[str] = None
