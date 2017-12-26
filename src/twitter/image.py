try:
    import Image
except ImportError:
    from PIL import Image
from pytesseract import pytesseract
import requests

from utils import globals as g

def get_image(url: str):
    return Image.open(requests.get(url, stream = True).raw)

def to_text(img):
    return pytesseract.image_to_string(img)

def init():
    if g.config["tesseract_cmd"]:
        pytesseract.tesseract_cmd = g.config["tesseract_cmd"]
