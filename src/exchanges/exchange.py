from typing import NamedTuple
import abc

class Exchange(abc.ABC):
    Market = NamedTuple("Market", [
        ("name", str),
        ("base", str),
        ("quote", str)])
    Currency = NamedTuple("Currency", [
        ("symbol", str),
        ("name", str)])

    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    def get_markets(self):
        pass

    @abc.abstractmethod
    def buy_order(self, market: Market) -> bool:
        pass
