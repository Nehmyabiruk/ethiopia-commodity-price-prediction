import pandas as pd



def main():

    # 2. Force convert period_date to datetime in BOTH dataframes
   
    df_price = pd.read_csv("../data/processed/ethiopia_commodity_prices_clean.csv", parse_dates=["period_date"])
    df_weather = pd.read_csv("../data/external/ethiopia_nasa_monthly_weather_2008_2025_full.csv", parse_dates=["period_date"])
    
    df_price["period_date"] = df_price["period_date"].dt.to_period("M").dt.to_timestamp()
    df_weather["period_date"] = df_weather["period_date"].dt.to_period("M").dt.to_timestamp()

    df_price["period_date"] = pd.to_datetime(df_price["period_date"], errors="coerce")
    df_weather["period_date"] = pd.to_datetime(df_weather["period_date"], errors="coerce")

    df_merged = pd.merge(
        df_price,
        df_weather,
        on=["market", "period_date"],
        how="left"
    )

    print("\nMerged shape:", df_merged.shape)
    print("Rows with weather:", df_merged["temp_mean"].notna().sum())
    print("Rows without weather:", df_merged["temp_mean"].isna().sum())

    # Clean column names (remove _x / _y if they appear)
    df_merged = df_merged.rename(columns={
        "latitude_x": "latitude",
        "longitude_x": "longitude"
    })

    df_merged = df_merged.drop(columns=["latitude_y", "longitude_y"], errors="ignore")

    print("\nFinal columns:")
    print(df_merged.columns.tolist())
    df_merged = df_merged.drop(columns=["latitude_y", "longitude_y"], errors="ignore")

    df_final = df_merged.dropna(subset=["temp_mean"]).copy()

    df_final.to_csv("../data/processed/ethiopia_commodity_prices_with_weather_clean.csv", index=False)
    print("\nClean dataset saved successfully!")