from sqlalchemy.orm import Session

from app.db import schemas
from app.db import models


def get_predictions(db: Session, ticker: str, limit: int = 7):
    return db.query(models.Predictions).filter(models.Predictions.ticker == ticker).limit(limit).all()


def create_predictions(db: Session, predictions: schemas.PredictionsCreate):
    db_predictions = models.Predictions(
        date=predictions.date,
        ticker=predictions.ticker,
        forecast=predictions.forecast
    )

    db.add(db_predictions)
    db.commit()
    db.refresh(db_predictions)
    return db_predictions
