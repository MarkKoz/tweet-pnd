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

### Requirements
* [Python 3.6](https://www.python.org/downloads/) or higher
* [tweepy](http://www.tweepy.org/)
* [freqtrade](https://github.com/gcarq/freqtrade)
    * On Windows, use Anaconda for [NumPy](http://www.numpy.org/) and
    [SciPy](https://www.scipy.org/) or install the wheels from
    [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/).
    * 64-bit Windows users need to instead install a
    [64-bit version](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib) of
    [ta-lib](https://github.com/mrjbq7/ta-lib).

### Installation
[pipenv](https://docs.pipenv.org/) can be used to simply the installation
process. Once it is installed, `cd` into the root directory and install the
dependencies from the pipefile using the command

```bash
pipenv install
```

Thee may be issues with it attempting to install `python-bittrex` from git. If
this is the case, simply install the package with pip before running the
command above. Because the virtualenv inherits global packages, it can be
installed either globally with `pip install` or locally with `pipenv install`.

For 64-bit Windows users, `ta-lib` needs to be installed from a wheel using
the link provided in the requirements section above. First run

```bash
pipenv uninstall ta-lib
```

and then

```bash
pipenv install <wheel-file.whl>
```

to install the package from the wheel. The same should be done for NumPy, SciPy,
and any other dependencies being installed as wheels if applicable. Afterwards,
the rest of the dependencies can be installed as normal.

### Running
Run `Main.py` to run the bot. If using pipenv:

```bash
pipenv run python Main.py
```

otherwise

```bash
python Main.py
```
