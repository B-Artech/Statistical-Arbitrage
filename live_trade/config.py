from util import phemex
import asyncio
import pandas as pd
import main_key as k


def open_positions(symbol):
    
    try:
        params = {f'symbol': {symbol},'type':'swap', 'code':'USDT'}
        phe_bal = phemex.fetch_balance(params=params)
        open_pos = phe_bal['info']['data']['positions']
        pos_side = open_pos[0]['side']
        pos_size = open_pos[0]['size']
        
        if pos_side == ('Buy'):
            openpos_bool = True 
            long = True 
        elif pos_side == ('Sell'):
            openpos_bool = True
            long = False
        else:
            openpos_bool = False
            long = None
            
        return open_pos, openpos_bool, pos_size, long
    except Exception as e:
        print(e)
        
    
def close_pc(sym1, timeframe, limit):
    """
    Get close prices for specified timeframe
    Returns dataframe with OHLCV data
    """
     # Convert timeframe to minutes
    timeframe_multiplier = {
        'm': 1,
        'h': 60,
        'd': 1440
    }
    
     # Extract number and unit from timeframe
    number = int(''.join(filter(str.isdigit, timeframe)))
    unit = ''.join(filter(str.isalpha, timeframe)).lower()
    
    # Calculate total minutes
    minutes = number * timeframe_multiplier.get(unit, 1)
    
    # Calculate since time in milliseconds
    since = phemex.milliseconds() - (limit * minutes * 60 * 1000)
    
    bars = phemex.fetch_ohlcv(sym1, timeframe=timeframe, since=since, limit=limit)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df


def close_pc(sym2, timeframe, limit):
    """
    Get close prices for specified timeframe
    Returns dataframe with OHLCV data
    """
     # Convert timeframe to minutes
    timeframe_multiplier = {
        'm': 1,
        'h': 60,
        'd': 1440
    }
    
     # Extract number and unit from timeframe
    number = int(''.join(filter(str.isdigit, timeframe)))
    unit = ''.join(filter(str.isalpha, timeframe)).lower()
    
    # Calculate total minutes
    minutes = number * timeframe_multiplier.get(unit, 1)
    
    # Calculate since time in milliseconds
    since = phemex.milliseconds() - (limit * minutes * 60 * 1000)
    bars = phemex.fetch_ohlcv(sym2, timeframe=timeframe, since=since, limit=limit)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def df_sma(symbol, timeframe, limit, sma):
    """
    Calculate SMA for given parameters
    Returns dataframe with SMA values
    """
    print('starting indis...')
    
    timeframe_minutes = int(''.join(filter(str.isdigit, timeframe)))  # Extract minutes from timeframe string
    since = phemex.milliseconds() - (limit * timeframe_minutes * 60 * 1000)  # Convert to milliseconds
    
    try:
        # Fetch OHLCV data
        bars = phemex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        
        # Create dataframe
        df_sma = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df_sma['timestamp'] = pd.to_datetime(df_sma['timestamp'], unit='ms')
        
        # Calculate SMA
        df_sma[f'sma{sma}_{timeframe}'] = df_sma.close.rolling(sma).mean()
        
        return df_sma
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None
   
def df_sma(symbol, timeframe, limit, sma):
    """
    Calculate SMA for given parameters with historical data
    Returns dataframe with SMA values
    
    Parameters:
    symbol (str): Trading pair symbol
    timeframe (str): Timeframe (e.g., '15m', '4h')
    limit (int): Number of candles to fetch
    sma (int): Simple Moving Average period
    """
    # Convert timeframe to minutes
    timeframe_multiplier = {
        'm': 1,
        'h': 60,
        'd': 1440
    }
    
    # Extract number and unit from timeframe
    number = int(''.join(filter(str.isdigit, timeframe)))
    unit = ''.join(filter(str.isalpha, timeframe)).lower()
    
    # Calculate total minutes
    minutes = number * timeframe_multiplier.get(unit, 1)
    
    # Calculate since time in milliseconds
    since = phemex.milliseconds() - (limit * minutes * 60 * 1000)
    
    # Fetch OHLCV data
    bars = phemex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)

    # Create dataframe
    df_sma = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df_sma['timestamp'] = pd.to_datetime(df_sma['timestamp'], unit='ms')
    df_sma.set_index('timestamp', inplace=True)
    
    # Calculate SMA
    df_sma[f'sma{sma}_{timeframe}'] = df_sma['close'].rolling(sma).mean()
    
    return df_sma
        
  
