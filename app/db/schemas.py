from typing import List
from pydantic import BaseModel
from datetime import date


class PredictionsBase(BaseModel):
    id: int
    date: date
    ticker: str
    forecast: float


class PredictionsCreate(PredictionsBase):
    pass


class Predictions(PredictionsBase):

    class Config:
        orm_mode = True
