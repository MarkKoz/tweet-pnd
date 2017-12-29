from importlib import import_module
from itertools import filterfalse
from typing import List

from coinmarketcap import Market

from exchanges.exchange import Exchange
import utils.globals as g

def get_exchanges() -> List[Exchange]:
    # Filters out exchanges with a priority of 0.
    exs = filterfalse(lambda item: not item[1]["priority"],
                      g.config["exchanges"].items())

    # Sorts exchanges by priority in ascending order.
    # Imports the modules, gets the classes from the modules,
    # and instantiates them.
    return [getattr(import_module("." + ex[0], "exchanges"),
                    ex[0].capitalize())()
            for ex in sorted(exs, key = lambda ex: ex[1]["priority"])]

def get_currencies():
    return list(map(lambda c: Exchange.Currency(c["symbol"], c["name"]),
                    Market().ticker(limit = 0)))
