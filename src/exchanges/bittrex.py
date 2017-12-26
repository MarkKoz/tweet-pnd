import logging

from bittrex import Bittrex as bx

from utils import globals as g

class Bittrex:
    def __init__(self):
        self._log: logging.Logger = logging.getLogger("bot.exchanges.Bittrex")
        self._api: bx = self._get_api()

    def _get_api(self) -> bx:
        key: str = g.config["bittrex"]["key"]
        secret: str = g.config["bittrex"]["secret"]

        if not key:
            self._log.warning("Key is missing from the config.")

        if not secret:
            self._log.warning("Secret is missing from the config.")

        return bx(g.config["bittrex"]["key"], g.config["bittrex"]["secret"])

    def get_currencies(self) -> list:
        currencies: dict = self._api.get_currencies()

        if not currencies["success"]:
            raise RuntimeError("The currencies could not be retrieved from "
                               "Bittrex.")

        currencies = currencies["result"]
        self._log.info(f"Retrieved {len(currencies)} currencies from Bittrex.")

        return currencies

    def get_active_currencies(self, currencies: list = None) -> list:
        if not currencies:
            currencies = self.get_currencies()

        active = [c for c in currencies if c["IsActive"]]

        self._log.info(f"Narrowed down to {len(active)} active currencies.")

        return active
