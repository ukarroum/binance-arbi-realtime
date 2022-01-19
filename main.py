import time

from binance import ThreadedWebsocketManager

def handle_ticker_data(msg):
    """
        Handle the ticker data received from binance
    """
    print(msg)

def main():
    twm = ThreadedWebsocketManager()

    twm.start()

    twm.start_ticker_socket(callback=handle_socket_message)

    twm.join()


if __name__ == "__main__":
   main()
