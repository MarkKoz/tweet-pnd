from typing import Optional
import logging
import traceback

from exchanges import exchanges
from exchanges.db import Database
from exchanges.exchanges import Exchange
from twitter.twitter import Twitter
from utils import globals as g, utils, image

def handle_text(text: str) -> bool:
    currency: Exchange.Currency = image.parse_currency(text)

    if not currency:
        g.log.info(f"No valid currency was found.")

        return False

    g.log.info(f"Currency | {currency.name} ({currency.symbol})")
    exchanges.place_order(exchanges.get_markets(currency))

    return True

def handle_image(image_url: str) -> bool:
    g.log.debug(f"Image URL | {image_url}")

    img = image.get_image(image_url)
    text: str = image.to_text(img)
    g.log.debug(f"OCR Results | {text}")

    return handle_text(text)

def callback(text: Optional[str] = None, image_url: Optional[str] = None) -> bool:
    if text:
        g.log.debug(f"Handling the tweet's text.")
        return handle_text(text)

    if image_url:
        g.log.debug(f"Handling the tweet's image.")
        return handle_image(image_url)

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
        Twitter(callback)
    except Exception as e:
        g.log.critical(f"{type(e).__name__}: {e}")
        g.log.critical(traceback.format_exc())

if __name__ == "__main__":
    main()
