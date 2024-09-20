import yfinance as yf
from sklearn.model_selection import train_test_split
import pandas as pd
from utils.feature_engineering import add_technical_indicators
import numpy as np
from sklearn.preprocessing import MinMaxScaler

ticker = "ITC"
#ticker = input("Please Enter the name of company: ")
stock_data = yf.download(ticker, start="2014-01-01", end="2024-01-01", interval='1d')
stock_data.to_csv('data/store_stock_data.csv')

def prepare_data_for_lstm(file_path, sequence_length=50):
    # Load data

    data = pd.read_csv(file_path)
    data = add_technical_indicators(data)

    # Normalize features
    scaler = MinMaxScaler()
    data[['RSI', 'SMA_20', 'SMA_50', 'EMA_20', 'EMA_50', 'Upper_BB', 'Lower_BB', 'Close']] = \
        scaler.fit_transform(data[['RSI', 'SMA_20', 'SMA_50', 'EMA_20', 'EMA_50', 'Upper_BB', 'Lower_BB', 'Close']])

    # Convert data to sequences
    def create_sequences(data, seq_length):
        sequences = []
        labels = []
        for i in range(len(data) - seq_length):
            seq = data.iloc[i:i + seq_length][
                ['RSI', 'SMA_20', 'SMA_50', 'EMA_20', 'EMA_50', 'Upper_BB', 'Lower_BB', 'Close']].values
            label = (data.iloc[i + seq_length]['Close'] > data.iloc[i + seq_length - 1][
                'Close'])  # Binary classification
            sequences.append(seq)
            labels.append(label)
        return np.array(sequences), np.array(labels)

    # Prepare sequences
    sequences, labels = create_sequences(data, sequence_length)

    # Split into training and test sets
    split = int(len(sequences) * 0.8)
    X_train, X_test = sequences[:split], sequences[split:]
    y_train, y_test = labels[:split], labels[split:]

    return X_train, X_test, y_train, y_test, scaler


stock_data.ffill(inplace=True)


stock_data.dropna(inplace=True)

