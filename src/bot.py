import logging
import traceback

from exchanges import exchanges
from exchanges.db import Database
from exchanges.exchanges import Exchange
from twitter.twitter import Twitter
from utils import globals as g, utils, image

def on_tweet(url: str) -> None:
    g.log.debug(f"Image URL | {url}")

    img = image.get_image(url)
    text: str = image.to_text(img)
    g.log.debug(f"OCR Results | {text}")

    currency: Exchange.Currency = image.parse_currency(text)

    if currency:
        g.log.info(f"Currency | {currency.name} "
                   f"({currency.symbol})")
        exchanges.place_order(exchanges.get_markets(currency))
    else:
        g.log.info(f"No valid currency was found.")

def main() -> None:
    utils.get_logger("bot")

    # Terminate if the config failed to load.
    if not utils.load_config():
        return

    # Set logging level to debug if verbose is true.
    if g.config["verbose"]:
        g.log.setLevel(logging.DEBUG)
        g.log.handlers[0].setLevel(logging.DEBUG)

    try:
        g.exchanges = exchanges.get_exchanges()
        g.db = Database()
        image.init()
        Twitter(on_tweet)
    except Exception as e:
        g.log.critical(f"{type(e).__name__}: {e}")
        g.log.critical(traceback.format_exc())

if __name__ == "__main__":
    main()
