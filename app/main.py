import logging
# from loguru import logger
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from app.model import convert, predict

from app.db.crud import get_predictions
from app.db.database import SessionLocal, engine, Base, get_db
from app.db.models import Predictions
from app.db import schemas


def init_db():
    print("###### Start creating schemas ########")
    Base.metadata.create_all(engine)  # start db

# SessionLocal = sessionmaker(autoflush=False, bind=engine)
# db = SessionLocal()


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


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.post("/predict", response_model=StockOut, status_code=200)
def get_prediction(payload: StockIn):
    ticker = payload.ticker

    prediction_list = predict(ticker)

    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {"ticker": ticker, "forecast": convert(prediction_list)}
    return response_object


@app.post("/fill", response_model=StockOut, status_code=200)
def fill_db(payload: StockIn):
    ticker = payload.ticker
    # print("##### Fill database #####")
    prediction_list = predict(ticker)
    # print(prediction_list)
    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {"ticker": ticker, "forecast": convert(prediction_list)}
    return response_object

# tom = Predictions(ticker="Tom", forecast=0.1)
# db.add(tom)     # add to db
# db.commit()     # save changes
# db.refresh(tom)
# print(tom.id)   # get ID


"""

@app.post("/predict", response_model=schemas.Predictions)
def create_predictions(predictions: schemas.PredictionsCreate, db: Session = Depends(get_db)):
    db_prediction = get_predictions(
        db, ticker=predictions.ticker)  # ToDo: check dates
    if db_prediction:
        raise HTTPException(
            status_code=400, detail="Predictions already exist")
    return crud.create_predictions(db=db, predictions=predictions)


@app.get("/predict", response_model=StockOut)
def read_predictions(payload: StockIn, limit: int = 7, db: Session = Depends(get_db)):
    prediction_list = get_predictions(
        db, limit=limit, ticker=payload.ticker)
    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {"ticker": ticker, "forecast": convert(prediction_list)}
    return response_object
"""
