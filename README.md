# Tweet Pump-and-Dump
### Description
Performs trades on Bittrex based on tweets of a user. Searches tweets for any
mentions of currencies available on Bittrex. Optionally searches for a key
term/phrase first before searching for currencies.

### Configuration
A file named `Configuration.json` and in the same directory as `Main.py` is used
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
        "search_term": "",
        "last_tweet_id": ""
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
* `last_tweet_id` - The ID of the last tweet found which met the search
criteria; there is no need to manually configure this.

#### Bittrex
* `key` - Bittrex API key.
* `secret` - Bittrex API secret.

### Running
Run `Main.py` to run the bot.

```bash
python Main.py
```

### Requirements
* [Python 3.6](https://www.python.org/downloads/) or higher
* [tweepy](http://www.tweepy.org/)
* [freqtrade](https://github.com/gcarq/freqtrade)
    * Windows users need to instead install a
    [64-bit version](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib) of
    [ta-lib](https://github.com/mrjbq7/ta-lib).
