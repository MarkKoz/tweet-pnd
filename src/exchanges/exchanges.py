from collections import defaultdict
from decimal import Decimal
from importlib import import_module
from itertools import filterfalse
from typing import DefaultDict, List, Tuple, Union

from coinmarketcap import Market

from exchanges.exchange import Exchange
import utils.globals as g

def get_exchanges() -> List[Exchange]:
    g.log.debug("Getting exchange instances.")
    # Filters out exchanges with a priority of 0.
    exs = filterfalse(lambda item: not item[1]["priority"],
                      g.config["exchanges"].items())

    # Sorts exchanges by priority in ascending order.
    # Imports the modules, gets the classes from the modules,
    # and instantiates them.
    return [getattr(import_module("." + ex[0], "exchanges"),
                    ex[0].capitalize())()
            for ex in sorted(exs, key = lambda ex: ex[1]["priority"])]

def get_currencies() -> List[Exchange.Currency]:
    g.log.debug("Getting currencies from CoinMarketCap.")
    return list(map(lambda c: Exchange.Currency(c["symbol"], c["name"], None),
                    Market().ticker(limit = 0)))

def get_markets(currency: Exchange.Currency) -> \
        DefaultDict[str, List[Exchange.Market]]:
    g.log.debug(f"Getting markets for base currency {currency.symbol}.")
    quotes: Tuple[str] = tuple(g.config["order"]["quote_currencies"].keys())
    cases: str = "\n".join(f"when '{ex}' then {i}"
                           for i, ex in enumerate(quotes))

    g.db.cursor.execute(f"""
        select 
            e.name,
            em.name,
            m.base,
            (select precision 
             from currencies 
             where symbol = m.base 
             limit 1) base_prec,
            m.quote,
            (select precision 
             from currencies 
             where symbol = m.base 
             limit 1) quote_prec,
            m.step
        from markets m
        join exchange_markets em
                on m.id = em.market_id
        join exchanges e
                on em.exchange_id = e.id
        where
            base = upper(?) and
            lower(quote) in ({", ".join(["?"] * len(quotes))})
        order by
            e.name,
            case lower(m.quote)
                {cases}
            end
    """, (currency.symbol,) + quotes)

    results: List[Tuple[str, str, str, int, str, int, Union[str, None]]] = g.db.cursor.fetchall()
    markets: DefaultDict[str, List[Exchange.Market]] = defaultdict(list)
    g.log.debug(f"Retrieved {len(results)} markets.")

    for ex, market, base, base_prec, quote, quote_prec, step in results:
        markets[ex].append(Exchange.Market(
                market,
                Exchange.Currency(base, None, base_prec),
                Exchange.Currency(quote, None, quote_prec),
                Decimal(step) if step else None))

    return markets

def place_order(data: DefaultDict[str, List[Exchange.Market]]) -> bool:
    g.log.debug("Attempting to place an order.")

    for exchange in g.exchanges:
        if exchange.name not in data:
            g.log.debug(f"No markets were found for {exchange.name}; skipping.")
            continue

        for market in data[exchange.name]:
            result: bool = exchange.buy_order(market)

            if result:
                return True

        g.log.warning(f"Orders failed to be placed for all of {exchange.name}'s"
                      " markets.")

    g.log.warning(f"Orders failed to be placed for all exchanges.")
    return False
