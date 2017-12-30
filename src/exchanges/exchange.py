from typing import NamedTuple

class Exchange:
    Market = NamedTuple("Market", [
        ("name", str),
        ("base", str),
        ("quote", str)])
    Currency = NamedTuple("Currency", [
        ("symbol", str),
        ("name", str)])

    def __init__(self, name: str):
        self.name = name

    def get_markets(self):
        return

    def buy_order(self, market: Market) -> bool:
        return False
