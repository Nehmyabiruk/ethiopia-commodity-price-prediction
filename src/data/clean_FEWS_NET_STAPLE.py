import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import os


def load_data(path):
        df = pd.read_csv(path)
        print(df.shape)
        print(df.columns.tolist())
        print(df.info())
        print(df.isnull().sum())

        return df   

def clean_data(df):
    df2=df.copy()
    df2=df2.drop(columns=['Unnamed: 15'])
    cols_to_keep = ['country', 'admin_1', 'market', 'latitude', 'longitude',
    'period_date', 'currency', 'product', 'value',
    'unit', 'price_type']
    df2 =df2[cols_to_keep]
    df2=df2.dropna(subset=['value'])
    products_to_keep = ['Goats (Local Quality)','Maize Grain (White)','Mixed Teff',  'Sorghum (Red)','Sorghum (White)','Sorghum (Yellow)','Wheat Flour',
    'Wheat Grain']
    df2 = df2[df2['product'].isin(products_to_keep)]
    product_map={
    'Goats (Local Quality)': 'livestock_goat',
    'Maize Grain (White)': 'maize',
    'Mixed Teff': 'teff',
    'Sorghum (Red)': 'sorghum',
    'Sorghum (White)': 'sorghum',
    'Sorghum (Yellow)': 'sorghum',
    'Wheat Flour': 'wheat',
    'Wheat Grain': 'wheat'}
    df2['product'] = df2['product'].replace(product_map)
    print(df2.columns.tolist())
    print('shape of df2')
    print(df2.shape)
    print('value count')
  
    print("is it null??????")
    print(df2.isnull().sum())
    print(df2.columns.tolist())
    df2=df2.drop(columns=['unit', 'price_type'])

    return df2

def save_data(df, path):
    df.to_csv(path, index=False)
    print(df.columns.tolist())
    print("Saved cleaned data to:", path)    





def main():
    df = load_data("../data/raw/fews_net_staple_food_price_data_ethiopia_hdx.csv")
    df_clean = clean_data(df)
    save_data(df_clean, "../data/processed/fews_net_CLEANED.csv")


if __name__ == "__main__":
    main()    
     

