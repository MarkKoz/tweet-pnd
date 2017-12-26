import tweepy
from tweepy.models import Status

import Globals as g
import Logging

class StreamListener(tweepy.StreamListener):
    def __init__(self, user: int, callback = None):
        global log
        log = Logging.getLogger("Stream")

        super(StreamListener, self).__init__()

        self.user: int = user
        self.currencies: list = []
        self.callback = callback

        self.getCurrencies()

    def getCurrencies(self):
        curr: dict = g.bittrex.get_currencies()

        if not curr["success"]:
            raise RuntimeError("The currencies could not be retrieved from "
                               "Bittrex.")

        self.currencies = curr["result"]
        log.info(f"Loaded {len(self.currencies)} currencies from Bittrex.")

        # self.currencies = [c for c in self.currencies if c["IsActive"]]
        # log.info(f"Narrowed down to {len(self.currencies)} active currencies.")

    def on_status(self, status: Status):
        text: str = status.text.lower()
        # log.info(f"{status.author.screen_name} tweeted | {status.text}")

        # Only parses statuses by the user and ignores retweets.
        if status.author.id == self.user and not hasattr(status, "retweeted_status"):
            term: str = g.config["twitter"]["search_term"]

            if term and term.lower() not in text:
                return

            log.info(f"User tweeted | {status.text}")

            # Finds the first currency whose long name is found in the text of
            # the status. None if no match is found.
            currency = next((currency for currency in self.currencies
                             if currency["CurrencyLong"].lower() in text or
                             currency["Currency"].lower() in text),
                            None)

            # Prints the name of currency market if one was found.
            if currency:
                self.callback(currency)
            else:
                log.warning("The currency in the tweet is not on Bittrex.")

    def on_error(self, status_code: int) -> bool:
        if status_code == 420:
            # TODO: Handle rate limiting properly.
            log.error("The stream has closed due to rate limiting.")
            return True

        log.error(f"The stream encountered an error with code {status_code}")
        return True

    def on_timeout(self) -> bool:
        log.warning("The stream timed out.")
        return True

    def on_disconnect(self, notice):
        log.warning(f"Stream disconnected with notice f{notice}")
