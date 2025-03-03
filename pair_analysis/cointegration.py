import ccxt
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint
from statsmodels.regression.linear_model import OLS
from scipy.stats import kendalltau, spearmanr
from scipy.optimize import minimize
import main_key as k
import time

def fetch_ohlcv_data(phemex, symbol, timeframe='1d', limit=250):
    """Fetch OHLCV data for a single symbol"""
    try:
        since = phemex.milliseconds() - (limit * 24 * 60 * 60 * 1000)
        ohlcv = phemex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        if len(df) < 249:
            print(f"Skipping {symbol}: Insufficient data ({len(df)} candles)")
            return None
        
        return df['close']
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

def load_live_data():
    """Load live data from Phemex for all symbols"""
    phemex = ccxt.phemex({
        'apiKey': k.key,
        'secret': k.secret,
        'enableRateLimit': True
    })

    symbols_df = pd.read_csv('pair_analysis\phe_symbols.csv')
    symbols = symbols_df['symbol'].tolist()

    print(f"Loading data for {len(symbols)} symbols...")
    
    data = {}
    for symbol in symbols:
        print(f"Fetching data for {symbol}")
        series = fetch_ohlcv_data(phemex, symbol)
        if series is not None and not series.empty:
            series = series.replace([np.inf, -np.inf], np.nan)
            if series.notna().sum() >= 100:
                data[symbol] = series
        time.sleep(phemex.rateLimit / 1000)

    result_df = pd.DataFrame(data)
    result_df = result_df.ffill().bfill().dropna()
    
    print(f"Successfully loaded {len(result_df.columns)} symbols with {len(result_df)} valid timestamps each")
    return result_df

def hedge_ratio(series1, series2):
    """Calculate hedge ratio using OLS regression."""
    try:
        X = np.vstack([series2, np.ones(len(series2))]).T
        model = OLS(series1, X).fit()
        return model.params[0]
    except:
        return np.nan

def half_life(series):
    """Calculate half-life of mean reversion using Ornstein-Uhlenbeck process."""
    try:
        series_lag = series.shift(1)
        delta_series = series - series_lag
        delta_series = delta_series.dropna()
        series_lag = series_lag.dropna()
        
        X = np.vstack([series_lag, np.ones(len(series_lag))]).T
        model = OLS(delta_series, X).fit()
        lambda_value = -model.params[0]
        return np.log(2) / lambda_value if lambda_value > 0 else np.nan
    except:
        return np.nan

def compute_statistics(series1, series2):
    """Compute correlation and dependency measures with error handling"""
    try:
        pearson_corr = series1.corr(series2)
        spearman_corr, _ = spearmanr(series1, series2)
        kendall_corr, _ = kendalltau(series1, series2)
        return pearson_corr, spearman_corr, kendall_corr
    except:
        return np.nan, np.nan, np.nan

def engle_granger_test(series1, series2):
    """Run Engle-Granger Cointegration Test with error handling"""
    try:
        score, p_value, _ = coint(series1, series2)
        return p_value if np.isfinite(p_value) else np.nan
    except:
        return np.nan

def analyze_pairs(data):
    """Analyze all pairs for cointegration, correlation, hedge ratio, and half-life."""
    symbols = list(data.columns)
    results = []
    
    for i in range(len(symbols)):
        for j in range(i + 1, len(symbols)):
            s1, s2 = symbols[i], symbols[j]
            series1, series2 = data[s1], data[s2]
            
            if len(series1) < 100 or len(series2) < 100:
                continue
            
            p_value = engle_granger_test(series1, series2)
            pearson_corr, spearman_corr, kendall_corr = compute_statistics(series1, series2)
            hedge = hedge_ratio(series1, series2)
            spread = series1 - hedge * series2
            half = half_life(spread)
            
            results.append([s1, s2, p_value, pearson_corr, spearman_corr, kendall_corr, hedge, half])
    
    df_results = pd.DataFrame(results, columns=['Asset1', 'Asset2', 'Cointegration P-Value', 'Pearson', 'Spearman', 'Kendall', 'Hedge Ratio', 'Half-Life'])
    return df_results.sort_values(by='Cointegration P-Value')

if __name__ == "__main__":
    print("Fetching live data from Phemex...")
    data = load_live_data()
    
    if data.empty or len(data.columns) < 2:
        print("Insufficient valid data to perform analysis")
    else:
        print("\nRunning pairs analysis...")
        results = analyze_pairs(data)
        
        if not results.empty:
            pd.set_option('display.max_rows', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_columns', None)
            
            print("\nTop 10 most cointegrated pairs:")
            print(results.head(10))
            
            filename = 'pairs_analysis_results.csv'
            results.to_csv(filename, index=False)
            print(f"\nResults have been saved to '{filename}'")
        else:
            print("No valid pairs found for analysis")
