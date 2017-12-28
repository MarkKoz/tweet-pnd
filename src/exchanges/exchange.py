from typing import List, NamedTuple

class Exchange:
    Market = NamedTuple("Market", [
        ("name", str),
        ("base", str),
        ("quote", str)])
    Currency = NamedTuple("Currency", [
        ("symbol", str),
        ("name", str)])

    def get_markets(self):
        return

    def get_active_currencies(self) -> List[Currency]:
        return []
