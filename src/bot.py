from exchanges.binance import Binance
from exchanges.bittrex import Bittrex
from twitter.twitter import Twitter
from utils import globals as g, utils

def main() -> None:
    utils.get_logger("bot")

    if not utils.load_config():
        return

    twitter = Twitter()

    if g.config["exchanges"]["binance"]["enabled"]:
        binance = Binance()

    if g.config["exchanges"]["bittrex"]["enabled"]:
        bittrex = Bittrex()

    while twitter.stream.running:
        inp: str = input("Enter 'exit' at any time to disconnect from the "
                         "stream.\n")

        if inp.lower() == "exit":
            g.log.info("Disconnecting from the stream.")
            twitter.stream.disconnect()
            break

    g.log.info("Steam has disconnected. The program will now close.")

if __name__ == "__main__":
    main()
