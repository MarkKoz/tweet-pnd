from itertools import chain, filterfalse
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
               member is not Exchange

    # Gets qualified names of all modules of the current package.
    modules: list = [sys.modules[f"{__package__}.{name}"]
                     for _, name, _ in pkgutil.iter_modules([__package__])]

    # Gets the members of each module.
    members = chain.from_iterable(inspect.getmembers(mod, predicate)
                                  for mod in modules)

    # Converts to a dictionary with lowercase keys.
    return dict((name.lower(), value) for name, value in members)

def get_exchanges() -> List[Exchange]:
    classes: dict = get_exchange_classes()
    print(classes)

    # Filter out exchanges with a priority of 0.
    exs = filterfalse(lambda item: not item[1]["priority"],
                      g.config["exchanges"].items())

    # Sort exchanges by priority in ascending order.
    srt = sorted(exs, key = lambda ex: ex[1]["priority"])

    # Construct an instance for each exchange.
    return list(map(lambda ex: classes[ex[0]](), srt))
