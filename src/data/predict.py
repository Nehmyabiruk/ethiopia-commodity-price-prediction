from pathlib import Path

import joblib

from src.data.feature_engineering import build_prediction_input, load_data
from src.data.utils import DEFAULT_MODEL_PATH


def load_pipeline(model_path: Path = DEFAULT_MODEL_PATH):
    return joblib.load(model_path)


def predict_price(pipeline, payload: dict, historical_df=None) -> float:
    if historical_df is None:
        historical_df = load_data()
    input_df = build_prediction_input(payload, historical_df)
    prediction = pipeline.predict(input_df)
    return float(prediction[0])
