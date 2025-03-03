from util import phemex, ask_bid, params
import asyncio
import json
import config as c

async def exit_trade():
    save_output = [] 
    timeframe = '1d'
    limit = 100
    positions_closed = False # TRACK IF ANY POSITIONS WAS CLOSED
    try:
        position_file = open("live_trade\open_positions.json")
        position_dict = json.load(position_file)
    except:
        return "complet"
    
    if len(position_dict) < 1:
        print("No open position in list")
        return "complet"
    
    for p in position_dict:
        
        is_close= False
        
        #EXTRACT POSITION INFORMATION FROM FILE
        sym1= p['sym1']
        sym1_size= p['sym1_size']
        sym2= p['sym2']
        sym2_size= p['sym2_size']
        hedge_ratio= p['hedge_ratio']
        z_score_traded = p['z_score']
        
        series_1 =  c.close_pc(sym1, timeframe, limit)
        series_2 =  c.close_pc(sym2, timeframe, limit)
        
        # CALCULATE Z_SCORE 
        spread = series_1.close - (hedge_ratio * series_2.close)
        spread_mean = spread.rolling(21).mean()
        spread_std = spread.rolling(21).std()
        z_score_calc= (spread - spread_mean) / spread_std
        print(f'{sym1} {sym2} z_score current {z_score_calc.iloc[-1]:.2f}')
        z_score_current = z_score_calc.iloc[-1]
        
        
        z_score_level_check = abs(z_score_current) >= abs(z_score_traded)
        z_score_cross_check = (z_score_current < 0 and z_score_traded > 0) or (z_score_current > 0 and z_score_traded < 0)
        
        open_pos1=  c.open_positions(sym1)
        open_pos2=  c.open_positions(sym2)
        
        if z_score_level_check and z_score_cross_check:
            is_close = True
        
        
        if is_close and open_pos1[1] and open_pos2[1]:
            print(">>> Working on Closing <<<")
            try:
                if not open_pos1[3] and not open_pos2[3]:
                    phemex.create_market_buy_order(sym1, sym1_size, params)
                    phemex.create_market_sell_order(sym2, sym2_size, params)
                else:
                    phemex.create_market_sell_order(sym1, sym1_size, params)
                    phemex.create_market_buy_order(sym2, sym2_size, params)
                await asyncio.sleep(0.5)
                positions_closed = True
                
            except Exception as e:
                print(f"Error executing trade {e}")
                save_output.append(p)
        else:
            save_output.append(p)
            
    if positions_closed:
        with open("open_positions.json", 'w') as f:
            json.dump(save_output, f)
    return "completed"
