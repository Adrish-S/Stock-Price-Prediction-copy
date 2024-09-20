# backtest/strategy_backtest.py

import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
from sklearn.metrics import accuracy_score, confusion_matrix
from data.datacollection import add_technical_indicators, prepare_data_for_lstm
from backtest.plot_results import plot_strategy


def run_backtest():
    # Load the trained LSTM model and scaler
    model = tf.keras.models.load_model('models/trained_lstm_model.h5')
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    # Load and prepare data
    data = pd.read_csv('data/store_stock_data.csv')
    data = add_technical_indicators(data)

    # Prepare data for prediction
    _, X_test, _, y_test, _ = prepare_data_for_lstm('data/store_stock_data.csv')

    # Generate predictions
    y_pred_prob = model.predict(X_test)
    y_pred = (y_pred_prob > 0.5).astype(int).flatten()

    # Calculate accuracy and confusion matrix
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    print(f"Backtest Model Accuracy: {accuracy:.2f}")
    print("Backtest Confusion Matrix:")
    print(conf_matrix)

    # Map predictions back to the original DataFrame
    data['Prediction'] = np.nan
    data.iloc[-len(y_pred):, data.columns.get_loc('Prediction')] = y_pred

    # Simulate buy/sell strategy based on model predictions and RSI
    data['Position'] = data['Prediction'].shift(1)  # Shift to simulate next day's trade
    data['Strategy_Return'] = data['Position'] * data['Close'].pct_change()
    data['Cumulative_Strategy_Returns'] = (1 + data['Strategy_Return']).cumprod()

    plot_strategy(data)
