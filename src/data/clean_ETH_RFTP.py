import pandas as pd 

import os

def load_data(path):
    df = pd.read_csv(path)
    print(df.isnull().sum())
    print(df.columns.tolist())
    print(df[['maize', 'sorghum', 'teff_fao', 'wheat', 'livestock_goat']].isnull().sum())
    return df

def clean_data(df):
    cols_to_keep=  ['country','adm1_name','mkt_name', 'lat', 'lon',
        'price_date', 'currency',
        'maize', 'sorghum', 'teff_fao', 'wheat', 'livestock_goat'
    ]
    df1=df[cols_to_keep].copy()
    df1_long=df1.melt(id_vars=['country','adm1_name','mkt_name', 'lat', 'lon', 'price_date', 'currency'],
                      value_vars=['maize', 'sorghum', 'teff_fao', 'wheat', 'livestock_goat'],
                      var_name='product', value_name='value') 
        
    df1_long['product']=df1_long['product'].replace({ 'teff_fao': 'teff' })
    df1_long=df1_long.dropna(subset=['value'])
        # Rename columns so they match Dataset 2
    df1_long = df1_long.rename(columns={
        'adm1_name': 'admin_1',
        'mkt_name': 'market',
        'lat': 'latitude',
        'lon': 'longitude',
        'price_date': 'period_date'
         })
    print("shape")
    print(df1_long.shape)
    print("their info")
    print(df1_long.info())
    
        
    print("is it null")
    print(df1_long.isnull().sum())
    print(df1_long.head(5))
    
        # Remove the fake "Market Average" rows
    df1_long = df1_long[df1_long['market'] != 'Market Average']
    print("Shape after removing Market Average:", df1_long.shape)
    print("\nMissing values:")
    print(df1_long.isnull().sum())
    print("\nDuplicates:", df1_long.duplicated().sum())
    print("\nUnique markets:", df1_long['market'].nunique())
    os.makedirs("../data/processed", exist_ok=True)
    return df1_long

def save_data(df, path):
    df.to_csv(path, index=False)
    print(df.columns.tolist())
    

def main():
    df = load_data("../data/raw/ETH_RTFP_mkt_2007_2026-07-06.csv")
    df_clean = clean_data(df)
    save_data(df_clean, "../data/processed/ETH_RTFP_cleaned_2007_2026-07-06.csv")
    
    
if __name__ == "__main__":
    main()