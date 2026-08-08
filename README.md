# Ethiopia Commodity Price Prediction

An ML-powered web application for predicting commodity prices in Ethiopian markets using historical market data, time-series features, and XGBoost.

## 🚀 Live Demo

[**Open Ethiopia Commodity Price Predictor →**](https://ethiopia-commodity-price-prediction.onrender.com/)

## Features

* Ethiopian commodity price prediction
* Market and product selection
* Time-series feature engineering
* Automatic lag feature generation
* Rolling price statistics
* Price-change features
* XGBoost machine learning model
* FastAPI prediction API
* Single-page frontend interface
* Live deployment on Render

## Overview

This project predicts commodity prices in Ethiopian markets using historical market data and machine learning.

The system uses historical prices to generate time-series features such as:

* Lag 1, 3, 6, and 12 months
* Rolling 3, 6, and 12 month averages
* Price changes over different time periods
* Calendar features such as year, month, and quarter
* Market and geographic information

The trained XGBoost model is exposed through a FastAPI backend and connected to a simple web-based frontend.

## Project Architecture

```text
User
 │
 ▼
Frontend
 │
 │ Prediction Request
 ▼
FastAPI API
 │
 ├── Feature Engineering
 ├── Historical Market Data
 └── XGBoost Model
 │
 ▼
Predicted Commodity Price
 │
 ▼
Frontend
```

The application is deployed as a Python web service on Render.

## Repository Structure

```text
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
├── requirements.txt
└── README.md
```

## Setup

Clone the repository:

```powershell
git clone https://github.com/Nehmyabiruk/ethiopia-commodity-price-prediction.git
cd ethiopia-commodity-price-prediction
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Make sure the processed dataset exists at:

```text
data/processed/combined_data.csv
```

## Training

Train the model with:

```powershell
python -m src.data.train
```

The training process:

* loads the processed market data
* performs feature engineering
* creates time-series and lag features
* uses TimeSeriesSplit for time-aware validation
* performs model training and hyperparameter tuning
* fits the preprocessing and XGBoost pipeline
* saves the trained model
* generates prediction results
* exports evaluation plots

## API

Start the FastAPI service locally:

```powershell
uvicorn src.app:app --reload
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Frontend

The frontend is served by the FastAPI application.

Users can select:

* Country
* Administrative region
* Market
* Product
* Year
* Month

The application then sends the prediction request to the FastAPI backend and displays the predicted commodity price.

Time-series features such as lag values, rolling averages, and price changes are handled by the backend rather than requiring the user to enter them manually.

## Deployment

The application is deployed on **Render** as a Python web service.

### Render Start Command

```bash
uvicorn src.app:app --host 0.0.0.0 --port $PORT
```

The application does not require a database for the current version.

The trained model and required historical data are packaged with the application and loaded by the FastAPI service.

## Requirements

The main dependencies are listed in `requirements.txt`, including:

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* FastAPI
* Uvicorn
* Joblib

## Notes

* The model must be trained before using the prediction API if the trained model is not already included.
* Historical data is used to generate time-series features required by the prediction model.
* The application currently does not store user predictions in a database.
* Render's free service may spin down after periods of inactivity, so the first request after inactivity may take longer.

## Future Improvements

* Add more Ethiopian commodities and markets
* Incorporate weather and seasonal information
* Add real-time market data updates
* Add prediction history
* Add price trend visualization
* Add confidence intervals for predictions
* Improve model performance with additional forecasting approaches
* Add a database for storing predictions and market updates

## Author

**Nehmya Biruk**

GitHub: [@Nehmyabiruk](https://github.com/Nehmyabiruk/)
