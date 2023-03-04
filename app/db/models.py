from sqlalchemy import Column, Float, Integer, String, Date
from app.db.database import Base


class Predictions(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    ticker = Column(String)
    forecast = Column(Float)
