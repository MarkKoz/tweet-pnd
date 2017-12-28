from typing import List
import logging

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

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

    def get_markets(self) -> List[Exchange.Market]:
        try:
            markets: dict = self._api.get_exchange_info()
        except (BinanceAPIException, BinanceRequestException) as e:
            if isinstance(e, BinanceAPIException):
                # TODO: Raise an exception when rate limited. Probably overkill
                # because it's unlikely over 1200 requests will be sent per
                # minute.
                if e.status_code == 429:
                    self._log.error("Being rate limited.")
                elif e.status_code == 418:
                    self._log.error("IP banned for violation of rate limits.")

            self._log.error("Markets could not be retrieved.")
            return []

        markets = markets["symbols"]
        self._log.debug(f"Retrieved {len(markets)} markets.")

        # TODO: Filter out inactive markets (m["status"] != "TRADING")
        return list(map(lambda m: Exchange.Market(m["symbol"],
                                                  m["baseAsset"],
                                                  m["quoteAsset"]),
                        markets))
