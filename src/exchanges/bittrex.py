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

    def _get_rate(self, market: str):
        ticker: dict = self._api.get_ticker(market)

        if not ticker["success"]:
            self._log.error(f"Tick values could not be retrieved for {market}.")
            return None

        ask: float = ticker["result"]["Ask"]
        self._log.debug(f"Retrieved asking price of {ask} for {market}.")

        if g.config["exchanges"]["bittrex"]["use_multiplier"]:
            return ask * (1 + g.config["order"]["multiplier"])
        else:
            return ask

    def get_markets(self) -> List[Exchange.Market]:
        markets: dict = self._api.get_markets()

        if not markets["success"]:
            self._log.error("Markets could not be retrieved: "
                            f"{markets['message']}")
            return []

        markets = markets["result"]
        self._log.debug(f"Retrieved {len(markets)} markets.")

        # TODO: Filter out inactive markets (not m["IsActive"])?
        return list(map(lambda m: Exchange.Market(
                            m["MarketName"],
                            Exchange.Currency(
                                    m["MarketCurrency"],
                                    m["MarketCurrencyLong"],
                                    None),
                            Exchange.Currency(
                                    m["BaseCurrency"],
                                    m["BaseCurrencyLong"],
                                    None),
                            None),
                        markets))

    def buy_order(self, market: Exchange.Market) -> bool:
        rate: float = self._get_rate(market.name)

        if not rate:
            return False

        quote_symbol: str = market.quote.symbol.lower()
        total: float = g.config["order"]["quote_currencies"][quote_symbol]
        quantity: float = total / rate
        response: dict = self._api.buy_limit(market.name, quantity, rate)

        if not response["success"]:
            self._log.error(f"Order failed | {quantity} {market.base.symbol} @ "
                            f"{rate} {market.quote.symbol} for a total of "
                            f"{total} {market.quote.symbol}: "
                            f"{response['message']}")
            return False

        self._log.info(f"Order placed | {quantity} {market.base.symbol} @ "
                       f"{rate} {market.quote.symbol} for a total of {total} "
                       f"{market.quote.symbol}.")
        self._log.debug(f"Order UUID | {response['result']['uuid']}")

        return True
