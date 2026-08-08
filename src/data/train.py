from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
from xgboost import XGBRegressor

from src.data.evaluate import save_results, evaluate_predictions, plot_predictions
from src.data.feature_engineering import (
    add_lag_and_rolling_features,
    add_time_features,
    load_data,
    prepare_training_data,
)
from src.data.utils import (
    DEFAULT_DATA_PATH,
    DEFAULT_MODEL_PATH,
    DEFAULT_RESULTS_PATH,
    DEFAULT_PLOT_PATH,
)
import joblib


def build_preprocessor(categorical_features):
    return ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_features,
            )
        ],
        remainder="passthrough",
    )


def build_search_model(random_state: int = 42):
    xgb_model = XGBRegressor(random_state=random_state, verbosity=0)
    param_dist = {
        "n_estimators": [100, 200, 300, 400, 500],
        "max_depth": [3, 5, 6, 8, 10],
        "learning_rate": [0.01, 0.02, 0.05, 0.1, 0.2],
        "subsample": [0.6, 0.8, 1.0],
        "colsample_bytree": [0.6, 0.8, 1.0],
    }
    return RandomizedSearchCV(
        estimator=xgb_model,
        param_distributions=param_dist,
        n_iter=20,
        cv=TimeSeriesSplit(n_splits=5),
        scoring="neg_mean_squared_error",
        n_jobs=-1,
        random_state=random_state,
        verbose=1,
    )


def build_pipeline(preprocessor, model):
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def save_model(pipeline, model_path: Path):
    joblib.dump(pipeline, model_path)
    return model_path


def train_model(data_path: Path = DEFAULT_DATA_PATH, split_date: str = "2025-01-01"):
    df = load_data(data_path)
    df = add_time_features(df)
    df = add_lag_and_rolling_features(df)

    X, y = prepare_training_data(df)
    categorical_features = ["country", "admin_1", "market", "currency", "product"]
    numerical_features = [col for col in X.columns if col not in categorical_features]

    preprocessor = build_preprocessor(categorical_features)
    search = build_search_model()
    search.fit(preprocessor.fit_transform(X), y)

    model = search.best_estimator_
    pipeline = build_pipeline(preprocessor, model)

    train_df = df[df["period_date"] < split_date]
    test_df = df[df["period_date"] >= split_date]

    X_train = train_df.drop(columns=["value", "period_date"])
    y_train = train_df["value"]
    X_test = test_df.drop(columns=["value", "period_date"])
    y_test = test_df["value"]

    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    metrics = evaluate_predictions(y_test, predictions)
    save_model(pipeline, DEFAULT_MODEL_PATH)
    save_results(y_test, predictions, DEFAULT_RESULTS_PATH)
    plot_predictions(y_test, predictions, DEFAULT_PLOT_PATH)

    return {
        "best_params": search.best_params_,
        "metrics": metrics,
        "model_path": DEFAULT_MODEL_PATH,
        "results_path": DEFAULT_RESULTS_PATH,
        "plot_path": DEFAULT_PLOT_PATH,
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Train the commodity price prediction model.")
    parser.add_argument(
        "--data-path",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to the processed CSV file.",
    )
    parser.add_argument(
        "--split-date",
        type=str,
        default="2025-01-01",
        help="Date used to split the time series data.",
    )
    args = parser.parse_args()

    report = train_model(data_path=args.data_path, split_date=args.split_date)
    print("Training complete")
    print(f"Best params: {report['best_params']}")
    print("Metrics:")
    for name, value in report["metrics"].items():
        print(f"  {name}: {value:.4f}")
    print(f"Model saved to: {report['model_path']}")
    print(f"Results saved to: {report['results_path']}")
    print(f"Plot saved to: {report['plot_path']}")


if __name__ == "__main__":
    main()
