from logging.handlers import TimedRotatingFileHandler
from typing import Optional
import logging

import tweepy
from tweepy.models import Status

import utils.globals as g

class StreamListener(tweepy.StreamListener):
    def __init__(self, user: int, callback = None):
        super().__init__()

        self._log: logging.Logger = logging.getLogger("bot.twitter.StreamListener")
        self._log_t: Optional[logging.Logger] = \
            self.get_logger() if g.config["twitter"]["log_tweets"] else None
        self._callback = callback

        self.user: int = user

    @staticmethod
    def get_logger() -> logging.Logger:
        logger: logging.Logger = logging.getLogger("StreamLogger")
        logger.setLevel(logging.INFO)
        formatter: logging.Formatter = logging.Formatter(
                "%(asctime)s - %(message)s")

        handler: TimedRotatingFileHandler = TimedRotatingFileHandler(
                filename = f"log-tweets-{g.config['twitter']['user']}.txt",
                when = "midnight",
                encoding = "utf-8")
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def on_connect(self):
        self._log.info("Stream connected.")

    def on_status(self, status: Status):
        text: str = status.text.lower()

        # Only parses statuses by the user.
        if status.author.id == self.user:
            if self._log_t:
                self._log_t.info(status.text)

            if g.config["twitter"]["ignore_retweets"] and \
                    hasattr(status, "retweeted_status"):
                return True

            term: str = g.config["twitter"]["search_term"]
            if term and term.lower() not in text: return True

            if not hasattr(status, "entities"): return True

            media = status.entities["media"] if "media" in status.entities else None
            if not media: return True

            photo = next((o for o in media if o["type"] == "photo"),  None)
            if not photo: return True

            self._log.info(f"User tweeted | {status.text}")

            if self._callback:
                self._callback(photo["media_url"])

                if g.config["twitter"]["disconnect_on_first"]:
                    return False

        return True

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
