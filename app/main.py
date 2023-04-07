from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.model import predict

from app.db.crud import get_predictions, convert_db_records, clean_db
from app.db.database import engine, Base, get_session
from app.db.models import Predictions

import datetime
import pandas as pd
import numpy as np


def init_db():
    print("###### Start creating schemas ########")
    Base.metadata.create_all(engine)  # start db


print("###### Start FastAPI #####")
app = FastAPI()


# pydantic models
class StockIn(BaseModel):
    ticker: str


class StockOut(StockIn):
    forecast: dict


@app.on_event("startup")
async def on_startup():
    init_db()


@app.post("/fill", status_code=200)
def write_forecast_to_DB(payload: StockIn):
    ticker = payload.ticker
    prediction_list = predict(ticker)
    TODAY = datetime.date.today()
    for data in prediction_list:
        lag = (pd.to_datetime(data["ds"]) -
               pd.to_datetime(TODAY)) / np.timedelta64(1, 'D')
        record = Predictions(ticker=ticker,
                             forecast=data["trend"],
                             date=data["ds"].strftime("%m/%d/%Y"),
                             gen_date=TODAY.strftime("%m/%d/%Y"),
                             lag=lag)
        with get_session() as session:
            session.add(record)
            session.commit()


@app.post("/forecast", response_model=StockOut, status_code=200)
def read_forecast_from_DB(payload: StockIn, limit: int = 7):
    ticker = payload.ticker
    with get_session() as session:
        predictions = get_predictions(session, limit=limit, ticker=ticker)
        if not predictions:
            raise HTTPException(status_code=400, detail="Data not found.")
        response_object = {"ticker": ticker,
                           "forecast": convert_db_records(predictions)}
        return response_object


@app.post("/clean", status_code=200)
def clean_DB():
    with get_session() as session:
        clean_db(session)


@app.get("/testing_api")
def read_all():
    print(" --- Read from DB ---")
    with get_session() as session:
        items = session.query(Predictions).all()

    return items
