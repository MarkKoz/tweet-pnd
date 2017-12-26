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
    "bittrex": {
        "key": "",
        "secret": ""
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

#### Bittrex
* `key` - Bittrex API key.
* `secret` - Bittrex API secret.

### Requirements
* [Python 3.6](https://www.python.org/downloads/) or higher
* [tweepy](http://www.tweepy.org/)
* [python-bittrex](https://github.com/ericsomdahl/python-bittrex)

### Installation
[pipenv](https://docs.pipenv.org/) can be used to simply the installation
process. Once it is installed, `cd` into the root directory and install the
dependencies from the pipefile using the command

```bash
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
