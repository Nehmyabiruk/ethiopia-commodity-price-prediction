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
OPTIONS = None
STATIC_PAGE = Path(__file__).resolve().parent / "static" / "index.html"


def build_dropdown_options(df):
    clean_df = df.dropna(subset=["country", "admin_1", "market", "product", "currency"])
    combos = (
        clean_df[["country", "admin_1", "market", "product", "currency"]]
        .drop_duplicates()
        .sort_values(["country", "admin_1", "market", "product", "currency"])
    )

    return {
        "country": sorted(combos["country"].astype(str).unique().tolist()),
        "admin_1": sorted(combos["admin_1"].astype(str).unique().tolist()),
        "market": sorted(combos["market"].astype(str).unique().tolist()),
        "product": sorted(combos["product"].astype(str).unique().tolist()),
        "currency": sorted(combos["currency"].astype(str).unique().tolist()),
        "year": sorted(df["period_date"].dt.year.dropna().astype(int).unique().tolist()),
        "month": sorted(df["period_date"].dt.month.dropna().astype(int).unique().tolist()),
        "combos": combos.to_dict(orient="records"),
    }


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
    global MODEL, HISTORICAL_DATA, OPTIONS
    try:
        MODEL = load_pipeline(MODEL_PATH)
    except Exception as exc:
        MODEL = None
        print(f"Warning: failed to load model at {MODEL_PATH}: {exc}")

    try:
        HISTORICAL_DATA = load_data()
        OPTIONS = build_dropdown_options(HISTORICAL_DATA)
    except Exception as exc:
        HISTORICAL_DATA = None
        OPTIONS = None
        print(f"Warning: failed to load historical data: {exc}")


@app.get("/", response_class=HTMLResponse)
def read_index():
    if STATIC_PAGE.exists():
        return FileResponse(STATIC_PAGE)
    raise HTTPException(status_code=404, detail="Frontend page not found")


@app.get("/options")
def get_options():
    if OPTIONS is None:
        raise HTTPException(status_code=503, detail="Historical data not available")
    return OPTIONS


def is_valid_combo(payload: dict) -> bool:
    if OPTIONS is None:
        return False
    for row in OPTIONS["combos"]:
        if (
            str(row["country"]).strip().lower() == str(payload["country"]).strip().lower()
            and str(row["admin_1"]).strip().lower() == str(payload["admin_1"]).strip().lower()
            and str(row["market"]).strip().lower() == str(payload["market"]).strip().lower()
            and str(row["product"]).strip().lower() == str(payload["product"]).strip().lower()
            and str(row["currency"]).strip().lower() == str(payload["currency"]).strip().lower()
        ):
            return True
    return False


@app.post("/predict")
def predict(request: PredictionRequest):
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    if HISTORICAL_DATA is None:
        raise HTTPException(status_code=503, detail="Historical data not available")

    payload = request.dict()
    if not is_valid_combo(payload):
        raise HTTPException(status_code=400, detail="Selected combination is not available in the dataset")

    try:
        predicted_price = predict_price(MODEL, payload, HISTORICAL_DATA)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="Prediction failed")

    return {"predicted_price": predicted_price}
