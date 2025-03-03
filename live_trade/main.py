import asyncio
import time
from position_exit import exit_trade
from position_entry import trade_entry

MANAGE_EXIT = True
MANAGE_TRADES = True


async def main():

    while True:
        if MANAGE_EXIT:
            try:
                print("Managing exits...")
                await exit_trade()
                time.sleep(1)
            except Exception as e:
                print(f"Error managing exiting position {e}")
                
                
        if MANAGE_TRADES:
            try:
                print("Looking for positions to open")
                await trade_entry()
            except Exception as e:
                print(f"Error opening trades: {e}")
                
        await asyncio.sleep(5)
        
if __name__ == "__main__":
    asyncio.run(main())