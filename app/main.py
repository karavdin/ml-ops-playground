from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from model import convert, predict

from db import crud, models, schemas

from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# pydantic models
class StockIn(BaseModel):
    ticker: str


class StockOut(StockIn):
    forecast: dict

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# routes


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


@app.post("/predict", response_model=schemas.Predictions)
def create_predictions(predictions: schemas.PredictionsCreate, db: Session = Depends(get_db)):
    db_prediction = crud.get_predictions(
        db, ticker=predictions.ticker)  # ToDo: check dates
    if db_prediction:
        raise HTTPException(
            status_code=400, detail="Predictions already exist")
    return crud.create_predictions(db=db, predictions=predictions)


@app.get("/predict", response_model=StockOut)
def read_predictions(payload: StockIn, limit: int = 7, db: Session = Depends(get_db)):
    prediction_list = crud.get_predictions(
        db, limit=limit, ticker=payload.ticker)
    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {"ticker": ticker, "forecast": convert(prediction_list)}
    return response_object
