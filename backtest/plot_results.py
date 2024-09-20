# backtest/plot_results.py

import matplotlib.pyplot as plt

def plot_strategy(data):
    plt.figure(figsize=(14, 8))
    plt.plot(data.index, data['Close'].pct_change().cumsum(), label='Market Returns')
    plt.plot(data.index, data['Cumulative_Strategy_Returns'], label='Strategy Returns (ML)')
    plt.title('Machine Learning-Enhanced Trading Strategy')
    plt.legend()
    plt.show()
