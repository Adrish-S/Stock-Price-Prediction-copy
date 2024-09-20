# utils/feature_engineering.py
from utils.rsi_calculation import calculate_rsi

def add_technical_indicators(df):
    # Add Simple Moving Averages (SMA)
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()

    # Add Exponential Moving Averages (EMA)
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()

    # Add Bollinger Bands
    df['stddev'] = df['Close'].rolling(window=20).std()
    df['Upper_BB'] = df['SMA_20'] + (2 * df['stddev'])
    df['Lower_BB'] = df['SMA_20'] - (2 * df['stddev'])

    # Add RSI
    df['RSI'] = calculate_rsi(df)

    # Fill NaN values (from moving averages, etc.)
    df.bfill(inplace=True)
    return df
