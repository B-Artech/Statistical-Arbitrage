import ccxt
import pandas as pd
import numpy as np
import time
from datetime import datetime
import main_key as k

def fetch_data_safely(phemex, symbol, timeframe='1d', limit=400):
    try:
        since = phemex.milliseconds() - (limit * 24 * 60 * 60 * 1000)
        ohlcv = phemex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching {symbol}: {str(e)}")
        return None

class PairsTrader:
    def __init__(self, asset1, asset2, hedge_ratio):
        self.asset1 = asset1
        self.asset2 = asset2
        self.hedge_ratio = float(hedge_ratio)
        self.trades = []
        self.position = 0
        self.current_capital = 1  # Assuming initial capital is 1, or could be set as a parameter
    
    def backtest(self, df1, df2, zscore_threshold=1.5):
        df = pd.DataFrame(index=df1.index)
        df['spread'] = df1['close'] - (self.hedge_ratio * df2['close'])
        df['zscore'] = (df['spread'] - df['spread'].rolling(window=21).mean()) / df['spread'].rolling(window=21).std()
        df = df.dropna()
        
        for i in range(1, len(df)):
            zscore = df['zscore'].iloc[i]
            spread = df['spread'].iloc[i]
            
            if self.position == 0:
                # Entry conditions
                if zscore < -zscore_threshold:
                    self.position = 1
                    self.trades.append({'type': 'long', 'entry_price': spread})
                elif zscore > zscore_threshold:
                    self.position = -1
                    self.trades.append({'type': 'short', 'entry_price': spread})
            
            elif self.position != 0:
                # Exit conditions
                if (self.position == 1 and zscore >= 0) or (self.position == -1 and zscore <= 0):
                    exit_price = spread
                    if self.position == 1:
                        returns = (exit_price - self.trades[-1]['entry_price']) / self.trades[-1]['entry_price']
                    else:  # position == -1
                        returns = (self.trades[-1]['entry_price'] - exit_price) / self.trades[-1]['entry_price']
                    
                    self.current_capital *= (1 + returns)
                    self.trades[-1]['returns'] = returns
                    self.position = 0
            
            # Update equity after each iteration
            df.loc[df.index[i], 'equity'] = self.current_capital
        
        return df
    
    def get_win_rate(self):
        closed_trades = [t for t in self.trades if 'returns' in t]
        if not closed_trades:
            return 0
        wins = sum(1 for t in closed_trades if t['returns'] > 0)
        return wins / len(closed_trades)

def main():
    # Initialize exchange
    phemex = ccxt.phemex({
        'apiKey': k.key,
        'secret': k.secret,
        'enableRateLimit': True
    })

    # Load and filter pairs
    df = pd.read_csv('pairs_analysis_results.csv')
    df_filtered = df[
        (df['Cointegration P-Value'] < 0.02) & 
        (df['Half-Life'] < 25) &
        (df['Pearson'] > 0.90) &
        (df['Spearman'] > 0.90) 
    ]
    
    print(f"Testing {len(df_filtered)} pairs")
    results = []
    
    for _, row in df_filtered.iterrows():
        asset1, asset2 = row['Asset1'], row['Asset2']
        print(f"\nTesting {asset1}-{asset2}")
        
        # Fetch data
        df1 = fetch_data_safely(phemex, asset1)
        time.sleep(1)
        df2 = fetch_data_safely(phemex, asset2)
        time.sleep(1)
        
        if df1 is None or df2 is None:
            continue
            
        # Align data
        df1, df2 = df1.align(df2, join='inner')
        
        if len(df1) < 40:
            print("Insufficient data")
            continue
            
        # Run backtest
        trader = PairsTrader(asset1, asset2, row['Hedge Ratio'])
        trader.backtest(df1, df2)
        win_rate = trader.get_win_rate()
        
        print(f"Win rate: {win_rate:.2%}")
        
        if win_rate > 0.75:
            results.append([asset1, asset2, win_rate])
    
    if results:
        pd.DataFrame(results, columns=['Asset1', 'Asset2', 'Win Rate']).to_csv('high_winrate_pairs.csv', index=False)
        print(f"\nSaved {len(results)} pairs with >75% win rate")

if __name__ == "__main__":
    main()