from collections import defaultdict
from importlib import import_module
from itertools import filterfalse
from typing import DefaultDict, List, Tuple

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
    return list(map(lambda c: Exchange.Currency(c["symbol"], c["name"]),
                    Market().ticker(limit = 0)))

def get_markets(currency: Exchange.Currency) -> DefaultDict[str, List[str]]:
    g.log.debug(f"Getting markets for base currency {currency.symbol}.")
    quotes: Tuple[str] = tuple(g.config["order"]["quote_currencies"])
    cases: str = "\n".join(f"when '{ex}' then {i}" for i, ex in enumerate(quotes))

    g.db.cursor.execute(f"""
        select 
            e.name,
            em.name
        from markets m
        join exchange_markets em
                on m.id = em.market_id
        join exchanges e
                on em.exchange_id = e.id
        where
            base = ? and
            lower(quote) in ({", ".join(["?"] * len(quotes))})
        order by
            e.name,
            case lower(m.quote)
                {cases}
            end
    """, (currency.symbol,) + quotes)

    results: Tuple[str, str] = g.db.cursor.fetchall()
    markets: DefaultDict[str, List[str]] = defaultdict(list)

    for ex, market in results:
        markets[ex].append(market)

    return markets

def place_order(data: DefaultDict[str, List[str]]) -> bool:
    exchanges: List[Exchange] = get_exchanges()

    for exchange, markets in data.items():
        ex: Exchange = next(ex for ex in exchanges if ex.name == exchange)

        for market in markets:
            return True
