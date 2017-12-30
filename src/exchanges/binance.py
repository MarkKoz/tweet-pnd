from typing import List
import logging

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from exchanges.exchange import Exchange
import utils.globals as g

class Binance(Exchange):
    def __init__(self):
        super().__init__(type(self).__name__)
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

    def _get_rate(self, market: str):
        try:
            ticker: dict = self._api.get_symbol_ticker(symbol = market)
        except (BinanceAPIException, BinanceRequestException) as e:
            if e.status_code == 429:
                self._log.error("Being rate limited.")
            elif e.status_code == 418:
                self._log.error("IP banned for violation of rate limits.")

            self._log.error(f"Tick values could not be retrieved for {market}.")
            return None

        price: str = ticker["price"]
        self._log.debug(f"Retrieved asking price of {price} for {market}.")

        if g.config["exchanges"]["binance"]["use_multiplier"]:
            return float(price) * (1 + g.config["order"]["multiplier"])
        else:
            return float(price)

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

    def buy_order(self, market: Exchange.Market) -> bool:
        rate: float = self._get_rate(market.name)

        if not rate:
            return False

        total: float = g.config["order"]["quote_currencies"][market.quote.lower()]
        quantity: float = total / rate

        try:
            response: dict = self._api.order_market_buy(
                    symbol = market.name,
                    quantity = total,
                    recvWindow = g.config["exchanges"]["binance"]["recvWindow"])
        except Exception as e:
            self._log.error(f"Order failed | {quantity} {market.base} @ "
                            f"{rate} {market.quote} for a total of {total} "
                            f"{market.quote}: {e}")
            return False

        self._log.info(f"Order placed | {quantity} {market.base} @ {rate} "
                       f"{market.quote} for a total of {total} {market.quote}.")
        self._log.debug(f"Order ID | {response['clientOrderId']}")

        return True
