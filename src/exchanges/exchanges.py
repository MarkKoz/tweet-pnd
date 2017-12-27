from itertools import chain
from typing import List
import inspect
import pkgutil
import sys

# All exchanges must be imported.
import exchanges.bittrex
import exchanges.binance
from exchanges.exchange import Exchange
import utils.globals as g

def get_exchange_classes() -> dict:
    def predicate(member):
        # Only subclasses of Exchange, excluding Exchange itself.
        return inspect.isclass(member) and \
               issubclass(member, Exchange) and \
               member.__module__ != "exchanges.exchange"

    # Gets qualified names of all modules of the current package.
    modules: list = [sys.modules[f"{__package__}.{name}"]
                     for _, name, _ in pkgutil.iter_modules([__package__])]

    # Gets the members of each module.
    members = chain.from_iterable(inspect.getmembers(mod, predicate)
                                  for mod in modules)

    # Converts to a dictionary with lowercase keys.
    return dict((name.lower(), val) for name, val in members)

def get_exchanges() -> List[Exchange]:
    classes: dict = get_exchange_classes()

    return [classes[name]()
            for name, v in g.config["exchanges"].items()
            if isinstance(v, dict) and v["enabled"]]
