from typing import List, NamedTuple

class Exchange:
    Currency = NamedTuple("Currency", [("name", str), ("symbol", str)])

    def get_active_currencies(self) -> List[Currency]:
        return []
