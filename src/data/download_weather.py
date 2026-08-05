import os
import time
import glob

import pandas as pd
import requests


def get_nasa_monthly(lat, lon, start_year=2008, end_year=2025):
    url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
    params = {
        "parameters": "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_year,
        "end": end_year,
        "format": "JSON",
    }

    try:
        response = requests.get(url, params=params, timeout=90)

        if response.status_code != 200:
            print(f"  Failed with status {response.status_code}")
            return None

        data = response.json()
        parameters = data["properties"]["parameter"]

        df = pd.DataFrame(parameters)
        df = df.reset_index().rename(columns={"index": "year_month"})

        df["year_month"] = df["year_month"].astype(str).str[:6]
        df["period_date"] = pd.to_datetime(df["year_month"], format="%Y%m", errors="coerce")
        df = df.dropna(subset=["period_date"])

        df["latitude"] = lat
        df["longitude"] = lon

        df = df.rename(columns={
            "T2M": "temp_mean",
            "T2M_MAX": "temp_max",
            "T2M_MIN": "temp_min",
            "PRECTOTCORR": "precipitation",
            "RH2M": "humidity",
        })

        return df[["period_date", "latitude", "longitude", "temp_mean", "temp_max", "temp_min", "precipitation", "humidity"]]
    except Exception as e:
        print(f"  Error: {e}")
        return None


def main():
    df_combined = pd.read_csv('../data/processed/combined_data.csv', parse_dates=['period_date'])
    locations = df_combined[['market', 'latitude', 'longitude']].drop_duplicates().reset_index(drop=True)

    os.makedirs("data/external/nasa_weather_long", exist_ok=True)

    existing = glob.glob("data/external/nasa_weather_long/*.csv")
    already_done = {os.path.basename(f).replace(".csv", "") for f in existing}


    all_weather = []
    failed = []

    for idx, row in locations.iterrows():
        market = row["market"]
        safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in market)

        if safe_name in already_done:
            print(f"Skipping {market}")
            continue
        print(f"Downloading {idx+1}/{len(locations)}: {market}")

        weather = get_nasa_monthly(row["latitude"], row["longitude"], start_year=2008, end_year=2025)

        out_path = os.path.join("data/external/nasa_weather_long", f"{safe_name}.csv")
        if weather is not None:
                weather["market"] = market
                all_weather.append(weather)
                weather.to_csv(out_path, index=False)
                weather.to_csv(f"data/external/nasa_weather_long/{safe_name}.csv", index=False)
                print("  → Saved")
        else:
                failed.append(market)
                print("  → Failed")
            
        time.sleep(1.0)

       
        
        

    all_files = glob.glob("data/external/nasa_weather_long/*.csv")
    if not all_files:
        return

    df_list = [pd.read_csv(f, parse_dates=["period_date"]) for f in all_files]
    df_weather = pd.concat(df_list, ignore_index=True)

    df_weather.to_csv("data/external/ethiopia_nasa_monthly_weather_2008_2025_full.csv", index=False)


if __name__ == "__main__":
    main()