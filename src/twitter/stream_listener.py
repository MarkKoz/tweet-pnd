from logging.handlers import TimedRotatingFileHandler
from typing import Optional
import logging

import tweepy
from tweepy.models import Status

import utils.globals as g

class StreamListener(tweepy.StreamListener):
    def __init__(self, user: int, callback):
        super().__init__()

        self._log: logging.Logger = logging.getLogger("bot.twitter.StreamListener")
        self._log_t: Optional[logging.Logger] = \
            self._get_logger() if g.config["twitter"]["log_tweets"] else None
        self._callback = callback

        self.user: int = user

    @staticmethod
    def _get_logger() -> logging.Logger:
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

    @staticmethod
    def _get_photo(status: Status) -> Optional[str]:
        # Ignores statuses without entities.
        if not hasattr(status, "extended_entities"):
            return None

        # Ignores statuses without a media entity.
        media = status.extended_entities[
            "media"] if "media" in status.extended_entities else None
        if not media:
            return None

        # Tries to find the first occurrence of a photo media entity.
        return next((o for o in media if o["type"] == "photo"), None)

    def _validate_status(self, status: Status) -> bool:
        # Only parses statuses by the user.
        if status.author.id != self.user:
            return False

        # Logs each status if the option is enabled.
        if self._log_t:
            self._log_t.info(status.text)

        # Ignores retweets if the option is enabled.
        if g.config["twitter"]["ignore_retweets"] and \
                hasattr(status, "retweeted_status"):
            return False

        # Ignores statuses which don't contain the search term.
        term: str = g.config["twitter"]["search_term"]
        if term and term.lower() not in status.text.lower():
            return False

        return True

    def on_connect(self):
        self._log.info("Stream connected.")

    def on_status(self, status: Status):
        if not self._validate_status(status):
            return True

        search_text: bool = g.config["twitter"]["search_text"]
        search_image: bool = g.config["twitter"]["search_image"]

        if search_text:
            result: bool = self._callback(text = status.text)

            # Returns if successful or image parsing is disabled.
            if (search_image and result) or not search_image:
                self._log.info(f"User tweeted | {status.text}")

                return not g.config["twitter"]["disconnect_on_first"]

        if search_image:
            photo: Optional[str] = self._get_photo(status)

            # Ignores the status if it doesn't have a photo.
            if not photo:
                return True

            self._log.info(f"User tweeted | {status.text}")
            self._callback(image_url = photo["media_url"])

            return not g.config["twitter"]["disconnect_on_first"]

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
