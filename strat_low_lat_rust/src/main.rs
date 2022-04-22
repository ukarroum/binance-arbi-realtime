use tungstenite::{connect};
use url::Url;

fn main() {
    let (mut socket, response) = connect(Url::parse("wss://stream.binance.com:9443/stream?streams=ethbtc@bookTicker/usdteth@bookTicker/btcusdt@bookTicker").unwrap()).expect("Can't connect");

    println!("Response http code: {}", response.status());

    loop {
        let msg = socket.read_message().expect("Error reading message");
        println!("{}", msg);
    }
}
