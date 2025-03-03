import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from arch import arch_model  
import main_key as k

phemex = ccxt.phemex({
    'apiKey': k.key,
    'secret': k.secret,
    'enableRateLimit': True
})

# Function to fetch historical OHLCV data
def fetch_data(symbol, timeframe='1d', limit=600):
    since = phemex.milliseconds() - (limit * 24 * 60 * 60 * 1000)  # Fetch last 'limit' days
    ohlcv = phemex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
    
    # Convert to DataFrame
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    return df

# List of cryptocurrencies
cryptos = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"] # INDEX OUT OF LIST OF ASSETS
# cryptos = ["SOLUSDT"]

# Fetch data for each crypto
data = {crypto: fetch_data(crypto) for crypto in cryptos}

# Compute log returns
returns = {crypto: np.log(data[crypto]['close'] / data[crypto]['close'].shift(1)).dropna() for crypto in cryptos}

# Function to calculate GARCH volatility
def garch_volatility(log_returns):
    model = arch_model(log_returns, vol='GARCH', p=1, q=1)
    res = model.fit(disp="off")
    return res.conditional_volatility

# Compute GARCH volatility for each crypto
garch_vol = pd.DataFrame({crypto: garch_volatility(returns[crypto]) for crypto in cryptos})

# Annualize volatility
annual_garch_vol = garch_vol * np.sqrt(365)

# Compute the Volatility Index (equal-weighted)
volatility_index = annual_garch_vol.mean(axis=1)
average30_day = volatility_index.rolling(30).mean()
last = average30_day

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(volatility_index, label="Crypto Volatility Index (GARCH)", color='red', linewidth=2)
plt.plot(average30_day, label="Average", color='blue', linewidth=2)

# Formatting the date axis for better readability
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m'))  

plt.title(f"Crypto Volatility Index {cryptos}{volatility_index.iloc[-1]:.2} - GARCH Model  average30_day {last.iloc[-1]:.2}")
plt.xlabel("Date")
plt.ylabel("Volatility")
plt.legend()
plt.grid()
plt.show()