def df_stoch(symbol, timeframe, limit, k_period, d_period, smooth_k):
    """
    Calculate Stochastic for given parameters with historical data
    Returns dataframe with Stochastic values

    Parameters:
    symbol (str): Trading pair symbol
    timeframe (str): Timeframe (e.g., '15m', '4h')
    limit (int): Number of candles to fetch
    k_period (int): Look-back period for %K
    d_period (int): Period for %D moving average
    smooth_k (int): Period for smoothing %K
    """
    # Convert timeframe to minutes
    timeframe_multiplier = {
        'm': 1,
        'h': 60,
        'd': 1440
    }

    # Extract number and unit from timeframe
    number = int(''.join(filter(str.isdigit, timeframe)))
    unit = ''.join(filter(str.isalpha, timeframe)).lower()

    # Calculate total minutes
    minutes = number * timeframe_multiplier.get(unit, 1)

    # Calculate since time in milliseconds
    since = phemex.milliseconds() - (limit * minutes * 60 * 1000)

    # Fetch OHLCV data
    bars = phemex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)

    # Create dataframe
    df_stoch = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df_stoch['timestamp'] = pd.to_datetime(df_stoch['timestamp'], unit='ms')
    df_stoch.set_index('timestamp', inplace=True)

    # Calculate Stochastic
    # Use pandas_ta for the calculation
    stoch = df_stoch.ta.stoch(high='high', low='low', close='close',
                                k=k_period, d=d_period, smooth_k=smooth_k)

    # Rename columns to match timeframe
    df_stoch[f'%K_{timeframe}'] = stoch[f'STOCHk_{k_period}_{d_period}_{smooth_k}']
    df_stoch[f'%D_{timeframe}'] = stoch[f'STOCHd_{k_period}_{d_period}_{smooth_k}']

    return df_stoch


def get_stoch(df, timeframe):
    """
    Get trading signal based on %D line crosses
    
    Parameters:
    df (pandas.DataFrame): DataFrame with stochastic values
    timeframe (str): Timeframe to check signals for
    
    Returns:
    str: 'buy', 'sell', or 'neutral'
    """
    if len(df) < 2:
        return 'neutral'
        
    current = df.iloc[-1]
    previous = df.iloc[-2]
  
    
    d_current = current[f'%D_{timeframe}']
    d_previous = previous[f'%D_{timeframe}']
    
    d_change_up = d_current - d_previous > 1
    d_change_down = d_current - d_previous < -1
    
    # Define levels
    OVERBOUGHT_LEVEL = 80
    OVERSOLD_LEVEL = 20
    
    # Bullish signal: %D crosses above oversold level
    if (d_previous <= OVERSOLD_LEVEL and d_current > OVERSOLD_LEVEL and d_change_up):
        return 'buy'
    
    # Bearish signal: %D crosses below overbought level
    elif (d_previous >= OVERBOUGHT_LEVEL and d_current < OVERBOUGHT_LEVEL and d_change_down):
        return 'sell'
    
    return 'neutral'

def swing(symbol, timeframe, limit, window=5):
    """
    Identify basic swing highs and lows from price action.
    
    Parameters:
    symbol (str): Trading pair symbol
    timeframe (str): Timeframe (e.g., '15m', '4h')  
    limit (int): Number of candles to fetch
    window (int): How many candles to check on each side (default 5)
    
    Returns:
    dict: Dictionary with support and resistance points
    """
    # Convert timeframe to minutes
    timeframe_multiplier = {
        'm': 1,
        'h': 60,
        'd': 1440
    }
    
    # Extract number and unit from timeframe
    number = int(''.join(filter(str.isdigit, timeframe)))
    unit = ''.join(filter(str.isalpha, timeframe)).lower()
    
    # Calculate total minutes
    minutes = number * timeframe_multiplier.get(unit, 1)
    
    # Calculate since time in milliseconds
    since = phemex.milliseconds() - (limit * minutes * 60 * 1000)
    
    # Fetch OHLCV data
    bars = phemex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)

    # Create dataframe
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    highs = df['high'].values  # Get all high prices as an array
    lows = df['low'].values    # Get all low prices as an array
    
    resistance_points = []
    support_points = []
    
    # For resistance (swing highs)
    for i in range(window, len(df) - window):
        current_high = highs[i]
        previous_prices = highs[i-window:i]
        next_prices = highs[i+1:i+window+1]
        
        if all(current_high > previous_prices) and all(current_high > next_prices):
            resistance_points.append(current_high)
    
    # For support (swing lows)
    for i in range(window, len(df) - window):
        current_low = lows[i]
        previous_prices = lows[i-window:i]
        next_prices = lows[i+1:i+window+1]
        
        if all(current_low < previous_prices) and all(current_low < next_prices):
            support_points.append(current_low)
    
    return {
        'resistance': resistance_points,
        'support': support_points
    }