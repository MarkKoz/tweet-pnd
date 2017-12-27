from typing import List
import logging

from exchanges.exchange import Exchange

config: dict = {}
log: logging.Logger = None
exchanges: List[Exchange] = []
