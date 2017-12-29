from importlib import import_module
from itertools import filterfalse
from typing import List

from coinmarketcap import Market

from exchanges.exchange import Exchange
import utils.globals as g

def get_exchanges() -> List[Exchange]:
    # Filter out exchanges with a priority of 0.
    exchange_names = filterfalse(lambda item: not item[1]["priority"],
                                 g.config["exchanges"].items())

    # Sort exchanges by priority in ascending order.
    exs: List[str] = sorted(exchange_names, key = lambda ex: ex[1]["priority"])

    # Imports the modules, gets the classes from the modules, and instantiates
    # them.
    return [getattr(import_module("." + ex[0], "exchanges"),
                    ex[0].capitalize())()
            for ex in exs]

def get_currencies():
    return list(map(lambda c: Exchange.Currency(c["symbol"], c["name"]),
                    Market().ticker(limit = 0)))
