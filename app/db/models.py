from sqlalchemy import Date, Column, Float, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Predictions(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    # date = Column(Date)
    ticker = Column(String)
    forecast = Column(Float)
