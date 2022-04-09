import sys
import math
from functools import partial

from binance import ThreadedWebsocketManager

# tickers
tickers = ["BTC", "ETH", "USDT"]

universe = {
    ticker: {
        "ask": math.inf,
        "qask": 0,
    } for ticker in tickers
}


def handle_socket(msg, sym1, sym2):
    universe[sym1]['ask'] = float(msg['a'])
    universe[sym1]['qask'] = float(msg['A'])

    compute_arbi()
    #print(msg)
    #print(type(msg))

def compute_arbi():
    if (universe["BTC"]["ask"] * universe["ETH"]["ask"] * universe["USDT"]["ask"]) < 1:
        q = min([ticker["qask"] for ticker in universe.values()])

        print("Arbitrage !")
        print(f"Buy {q}")

def main():
    
    twm = ThreadedWebsocketManager()

    twm.start()

    twm.start_symbol_book_ticker_socket(partial(handle_socket, sym1="ETH", sym2="BTC"), symbol="ETHBTC")
    twm.start_symbol_book_ticker_socket(partial(handle_socket, sym1="USDT", sym2="ETH"), symbol="USDTETH")
    twm.start_symbol_book_ticker_socket(partial(handle_socket, sym1="BTC", sym2="USDT"), symbol="BTCUSDT")

if __name__ == "__main__":
    main()
