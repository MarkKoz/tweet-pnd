from typing import Optional
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

def get_image(url: str) -> Image.Image:
    """Creates an Image object from a URL.

    Requests an image from :any:`url` and constructs an
    :class:`~PIL.Image.Image` object from it.

    Notes
    -----
    Requests the image using :abbr:`HTTP (Hypertext Transfer Protocol)` GET.

    Parameters
    ----------
    url: str
        The :abbr:`URL (Uniform Resource Locator)` from which to request the
        image.

    Returns
    -------
    PIL.Image.Image
        The :class:`~PIL.Image.Image` object created from the image at the given
        :abbr:`URL (Uniform Resource Locator)`.
    """
    log.debug("Downloading the image.")
    return Image.open(requests.get(url, stream = True).raw)

def to_text(img: Image.Image) -> str:
    """Performs OCR on an image.

    Performs :abbr:`OCR (optical character recognition)` on the
    :class:`~PIL.Image.Image` :any:`img` and returns the resulting string.

    Notes
    -----
    OCR is performed using :mod:`pytesseract`.

    Parameters
    ----------
    img: Image.Image
        The image on which to perform OCR.

    Returns
    -------
    str
        The resulting text from OCR.
    """
    log.debug("Performing OCR.")
    return pytesseract.image_to_string(img)

def parse_currency(text: str) -> Optional[Exchange.Currency]:
    """Finds a currency in a string.

    Searches for a currency in the string :any:`text` and returns the first
    match.

    Notes
    -----
    Queries the database for all currencies and iterates them. Uses a regular
    expression to find a match in the text and constructs a
    :class:`~Exchange.Currency` from it.

    Parameters
    ----------
    text: str
        The string in which to search for a currency.

    Returns
    -------
    Exchange.Currency or None
        The first matching currency found in the string, or :any:`None` if no
        matches are found.
    """
    log.debug("Searching for a currency in the text.")
    g.db.cursor.execute("select * from currencies")

    return next((Exchange.Currency(symbol, name, precision)
                 for symbol, name, precision in g.db.cursor.fetchall()
                 if re.search((name if g.config["search_currency_name"] else "")
                                  + r"\s*?[(\[{]+?\s*?" + symbol + r"\s*?[)\]}]",
                              text,
                              re.IGNORECASE)),
                None)

def init() -> None:
    """Initialises the module.

    Creates a global Logger and sets the
    :attr:`path to Tesseract<pytesseract.pytesseract.tesseract_cmd>` if given.

    Returns
    -------
    None
    """
    global log
    log = logging.getLogger("bot.utils.image")

    if g.config["tesseract_cmd"]:
        pytesseract.tesseract_cmd = g.config["tesseract_cmd"]
