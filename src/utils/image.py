from typing import List, NamedTuple, Union
import logging
import re

try:
    import Image
except ImportError:
    from PIL import Image
from pytesseract import pytesseract
import requests

from exchanges import exchanges as exs
from exchanges.exchange import Exchange
import utils.globals as g

ParseResult = NamedTuple("ParseResult", [("exchange", Exchange),
                                         ("currency", Exchange.Currency)])

def get_image(url: str):
    log.debug("Downloading the image.")
    return Image.open(requests.get(url, stream = True).raw)

def to_text(img) -> str:
    log.debug("Performing OCR.")
    return pytesseract.image_to_string(img)

def parse_currency(text: str) -> Union[ParseResult, None]:
    log.debug("Parsing the text.")

    for ex in exchanges:
        currencies: List[Exchange.Currency] = ex.get_active_currencies()
        currency: Union[Exchange.Currency, None] = next(
                (c for c in currencies
                 if re.search(c.name + r"[( ]*?\(?" + c.symbol,
                              text,
                              re.IGNORECASE)),
                None)

        if currency:
            return ParseResult(ex, currency)

    return None

def init():
    global log
    global exchanges

    log = logging.getLogger("bot.utils.image")
    exchanges = exs.get_exchanges()

    if g.config["tesseract_cmd"]:
        pytesseract.tesseract_cmd = g.config["tesseract_cmd"]
