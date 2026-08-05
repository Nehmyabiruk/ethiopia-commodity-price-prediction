import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

def load_data(path):
        df = pd.read_csv(path)
        print(df.shape)
        print(df.columns.tolist())
        print(df.info())
        

        return df


        

def clean_data(df):
    dfcombined=df.drop_duplicates()
    # 4. Sort by date and market for cleanliness
    dfcombined = dfcombined.sort_values(['period_date', 'market', 'product']).reset_index(drop=True)
    # 5. Final check
    print("Combined shape:", dfcombined.shape)
    print("\nProduct counts:")
    print(dfcombined['product'].value_counts())
    print("\nDate range:", dfcombined['period_date'].min(), "→", dfcombined['period_date'].max())
    print("\nMissing values:")
    print(dfcombined.isnull().sum())
    print("\nUnique markets:", dfcombined['market'].nunique())

    return dfcombined


def merge_data(df1, df2):
    common_columns = ['country', 'admin_1', 'market', 'latitude', 'longitude',
    'period_date', 'currency', 'product', 'value'
     ]
    df1=df1[common_columns]
    df2=df2[common_columns]
    dfcombined=pd.concat([df1, df2], ignore_index=True)
    
    return dfcombined

def save_data(dfcombined, path):
    dfcombined.to_csv(path, index=False)
    print("Saved cleaned data to:", path)   

    return dfcombined

def main():    
    df1=load_data(("../data/processed/fews_net_CLEANED.csv"))
    df2=load_data(("../data/processed/ETH_RTFP_cleaned_2007_2026-07-06.csv"))
    dfcombined=merge_data(df1, df2)
    dfcombined = clean_data(dfcombined)
    save_data(dfcombined, "../data/processed/combined_data.csv")

if __name__ == "__main__":
    main()       