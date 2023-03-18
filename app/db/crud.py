from sqlalchemy.orm import Session

from app.db import schemas
from app.db import models


def get_items(db: Session):
    return db.execute(models.Predictions).scalars().all()


def get_predictions(db: Session, ticker: str, limit: int = 7):
    # print(" Query forecast")
    forecast = db.query(models.Predictions).filter(
        models.Predictions.ticker == ticker).limit(limit).all()
    # print(forecast)
    return forecast


def convert_db_records(predictions):
    output = {}
    for data in predictions:
        print("data", data)
        print("data['ticker']", data['ticker'])
        print("data['date']", data["date"])
        date = data["date"].strftime("%m/%d/%Y")
        output[date] = data["forecast"]
    return output


# def create_predictions(db: Session, predictions: schemas.PredictionsCreate):
#     db_predictions = models.Predictions(
#         date=predictions.date,
#         ticker=predictions.ticker,
#         forecast=predictions.forecast
#     )

#     db.add(db_predictions)
#     db.commit()
#     db.refresh(db_predictions)
#     return db_predictions
