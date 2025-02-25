import requests
import pandas as pd 
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json 
import time

load_dotenv()  # Load .env file


# _ _ _ CONFIGURATION _ _ _
FRED_API_KEY = os.getenv("FRED_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Define economic indicators to fetch from FRED
FRED_INDICATORS = {
    "GDP": "GDP",
    "Inflation": "CPIAUCSL",
    "Interest Rate": "FEDFUNDS"
}

# fUNCTION TO FETCH MACROECONOMIC DATA FROM FRED
def fetch_fred_data(series_id, start_date, end_date):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json&observation_start={start_date}&observation_end={end_date}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = json.loads(response.text)
            print(f"Fetched data for {series_id}: {data}")  # Debugging print
            
            # Ensure data contains "observations"
            if "observations" in data and isinstance(data["observations"], list):
                return {obs["date"]: obs["value"] for obs in data["observations"]}
            else:
                print(f"Unexpected response structure for {series_id}: {data}")
                return {}
        
        except Exception as e:
            print(f"Error parsing JSON for {series_id}: {e}")
            return {}
    else:
        print(f'error fetch {series_id}: {response.status_code}')
        return {}
    
# FUNCTION TO FETCH NEWS ARTICLES FROM NEWSAPI
def fetch_news_sentiment(date):
    url = f"https://newsapi.org/v2/everything?q=oil&from={date}&to={date}&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = json.loads(response.text)
        articles = data.get("articles", [])
        headlines = [article["title"] for article in articles]
        return headlines
    elif response.status_code == 429:
        print(f"Rate limit hit for {date}. Waiting before retrying...")
        time.sleep(5)  # Wait 5 seconds before retrying
        return fetch_news_sentiment(date)  # Retry after waiting
    else:
        print(f"Error fetching news for {date}: {response.status_code}")
        return []

# MAIN EXCUTION 
def main():
    # Load Brent oil data
    brent_data = pd.read_csv("C:\\Users\\Aman\\Desktop\\kifyaw10\\data\\BrentOilPrices.csv")
    brent_data['Date'] = pd.to_datetime(brent_data["Date"]).dt.date

    start_date = brent_data["Date"].min()
    end_date = brent_data['Date'].max()

    # #   featch macro economic data
    # macro_data = {}
    # for indicator, series_id in FRED_INDICATORS.items():
    #     macro_data[indicator] = fetch_fred_data(series_id, start_date, end_date)
    
    # fetch news sentiment
    news_data = {date: fetch_news_sentiment(date) for date in brent_data['Date'].astype(str)}

    # # Merge all data into brent oil dataset
    # for indicator in macro_data:
    #     brent_data[indicator] = brent_data['Date'].astype(str).map(macro_data[indicator])
    
    brent_data['News Headlines'] = brent_data['Date'].astype(str).map(news_data)

    # save final dataset
    brent_data.to_csv("brent_oil_enricled_2.csv", index= False)
    print ("Data collection complete. Output saved to brent_oil_enriched.csv")

if __name__ == "__main__":
    main()