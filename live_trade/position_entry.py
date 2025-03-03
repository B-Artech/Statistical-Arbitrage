import asyncio
from util import phemex, ask_bid, params
from position_manager import PositionManager
import pandas as pd
import config as c

ENTRY_THRESHOLD = 2
LEVERAGE = 2
DOLLAR_SIZE = 10

async def trade_entry():
    
    df = pd.read_csv(r'C:\Users\Bartezz\Dropbox\algo\Statistical Arbitrage\live_trade\cointegration_pairs.csv')
    timeframe = '1d'
    limit = 100
    OVERBOUGHT_LEVEL = 80
    OVERSOLD_LEVEL = 20
    
        
    for index, row in df.iterrows():
        
        # GET INFORMATION ABOUT PAIR FROM FILE
        sym1 = row['Asset1']
        sym2 = row['Asset2']
        hedge_ratio = row['Hedge Ratio']
        half_life = row['Half-Life']
        
        # CURRENT DATA SERIES FOR EACH SYMBOL
        series_1 =  c.close_pc(sym1, timeframe, limit)
        series_2 =  c.close_pc(sym2, timeframe, limit)
        
        # CALCULATE Z_SCORE
        spread = series_1.close - (hedge_ratio * series_2.close)
        spread_mean = spread.rolling(21).mean()
        spread_std = spread.rolling(21).std()
        z_score = (spread - spread_mean) / spread_std
        
        # SPREAD CHANGE
        spread_curr = spread.iloc[-1]
        spread_prev = spread.iloc[-2]
        spread_change = 'Long' if spread_curr - spread_prev > 0 else 'Short'
        print(f'{sym1} {sym2} z_score {z_score.iloc[-1]:.2f}')
        
        #Z_SCORE REVERSAL
        zs_curr = z_score.iloc[-1]
        zs_prev = z_score.iloc[-2]
        short_reversal = False
        long_reversal = False
        long_reversal = zs_curr < -2 and zs_curr - zs_prev > 0
        short_reversal = zs_curr > 2 and zs_curr - zs_prev < 0
            
        print(f"Long Reversal: {long_reversal}, Short Reversal: {short_reversal}")
        print('>>>>>  <<<<<')
        await asyncio.sleep(0.5)
        
        #CALCULATE STOCHASTIC INDICATOR
        # k_period = 5
        # d_period = 3
        # stoch = ta.stoch(high=spread, low=spread, close=spread, k=k_period, d=d_period)
        # stoch_d_column = f'STOCHd_{k_period}_{d_period}_3'
        # d_current = stoch[stoch_d_column].iloc[-1]
        # d_previous = stoch[stoch_d_column].iloc[-2]
        # d_change_up = d_current - d_previous > 1
        # d_change_down = d_current - d_previous < -1
        
        # if (d_previous <= OVERSOLD_LEVEL and d_current > OVERSOLD_LEVEL and d_change_up):
        #     stoch_s='buy'
        # # Bearish signal: %D crosses below overbought level
        # elif (d_previous >= OVERBOUGHT_LEVEL and d_current < OVERBOUGHT_LEVEL and d_change_down):
        #     stoch_s='sell'
        # else:
        #     stoch_s='neutral'
        
        pos1 = c.open_positions(sym1)
        pos2 = c.open_positions(sym2)
        
        if pos1[1] == True or pos2[1]== True:
            print('Already in Position')
            await asyncio.sleep(0.5)
        
        if abs(zs_curr) > ENTRY_THRESHOLD:
        
            try:
                phemex.set_leverage(LEVERAGE, sym1)
                phemex.set_leverage(LEVERAGE, sym2)
            except Exception as e:
                print(e)
                continue

            price1 = (ask_bid(sym1)[0] + ask_bid(sym1)[1]) / 2
            price2 = (ask_bid(sym2)[0] + ask_bid(sym2)[1]) / 2
            
            size1 = DOLLAR_SIZE / price1
            size2 = DOLLAR_SIZE / price2
            
            action = "BUY" if zs_curr < 0 else "SELL"
            try:
                if pos1[1] == False and pos2[1] == False:
                    if action == 'BUY' and long_reversal == True and spread_change == 'Long':
                        print("WORKING TO BUY LONG SPREAD")
                        phemex.create_market_buy_order(sym1, size1, params)
                        phemex.create_market_sell_order(sym2, size2, params)
                        print(f"Opening positions: Long {sym1} ({size1}), Short {sym2} ({size2})")
                        
                        position = PositionManager(
                            sym1=sym1, sym1_side="BUY", sym1_size=size1, sym1_price=price1,
                            sym2=sym2, sym2_side="SELL", sym2_size=size2, sym2_price=price2,
                            z_score=zs_curr, half_life=half_life, hedge_ratio=hedge_ratio
                        )
                        position.save_to_json()
                        await asyncio.sleep(5)
                        
                    elif action  == 'SELL' and short_reversal == True and spread_change == 'Short':
                        print("WORKING TO SELL SHORT SPREAD")
                        phemex.create_market_sell_order(sym1, size1, params)
                        phemex.create_market_buy_order(sym2, size2, params)
                        print(f"Opening positions: Short {sym1} ({size1}), Long {sym2} ({size2})")
                        
                        position = PositionManager(
                            sym1=sym1, sym1_side="SELL", sym1_size=size1, sym1_price=price1,
                            sym2=sym2, sym2_side="BUY", sym2_size=size2, sym2_price=price2,
                            z_score=zs_curr, half_life=half_life, hedge_ratio=hedge_ratio
                        )                        
                        position.save_to_json()
                        await asyncio.sleep(5)

            except Exception as e:
                print(e)
        else:
            print(f"Not submitting any orders")
            await asyncio.sleep(0.5)
