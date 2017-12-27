import logging

from exchanges.exchange import Exchange
import utils.globals as g

class Binance(Exchange):
    def __init__(self):
        self._log: logging.Logger = logging.getLogger("bot.exchanges.Binance")
        self._api = self._get_api()

    def _get_api(self):
        return
