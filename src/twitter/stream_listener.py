import logging

import tweepy
from tweepy.models import Status

from utils import globals as g

class StreamListener(tweepy.StreamListener):
    def __init__(self, user: int, callback = None):
        super(StreamListener, self).__init__()

        self._log: logging.Logger = logging.getLogger("bot.twitter.StreamListener")
        self._callback = callback

        self.user: int = user

    def on_connect(self):
        self._log.info("Stream connected.")

    def on_status(self, status: Status):
        text: str = status.text.lower()

        # Only parses statuses by the user and ignores retweets.
        if status.author.id == self.user and not hasattr(status, "retweeted_status"):
            term: str = g.config["twitter"]["search_term"]

            if term and term.lower() not in text:
                return

            self._log.info(f"User tweeted | {status.text}")

            if self._callback:
                self._callback(status)

    def on_error(self, status_code: int) -> bool:
        if status_code == 420:
            # TODO: Handle rate limiting properly.
            self._log.warning("The bot is being rate limited.")
            return True

        if status_code == 401:
            self._log.error("The bot is unauthorised. Ensure the provided "
                            "client and access authorisation credentials "
                            "are valid.")
            return False

        self._log.warning("The stream encountered an error with code "
                          f"{status_code}")
        return True

    def on_timeout(self) -> bool:
        self._log.warning("The stream timed out.")
        return True

    def on_disconnect(self, notice):
        self._log.warning(f"Stream disconnected with notice f{notice}")
