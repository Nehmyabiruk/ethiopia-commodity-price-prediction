# Ethiopia Commodity Price Prediction

## Overview

This project aims to predict future commodity prices in Ethiopia using Machine Learning and historical market data.

The project focuses on essential Ethiopian commodities such as:

- Teff
- Maize
- Wheat
- Sorghum
- Livestock (Goat)

The goal is to build a forecasting system that can help understand price trends and support decision-making for farmers, businesses, and organizations.

---

## Project Objectives

- Collect and combine historical commodity price datasets.
- Clean and preprocess Ethiopian market data.
- Engineer time-series features.
- Train machine learning models for price prediction.
- Evaluate model performance.
- Deploy a prediction system.

---

## Dataset Sources

The project uses:

- Ethiopian market price data.
- FEWS NET staple food price data.

The raw datasets are not included in this repository because of their size.

---

## Project Structure
commodity-predict/

│
├── data/
│ ├── raw/
│ └── processed/
│
├── notebooks/
│
├── src/
│ ├── clean_rtfp.py
│ ├── clean_fews.py
│ ├── merge_data.py
│ ├── feature_engineering.py
│ ├── train.py
│ ├── evaluate.py
│ └── predict.py
│
├── models/
│
├── requirements.txt
│
└── README.md


---

## Data Processing Pipeline

The preprocessing pipeline contains:

1. Loading raw datasets.
2. Selecting required columns.
3. Reshaping data into a consistent format.
4. Removing missing values.
5. Removing duplicate records.
6. Combining multiple datasets.

---

## Machine Learning Workflow

The planned workflow:


Data Collection
|
↓
Data Cleaning
|
↓
Feature Engineering
|
↓
Model Training
|
↓
Model Evaluation
|
↓
Prediction


---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Jupyter Notebook
- Git

---

## Future Improvements


- Build time-series forecasting models.
- Create an API for predictions.
- Deploy the model.

---

## Author

Nehmya Biruk