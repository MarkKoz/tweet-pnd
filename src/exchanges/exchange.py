from decimal import Decimal
from typing import List, NamedTuple, Union
import abc

class Exchange(abc.ABC):
    Currency = NamedTuple("Currency", [
        ("symbol", str),
        ("name", Union[str, None]),
        ("precision", Union[int, None])])

    Market = NamedTuple("Market", [
        ("name", str),
        ("base", Currency),
        ("quote", Currency),
        ("step", Union[Decimal, None])])

    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    def get_markets(self) -> List[Market]:
        pass

    @abc.abstractmethod
    def buy_order(self, market: Market) -> bool:
        pass
