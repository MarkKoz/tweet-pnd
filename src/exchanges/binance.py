import logging

from binance.client import Client

from exchanges.exchange import Exchange
import utils.globals as g

class Binance(Exchange):
    def __init__(self):
        self._log: logging.Logger = logging.getLogger("bot.exchanges.Binance")
        self._api = self._get_api()

    def _get_api(self):
        key: str = g.config["exchanges"]["binance"]["key"]
        secret: str = g.config["exchanges"]["binance"]["secret"]

        if not key:
            self._log.warning("Key is missing from the config.")

        if not secret:
            self._log.warning("Secret is missing from the config.")

        return Client(key, secret)
