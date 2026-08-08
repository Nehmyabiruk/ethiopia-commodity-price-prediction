from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "combined_data.csv"
DEFAULT_MODEL_PATH = PROJECT_ROOT / "commodity_price_forecasting_pipeline.pkl"
DEFAULT_RESULTS_PATH = PROJECT_ROOT / "prediction_results.csv"
DEFAULT_PLOT_PATH = PROJECT_ROOT / "prediction_plot.png"

MODEL_FEATURES = [
    "country",
    "admin_1",
    "market",
    "latitude",
    "longitude",
    "currency",
    "product",
    "year",
    "month",
    "quarter",
    "lag1",
    "lag3",
    "lag6",
    "lag12",
    "rolling_3",
    "rolling_6",
    "rolling_12",
    "price_change_1",
    "price_change_3",
    "price_change_12",
]

NUMERIC_FEATURES = [
    "latitude",
    "longitude",
    "year",
    "month",
    "quarter",
    "lag1",
    "lag3",
    "lag6",
    "lag12",
    "rolling_3",
    "rolling_6",
    "rolling_12",
    "price_change_1",
    "price_change_3",
    "price_change_12",
]

PREDICTION_INPUT_FIELDS = [
    "country",
    "admin_1",
    "market",
    "currency",
    "product",
    "year",
    "month",
]
