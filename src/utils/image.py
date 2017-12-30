from typing import Union
import logging
import re

try:
    import Image
except ImportError:
    from PIL import Image
from pytesseract import pytesseract
import requests

from exchanges.exchange import Exchange
import utils.globals as g

def get_image(url: str):
    log.debug("Downloading the image.")
    return Image.open(requests.get(url, stream = True).raw)

def to_text(img) -> str:
    log.debug("Performing OCR.")
    return pytesseract.image_to_string(img)

def parse_currency(text: str) -> Union[Exchange.Currency, None]:
    log.debug("Parsing the text.")
    g.db.cursor.execute("select * from currencies")

    return next((Exchange.Currency(symbol, name)
                 for symbol, name in g.db.cursor.fetchall()
                 if re.search(name + r"[( ]*?\(?" + symbol,
                              text,
                              re.IGNORECASE)),
                None)

def init():
    global log
    log = logging.getLogger("bot.utils.image")

    if g.config["tesseract_cmd"]:
        pytesseract.tesseract_cmd = g.config["tesseract_cmd"]
