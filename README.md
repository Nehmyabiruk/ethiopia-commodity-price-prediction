# Ethiopia Commodity Price Prediction

An ML-powered web application for predicting commodity prices in Ethiopian markets using historical market data, lag features, rolling statistics, and XGBoost.

## 🚀 Live Demo

[**Open Ethiopia Commodity Price Predictor →**](https://ethiopia-commodity-price-prediction.onrender.com/)

## Features

- Ethiopian market commodity price prediction
- Market and product selection
- Automatic lag feature generation
- Rolling price statistics
- XGBoost prediction model
- FastAPI backend
- Live deployment on Render

## Overview

This repository predicts Ethiopian commodity prices using a machine learning pipeline and provides a prediction API with a simple frontend.

It includes:
- feature engineering for time-series and lag features
- XGBoost model training
- evaluation metrics and plot export
- FastAPI prediction service
- single-page frontend UI
- Docker deployment support

## Repository Structure

```
commodity-predict/
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── notebooks/
├── src/
│   ├── app.py
│   ├── static/
│   │   └── index.html
│   └── data/
│       ├── __init__.py
│       ├── eda.py
│       ├── evaluate.py
│       ├── feature_engineering.py
│       ├── predict.py
│       ├── train.py
│       └── utils.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Setup

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Make sure the processed dataset exists at:

- `data/processed/combined_data.csv`

## Training

Train the model with:

```powershell
python -m src.data.train
```

This will:
- load processed training data
- engineer features
- perform hyperparameter search with TimeSeriesSplit
- fit a pipeline that includes preprocessing
- save the model to `commodity_price_forecasting_pipeline.pkl`
- save predictions to `prediction_results.csv`
- save a plot to `prediction_plot.png`

## API

Start the FastAPI service:

```powershell
uvicorn src.app:app --reload
```

Open in the browser:

- `http://127.0.0.1:8000/` — frontend form
- `http://127.0.0.1:8000/docs` — Swagger UI

## Frontend

The page at `src/static/index.html` lets you enter model features and returns a predicted price.

## Docker

Build and run the container:

```powershell
docker build -t commodity-predict .
docker run -p 8000:8000 commodity-predict
```

Or use docker-compose:

```powershell
docker-compose up --build
```

## Requirements

Dependencies are in `requirements.txt`.

## Notes

- Run training before using the API so `commodity_price_forecasting_pipeline.pkl` is available.
- If you prefer, you can use `python src\data\eda.py` to invoke training from the old entry point.

## Author

Nehmya Biruk