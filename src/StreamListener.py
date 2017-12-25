import logging

import tweepy
from tweepy.models import Status
from bittrex import Bittrex

class StreamListener(tweepy.StreamListener):
    config: dict = {}
    bittrex: Bittrex = None
    log: logging.Logger = None

    def __init__(self,
                 cfg: dict,
                 logger: logging.Logger,
                 user: int,
                 callback = None):
        global config
        global bittrex
        global log
        config = cfg
        bittrex = Bittrex(config["bittrex"]["key"],
                          config["bittrex"]["secret"],
                          api_version = "v2.0")
        log = logger

        super(StreamListener, self).__init__()

        self.user: int = user
        self.currencies: list = []
        self.callback = callback

        self.getCurrencies()

    def getCurrencies(self):
        curr: dict = bittrex.get_currencies()

        if not curr["success"]:
            raise RuntimeError("The currencies could not be retrieved from "
                               "Bittrex.")

        self.currencies = curr["result"]
        log.info(f"Loaded {len(self.currencies)} currencies from Bittrex.")

        self.currencies = [c for c in self.currencies if c["IsActive"]]
        log.info(f"Narrowed down to {len(self.currencies)} active currencies.")

    def on_status(self, status: Status):
        # log.info(f"{status.author.screen_name} tweeted | {status.text}")

        # Only parses statuses by the author; ignores retweets, replies, etc.
        if status.author.id == self.user:
            log.info(f"User tweeted | {status.text}")

            # Finds the first currency whose long name is found in the text of
            # the status. None if no match is found.
            currency = next((currency for currency in self.currencies
                             if currency["CurrencyLong"] in status.text or
                             currency["Currency"] in status.text),
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
