import yfinance as yf
import pandas as pd
import schedule
import time


def download_stock_data():
    ticker = "AAPL"

    # Download data from a specific start date up to the latest available data (real-time)
    stock_data = yf.download(ticker, start="2020-01-01", interval='1d')
    # Fill missing values with the previous row’s value (forward fill)
    stock_data.ffill(inplace=True)

    # Drop rows with missing values
    stock_data.dropna(inplace=True)

    # Save the data to a CSV file, overwriting the file if it exists
    stock_data.to_csv('store_stock_data.csv', mode='w')


# Schedule the job to run every day at 9:00 AM
#schedule.every().day.at("09:00").do(download_stock_data)
#schedule.every().hour.do(download_stock_data)
schedule.every(1).minute.do(download_stock_data)

# Keep the script running to check if it's time to run the job
while True:
    schedule.run_pending()
    time.sleep(1)

