from typing import List
import logging

from bittrex import Bittrex as bx

from exchanges.exchange import Exchange
import utils.globals as g

class Bittrex(Exchange):
    def __init__(self):
        super().__init__(type(self).__name__)
        self._log: logging.Logger = logging.getLogger("bot.exchanges.Bittrex")
        self._api: bx = self._get_api()

    def _get_api(self) -> bx:
        key: str = g.config["exchanges"]["bittrex"]["key"]
        secret: str = g.config["exchanges"]["bittrex"]["secret"]

        if not key:
            self._log.warning("Key is missing from the config.")

        if not secret:
            self._log.warning("Secret is missing from the config.")

        return bx(key, secret)

    def get_markets(self) -> List[Exchange.Market]:
        markets: dict = self._api.get_markets()

        if not markets["success"]:
            self._log.error("Markets could not be retrieved.")
            return []

        markets = markets["result"]
        self._log.debug(f"Retrieved {len(markets)} markets.")

        # TODO: Filter out inactive markets (not m["IsActive"])?
        return list(map(lambda m: Exchange.Market(m["MarketName"],
                                                  m["MarketCurrency"],
                                                  m["BaseCurrency"]),
                        markets))

    def _get_currencies(self) -> list:
        currencies: dict = self._api.get_currencies()

        if not currencies["success"]:
            self._log.error("Currencies could not be retrieved.")
            return []

        currencies = currencies["result"]
        self._log.debug(f"Retrieved {len(currencies)} currencies.")

        return currencies

    def get_active_currencies(self) -> List[Exchange.Currency]:
        currencies: List[Exchange.Currency] = [
            Exchange.Currency(c["CurrencyLong"], c["Currency"])
            for c in self._get_currencies() if c["IsActive"]]

        self._log.debug(f"Narrowed down to {len(currencies)} active currencies.")

        return currencies
