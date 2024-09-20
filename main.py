# main.py

from models.model_training import train_model
from backtest.strategy_backtest import run_backtest
import yfinance as yf

def main():
    ticker = "ITC"
    # ticker = input("Please Enter the name of company: ")
    stock_data = yf.download(ticker, start="2014-01-01", end="2024-01-01", interval='1d')
    stock_data.to_csv('data/store_stock_data.csv')
    # Train model
    train_model()

    # Run backtest and plot results
    run_backtest()

if __name__ == "__main__":
    main()
