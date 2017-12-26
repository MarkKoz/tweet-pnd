# Tweet Pump-and-Dump
### Description
Performs trades on Bittrex based on tweets of a user. Searches tweets for any
mentions of currencies available on Bittrex. Optionally searches for a key
term/phrase first before searching for currencies.

### Configuration
A file named `Configuration.json` and in the same directory as `bot.py` is used
for configuration of the bot. Below is the base configuration for the bot:

```json
{
    "twitter": {
        "api": {
            "key": "",
            "secret": "",
            "access_token": "",
            "access_secret": ""
        },
        "user": "",
        "search_term": ""
    },
    "exchanges": {
        "binance": {
            "enabled": false,
            "key": "",
            "secret": ""
        },
        "bittrex": {
            "enabled": true,
            "key": "",
            "secret": ""
        },
        "preferred": "bittrex"
    }
}
```

#### Twitter
* `key` - Consumer key (API key)
* `secret` - Consumer secret (API secret)
* `access_token` - Access token; can be used to make API requests on your own
account's behalf.
* `access_secret` - Access secret
* `user` - The Twitter handle of the user whose tweets will be read.
* `search_term` - A search term to use to filter the user's tweets; ignored if
empty.

#### Exchanges
* `enabled` - `true` if this exchange should be used; `false` otherwise.
* `key` -  The exchange's API key.
* `secret` - The exchange's API secret.
* `preferred` - The name of the preferred exchange; it will have the highest
priority when selecting the exchange on which to place an order.

### Requirements
* [Python 3.6](https://www.python.org/downloads/) or higher
* [tweepy](http://www.tweepy.org/)
* [pytesseract](https://github.com/madmaze/pytesseract)
    * Requires
    [Google Tesseract OCR](https://github.com/tesseract-ocr/tesseract) to be
    installed and present in the system's `PATH`. See
    [this](https://github.com/tesseract-ocr/tesseract/wiki) page for more
    specific installation instructions.
* [python-binance](https://github.com/sammchardy/python-binance)
* [python-bittrex](https://github.com/ericsomdahl/python-bittrex)

### Installation
[pipenv](https://docs.pipenv.org/) can be used to simply the installation
process. Once it is installed, `cd` into the root directory and install the
dependencies from the pipefile with

```bash
pipenv install
```

An error may occur while installing python-binance on Windows. More specifically

> Failed building wheel for Twisted

The error can be circumvented by downloading a pre-built wheel of Twisted from
[here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted). Download the
32-bit or 64-bit version depending on your OS and move the file into the root
directory of the program. To install Twisted and finish the installation of
python-binance run

```bash
pipenv install twisted-wheel-file-name.whl
pipenv install
```

### Running
Run `bot.py` to run the bot. If using pipenv:

```bash
pipenv shell
cd src
python bot.py
```

otherwise

```bash
python bot.py
```
