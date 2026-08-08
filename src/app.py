from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

from src.data.feature_engineering import load_data
from src.data.predict import load_pipeline, predict_price
from src.data.utils import DEFAULT_MODEL_PATH

app = FastAPI(
    title="Commodity Price Forecast API",
    description="A simple FastAPI service for commodity price prediction.",
    version="1.0.0",
)

MODEL_PATH = DEFAULT_MODEL_PATH
MODEL = None
HISTORICAL_DATA = None
STATIC_PAGE = Path(__file__).resolve().parent / "static" / "index.html"


class PredictionRequest(BaseModel):
    country: str
    admin_1: str
    market: str
    currency: str
    product: str
    year: int
    month: int


@app.on_event("startup")
def startup_event():
    global MODEL, HISTORICAL_DATA
    try:
        MODEL = load_pipeline(MODEL_PATH)
    except Exception as exc:
        MODEL = None
        print(f"Warning: failed to load model at {MODEL_PATH}: {exc}")

    try:
        HISTORICAL_DATA = load_data()
    except Exception as exc:
        HISTORICAL_DATA = None
        print(f"Warning: failed to load historical data: {exc}")


@app.get("/", response_class=HTMLResponse)
def read_index():
    if STATIC_PAGE.exists():
        return FileResponse(STATIC_PAGE)
    raise HTTPException(status_code=404, detail="Frontend page not found")


@app.post("/predict")
def predict(request: PredictionRequest):
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    if HISTORICAL_DATA is None:
        raise HTTPException(status_code=503, detail="Historical data not available")

    payload = request.dict()
    try:
        predicted_price = predict_price(MODEL, payload, HISTORICAL_DATA)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="Prediction failed")

    return {"predicted_price": predicted_price}
