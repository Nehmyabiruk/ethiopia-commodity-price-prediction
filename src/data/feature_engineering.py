from pathlib import Path

import pandas as pd

from src.data.utils import DEFAULT_DATA_PATH, MODEL_FEATURES, NUMERIC_FEATURES


def load_data(data_path: Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(data_path)
    df["period_date"] = pd.to_datetime(df["period_date"])
    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["market", "product", "period_date"]).reset_index(drop=True)
    df["year"] = df["period_date"].dt.year
    df["month"] = df["period_date"].dt.month
    df["quarter"] = df["period_date"].dt.quarter
    return df


def add_lag_and_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    df["lag1"] = df.groupby(["market", "product"])["value"].shift(1)
    df["lag3"] = df.groupby(["market", "product"])["value"].shift(3)
    df["lag6"] = df.groupby(["market", "product"])["value"].shift(6)
    df["lag12"] = df.groupby(["market", "product"])["value"].shift(12)

    df["rolling_3"] = (
        df.groupby(["market", "product"])["value"]
          .transform(lambda x: x.shift(1).rolling(3).mean())
    )
    df["rolling_6"] = (
        df.groupby(["market", "product"])["value"]
          .transform(lambda x: x.shift(1).rolling(6).mean())
    )
    df["rolling_12"] = (
        df.groupby(["market", "product"])["value"]
          .transform(lambda x: x.shift(1).rolling(12).mean())
    )
    return df


def prepare_training_data(df: pd.DataFrame):
    df = df.dropna().reset_index(drop=True)
    df = df.sort_values("period_date").reset_index(drop=True)
    X = df.drop(columns=["value", "period_date"])
    y = df["value"]
    return X, y


def build_prediction_input(payload: dict, historical_df: pd.DataFrame) -> pd.DataFrame:
    required = ["country", "admin_1", "market", "currency", "product", "year", "month"]
    missing_fields = [field for field in required if field not in payload]
    if missing_fields:
        raise ValueError(f"Missing fields for prediction: {', '.join(missing_fields)}")

    country = str(payload["country"]).strip()
    admin_1 = str(payload["admin_1"]).strip()
    market = str(payload["market"]).strip()
    currency = str(payload["currency"]).strip()
    product = str(payload["product"]).strip()
    year = int(payload["year"])
    month = int(payload["month"])

    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")

    quarter = (month - 1) // 3 + 1
    target_date = pd.Timestamp(year=year, month=month, day=1)

    hist = historical_df.copy()
    hist = hist[hist["period_date"] < target_date]
    mask = (
        hist["country"].astype(str).str.lower() == country.lower()
    ) & (
        hist["admin_1"].astype(str).str.lower() == admin_1.lower()
    ) & (
        hist["market"].astype(str).str.lower() == market.lower()
    ) & (
        hist["currency"].astype(str).str.lower() == currency.lower()
    ) & (
        hist["product"].astype(str).str.lower() == product.lower()
    )
    hist = hist.loc[mask].sort_values("period_date").reset_index(drop=True)

    if hist.empty:
        raise ValueError("No historical data found for the requested market/product combination.")
    if len(hist) < 12:
        raise ValueError("At least 12 months of history are required to compute prediction features.")

    values = hist["value"].astype(float).tolist()
    latest_row = hist.iloc[-1]
    latitude = float(latest_row["latitude"])
    longitude = float(latest_row["longitude"])

    price_change_1 = (values[-1] - values[-2]) / float(values[-2]) if len(values) >= 2 and values[-2] != 0 else 0.0
    price_change_3 = (values[-1] - values[-4]) / float(values[-4]) if len(values) >= 4 and values[-4] != 0 else 0.0
    price_change_12 = (values[-1] - values[-13]) / float(values[-13]) if len(values) >= 13 and values[-13] != 0 else 0.0

    row = {
        "country": country,
        "admin_1": admin_1,
        "market": market,
        "latitude": latitude,
        "longitude": longitude,
        "currency": currency,
        "product": product,
        "year": year,
        "month": month,
        "quarter": quarter,
        "lag1": float(values[-1]),
        "lag3": float(values[-3]),
        "lag6": float(values[-6]),
        "lag12": float(values[-12]),
        "rolling_3": float(sum(values[-3:]) / 3.0),
        "rolling_6": float(sum(values[-6:]) / 6.0),
        "rolling_12": float(sum(values[-12:]) / 12.0),
        "price_change_1": float(price_change_1),
        "price_change_3": float(price_change_3),
        "price_change_12": float(price_change_12),
    }

    return pd.DataFrame([{feature: row[feature] for feature in MODEL_FEATURES}])
