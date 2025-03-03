import ccxt
import pandas as pd
import schedule
import time
import datetime
import live_trade.main_key as k
import os
import json

# ---- CONNECT TO PHEMEX ----
phemex = ccxt.phemex({
    'apiKey': k.key,
    'secret': k.secret,
    'enableRateLimit': True
})

# ---- FILE PATHS ----
CSV_FILE = "crypto_spread_data.csv"
JSON_FILE = "open_positions.json"

# ---- LOAD SYMBOLS FROM JSON ----
def load_symbols_from_json():
    try:
        with open(JSON_FILE, 'r') as file:
            positions = json.load(file)
        
        symbols = []
        for pos in positions:
            if pos["sym1_side"] == "BUY":
                long_sym, short_sym = pos["sym1"], pos["sym2"]
                long_price, short_price = pos["sym1_price"], pos["sym2_price"]
            else:
                long_sym, short_sym = pos["sym2"], pos["sym1"]
                long_price, short_price = pos["sym2_price"], pos["sym1_price"]
            
            symbols.append((long_sym, short_sym, long_price, short_price))
        
        return symbols
    except Exception as e:
        print(" Error loading symbols from JSON:", e)
        return []

# ---- CREATE INITIAL CSV ----
def create_csv():
    if not os.path.exists(CSV_FILE):
        try:
            symbols = load_symbols_from_json()
            if not symbols:
                print("No symbols found in JSON.")
                return
            
            data = []
            for i, (long_sym, short_sym, long_price, short_price) in enumerate(symbols, start=1):
                start_spread = round(long_price / short_price, 4)
                data.append([i, long_sym, short_sym, long_price, short_price, start_spread, long_price, short_price, start_spread, 0, 0])

            columns = ["Ind", "L Sym", "S Sym", "L Ent", "S Ent", "Str Spr", 
                       "Cur L", "Cur S", "Cur Spr", "% Chg", "Cyc"]

            df = pd.DataFrame(data, columns=columns)
            df.to_csv(CSV_FILE, index=False)
            print(" CSV Template created.")
        except Exception as e:
            print(" Error creating CSV:", e)

# ---- UPDATE PRICES EVERY MINUTE ----
def update_prices():
    try:
        df = pd.read_csv(CSV_FILE)

        for i in range(len(df)):
            long_sym = df.at[i, "L Sym"]
            short_sym = df.at[i, "S Sym"]
            current_long = phemex.fetch_ticker(long_sym)['last']
            current_short = phemex.fetch_ticker(short_sym)['last']
            current_spread = round(current_long / current_short, 4)
            spread_change = round((current_spread - df.at[i, "Str Spr"]) / df.at[i, "Str Spr"], 6)
            df.at[i, "Cur L"] = current_long
            df.at[i, "Cur S"] = current_short
            df.at[i, "Cur Spr"] = current_spread
            df.at[i, "% Chg"] = spread_change

        df.to_csv(CSV_FILE, index=False)
        print(f"✅ Prices updated at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(" Error updating prices:", e)

# ---- UPDATE 30-MINUTE PERFORMANCE ----
def update_minutes_performance():
    try:
        df = pd.read_csv(CSV_FILE)

        for i in range(len(df)):
            df.at[i, "Cyc"] += 1
            cycle = df.at[i, "Cyc"]
            cycle_col = f"H {cycle}"
            if cycle_col not in df.columns:
                df[cycle_col] = 0.0
            if cycle == 1:
                df.at[i, cycle_col] = df.at[i, "% Chg"]
            else:
                prev_cycles_sum = df.iloc[i, 11:11 + cycle - 1].sum()
                df.at[i, cycle_col] = df.at[i, "% Chg"] - prev_cycles_sum

        df.to_csv(CSV_FILE, index=False)
        print(f"✅ 30-minute performance updated at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(" Error updating 30-minute performance:", e)

# ---- SCHEDULE UPDATES ----
schedule.every(1).minutes.do(update_prices)
schedule.every(30).minutes.do(update_minutes_performance)

if __name__ == "__main__":
    create_csv()
    while True:
        schedule.run_pending()
        time.sleep(10)
