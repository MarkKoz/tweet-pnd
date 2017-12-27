import logging

from twitter.twitter import Twitter
from utils import globals as g, utils, image

def on_tweet(url: str):
    g.log.debug(f"Image URL | {url}")

    img = image.get_image(url)
    text: str = image.to_text(img)
    g.log.debug(f"OCR Results | {text}")

    result: image.ParseResult = image.parse_currency(text)

    if result:
        g.log.info(f"Currency | {result.currency.name} "
                   f"({result.currency.symbol})")
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

    image.init()
    twitter = Twitter(on_tweet)

    while twitter.stream.running:
        inp: str = input("Enter 'exit' at any time to disconnect from the "
                         "stream.\n")

        if inp.lower() == "exit":
            g.log.info("Disconnecting from the stream.")
            twitter.stream.disconnect()
            break

    g.log.info("Stream has disconnected. The program will now close.")

if __name__ == "__main__":
    main()
