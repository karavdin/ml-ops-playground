import sqlalchemy as sa
from sqlalchemy.orm import Session
from app.db.models import Predictions


def get_predictions(db: Session, ticker: str, limit: int = 7):
    forecast = db.query(Predictions).filter(
        Predictions.ticker == ticker).limit(limit).all()
    return forecast


def convert_db_records(predictions):
    output = {}
    for data in predictions:
        date = data.date.strftime("%m/%d/%Y")
        output[date] = data.forecast
    return output


def clean_db(db: Session):

    # Create a query that identifies the row for each domain with the lowest id
    inner_q = db.query(sa.func.min(Predictions.id)).group_by(
        Predictions.ticker, Predictions.date)
    aliased = sa.alias(inner_q)
    # Select the rows that do not match the subquery
    q = db.query(Predictions).filter(~Predictions.id.in_(aliased))

    # Delete the unmatched rows (SQLAlchemy generates a single DELETE statement from this loop)
    for forecast in q:
        db.delete(forecast)
    db.commit()
