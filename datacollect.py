import time
import sys
import os
import functools

from binance import ThreadedWebsocketManager
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


def handle_ticker_data(msg, write_client):
    """
        Handle the ticker data received from binance
    """
    print(msg)
    
    # saving to influxdb
    for t in msg:
        # same order as in here: https://python-binance.readthedocs.io/en/latest/binance.html#binance.streams.BinanceSocketManager.symbol_ticker_socket
        p = influxdb_client.Point("ticker_data")\
                .tag("event_type", t["e"])\
                .field("event_time", t["E"])\
                .tag("symbol", t["s"])\
                .field("price_change", t["p"])\
                .field("price_change_percent", t["P"])\
                .field("weighted_average_price", t["w"])\
                .field("prev_close_price", t["x"])\
                .field("close_price", t["c"])\
                .field("close_qty", t["Q"])\
                .field("bid", t["b"])\
                .field("bid_qty", t["B"])\
                .field("ask", t["a"])\
                .field("ask_qty", t["A"])\
                .field("open", t["o"])\
                .field("high", t["h"])\
                .field("low", t["l"])\
                .field("total_traded_base_volume", t["v"])\
                .field("total_traded_quote_volume", t["q"])\
                .field("stats_open", t["O"])\
                .field("stats_close", t["C"])\
                .field("first_tid", t["F"])\
                .field("last_tid", t["L"])\
                .field("total_trades", t["n"])

        save_point(p, write_client)


def handle_symbol_book_ticker_socket(msg, write_client):
    print(msg)

    p = influxdb_client.Point("book_ticker")\
            .tag("symbol", msg["s"])\
            .field("updamsge_id", msg["u"])\
            .field("bid", msg["b"])\
            .field("ask", msg["a"])\
            .field("bid_qty", msg["B"])\
            .field("ask_qty", msg["A"])

    save_point(p, write_client)


def save_point(p, write_client):
    write_client.write(bucket=os.environ['ARBI_INFLUX_BUCKET'], org=os.environ["ARBI_INFLUX_ORG"], record=p)

def get_writer():
    client = influxdb_client.InfluxDBClient(
        url=os.environ['ARBI_INFLUX_URL'],
        token=os.environ['ARBI_INFLUX_TOKEN'],
        org=os.environ['ARBI_INFLUX_ORG']
    )

    return client.write_api(write_options=SYNCHRONOUS)


def main():
    write_client = get_writer()

    twm = ThreadedWebsocketManager()

    twm.start()

    twm.start_symbol_book_ticker_socket(callback=functools.partial(handle_symbol_book_ticker_socket, write_client=write_client), symbol="BNBUSDT")

    twm.join()


if __name__ == "__main__":
   main()
