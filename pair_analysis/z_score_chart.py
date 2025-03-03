import ccxt
import pair_analysis.main_key as k
import pandas as pd
import matplotlib.pyplot as plt
from pykalman import KalmanFilter


import numpy as np

# Initialize Phemex with API keys
phemex = ccxt.phemex({
    'apiKey': k.key,
    'secret': k.secret,
    'enableRateLimit': True
})

# Parameters
timeframe = '1d' # Interval
limit = 600  # Number of data points to fetch
Z_score = 2 # Set Z score Threshold 
hedge = 583.537883639752

# Symbols
asset1 = 'NEOUSDT'
asset2 = 'ZILUSDT'

def fetch_data(symbol, timeframe, limit):
    since = phemex.milliseconds() - (limit * 24 * 60 * 60 * 1000)
    ohlcv = phemex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

df1 = fetch_data(asset1, timeframe, limit)
df2 = fetch_data(asset2, timeframe, limit)

# Ensure timestamps match
df1, df2 = df1.align(df2, join='inner')
# Define hedge ratio (β)
hedge_ratio = hedge

# Calculate Spread (Default: Asset1 / Asset2)
df1['spread_default'] = df1['close'] - (hedge_ratio * df2['close'])

# # Calculate Spread (Default: Asset1 / Asset2)
# df1['spread_default'] = df1['close'] / df2['close']


# Calculate Z-score
df1['z_score'] = (df1['spread_default'] - df1['spread_default'].rolling(21).mean()) / df1['spread_default'].rolling(21).std()
# df1['z_score'] = (df1['spread_default'] - df1['spread_default'].mean()) / df1['spread_default'].std()

# --- Calculate the Stochastic Oscillator on the Spread ---
# Parameters for the stochastic indicator
k_window = 5  # Lookback period for %K calculation
d_window = 3  # Smoothing period for %D calculation

# Calculate the rolling lowest and highest spread values
df1['lowest_spread'] = df1['spread_default'].rolling(window=k_window).min()
df1['highest_spread'] = df1['spread_default'].rolling(window=k_window).max()

# Compute %K. Multiply by 100 to get percentage values.
df1['%K'] = 100 * (df1['spread_default'] - df1['lowest_spread']) / (df1['highest_spread'] - df1['lowest_spread'])

# Compute %D as the moving average of %K
df1['%D'] = df1['%K'].rolling(window=d_window).mean()



# Normalize closing prices
norm_close1 = (df1['close'] - df1['close'].min()) / (df1['close'].max() - df1['close'].min()) * 100
norm_close2 = (df2['close'] - df2['close'].min()) / (df2['close'].max() - df2['close'].min()) * 100

# Plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

# First chart: Prices & Z-Score
ax1.plot(df1.index, norm_close1, label=f'{asset1}', color='green')
ax1.plot(df1.index, norm_close2, label=f'{asset2}', color='purple')
ax1.set_ylabel('Normalized Prices')
ax1.set_title(f'Prices & Z-Score: {asset1} / {asset2} (Last Z-Score: {df1["z_score"].iloc[-1]:.2f})')
ax1.legend()
ax1.grid(True)
ax1_twin = ax1.twinx()
ax1_twin.plot(df1.index, df1['z_score'], label='ZS', color='red', linestyle='dashed')
ax1_twin.axhline(y=0, color='black', linestyle='solid', linewidth=1)
ax1_twin.set_ylabel('Z-Score')
ax1_twin.legend(loc='upper left')

# Second chart: Dynamic Spread
ax2.plot(df1.index, df1['spread_default'], label='Spread', color='blue')
ax2.set_ylabel('Spread')
ax2.set_title(f'Dynamic Spread ({df1["spread_default"].iloc[-1]:.6f})')
ax2.legend()
ax2.grid(True)

# Third chart: Stochastic Oscillator
# ax3.plot(df1.index, df1['%K'], label='%K', color='blue')
ax3.plot(df1.index, df1['%D'], label='%D', color='red')
ax3.axhline(80, color='blue', linestyle='dashed', linewidth=2)
ax3.axhline(20, color='blue', linestyle='dashed', linewidth=2)
ax3.set_ylabel('Stochastic %K & %D')
ax3.set_title('Stochastic Oscillator on Spread')
ax3.legend()
ax3.grid(True)

plt.xlabel('Time')
plt.tight_layout()
plt.show()
