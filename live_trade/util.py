import ccxt
import main_key as k

params = {'type': 'swap', 'code': 'USDT'} # Market Orders
phemex = ccxt.phemex({
    'apiKey': k.key,
    'secret': k.secret,
    'enableRateLimit': True
})

def ask_bid(symbol):
        ob = phemex.fetch_order_book(symbol)
        bid = ob['bids'][0][0]
        ask = ob['asks'][0][0]
        return ask, bid