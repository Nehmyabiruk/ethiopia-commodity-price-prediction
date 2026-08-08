from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_predictions(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    r2 = r2_score(y_true, y_pred)
    return {
        "mae": mae,
        "rmse": rmse,
        "mape": mape,
        "r2": r2,
    }


def plot_predictions(y_true, y_pred, path: Path, n_points: int = 200):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(y_true.values[:n_points], label="Actual")
    ax.plot(y_pred[:n_points], label="Predicted")
    ax.set_title("Actual vs Predicted Prices")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Value")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


def save_results(y_true, y_pred, path: Path):
    results = pd.DataFrame({"Actual": y_true, "Predicted": y_pred})
    results.to_csv(path, index=False)
    return path
