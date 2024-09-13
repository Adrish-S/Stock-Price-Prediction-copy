import yfinance as yf

# Download historical data for a specific stock (e.g., AAPL)
ticker = "AAPL"
#ticker = input("Please Enter the name of company: ")
stock_data = yf.download(ticker, start="2020-01-01", end="2023-01-01", interval='1d')
# Fill missing values with the previous row’s value (forward fill)
stock_data.ffill(inplace=True)

# Drop rows with missing values
stock_data.dropna(inplace=True)

stock_data.to_csv('store_stock_data.csv', mode='w')
# Create a simple moving average (SMA)
stock_data['SMA_20'] = stock_data['Close'].rolling(window=20).mean()

# Calculate RSI (Relative Strength Index)
def RSI(series, period=14):
    delta = series.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

stock_data['RSI'] = RSI(stock_data['Close'])
print(stock_data.head(30))
stock_data.ffill(inplace=True)

# Drop rows with missing values
stock_data.dropna(inplace=True)

stock_data.to_csv('store_stock_data.csv', mode='w')

