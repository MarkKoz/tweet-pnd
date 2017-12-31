from decimal import Decimal, ROUND_DOWN
from typing import List, Union
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

    @staticmethod
    def _get_step_size(filters: dict) -> Union[Decimal, None]:
        return next((Decimal(f["stepSize"].rstrip("0")) for f in filters
                     if f["filterType"] == "LOT_SIZE"), None)

    def _get_price(self, market: Exchange.Market) -> Union[Decimal, None]:
        try:
            ticker: dict = self._api.get_symbol_ticker(symbol = market.name)
        except (BinanceAPIException, BinanceRequestException) as e:
            if e.status_code == 429:
                self._log.error("Being rate limited.")
            elif e.status_code == 418:
                self._log.error("IP banned for violation of rate limits.")

            self._log.error("Tick values could not be retrieved for "
                            f"{market.name}.")
            return None

        price: str = ticker["price"].rstrip("0")
        self._log.debug(f"Retrieved asking price of {price} for {market.name}.")

        p: Union[int, None] = market.quote.precision
        precision: Decimal = Decimal(10) ** -p if p else -8

        use_mult: bool = g.config["exchanges"]["binance"]["use_multiplier"]
        mult_str: str = str(g.config["order"]["multiplier"]).rstrip("0")
        mult: Decimal = Decimal(mult_str) if use_mult else Decimal(0)

        price_d: Decimal = (Decimal(price) * (1 + mult)).quantize(precision)
        self._log.debug(f"Adjusted price to {price_d} with a precision of "
                        f"{precision}.")

        return price_d

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
        return list(map(lambda m: Exchange.Market(
                            m["symbol"],
                            Exchange.Currency(
                                    m["baseAsset"],
                                    None,
                                    m["baseAssetPrecision"]),
                            Exchange.Currency(
                                    m["quoteAsset"],
                                    None,
                                    m["quotePrecision"]),
                            self._get_step_size(m["filters"])),
                        markets))

    def buy_order(self, market: Exchange.Market) -> bool:
        price: Union[Decimal, None] = self._get_price(market)

        if not price:
            return False

        quote_symbol: str = market.quote.symbol.lower()
        total_f: float = g.config["order"]["quote_currencies"][quote_symbol]
        total: Decimal = Decimal(str(total_f))
        step: Decimal = market.step
        quantity: Decimal = (total / price).quantize(step, rounding = ROUND_DOWN) \
            if step else (total / price)

        try:
            response: dict = self._api.order_market_buy(
                    symbol = market.name,
                    quantity = quantity,
                    recvWindow = g.config["exchanges"]["binance"]["recvWindow"])
        except Exception as e:
            self._log.error(f"Order failed | {quantity} {market.base.symbol} @ "
                            f"{price} {market.quote.symbol} for a total of "
                            f"{total} {market.quote.symbol}: {e}")
            return False

        self._log.info(f"Order placed | {quantity} {market.base.symbol} @ "
                       f"{price} {market.quote.symbol} for a total of {total} "
                       f"{market.quote.symbol}.")
        self._log.debug(f"Order ID | {response['clientOrderId']}")

        return True
