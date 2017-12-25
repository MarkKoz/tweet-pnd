import json
import logging

import tweepy

from StreamListener import StreamListener

config: dict = {}
twitter: tweepy.API = None
log: logging.Logger = None

def loadConfig() -> dict:
    """
    Retrieves the configuration from Configuration.json. The JSON is
    deserialised into a :class:`dictionary<dict>`.

    Returns
    -------
    dict
        The configuration.
    """
    with open("Configuration.json", "r") as file:
        return json.load(file)

def getTwitterAPI() -> tweepy.API:
    """
    Creates a Tweepy API object from the configuration.

    Returns
    -------
    tweepy.API
        The API object.
    """
    apicfg = config["twitter"]["api"]
    auth = tweepy.OAuthHandler(apicfg["key"], apicfg["secret"])

    token: str = apicfg["access_token"]
    secret: str = apicfg["access_secret"]

    if token and secret:
        auth.set_access_token(token, secret)

    return tweepy.API(auth, wait_on_rate_limit = True)

def startStream(callback) -> tweepy.Stream:
    """
    Creates and starts a :class:`stream<tweepy.Stream>` of the user's tweets
    which match the search term in the configuration and contain a Bittrex
    currency.

    Parameters
    ----------
    callback
        The function to execute when a desired tweet is successfully found.

    Returns
    -------
    tweepy.Stream
        The stream which is created.
    """
    id: int = twitter.get_user(config["twitter"]["user"]).id

    listener: StreamListener = StreamListener(config, log, id, callback)
    stream: tweepy.Stream = tweepy.Stream(auth = twitter.auth,
                                          listener = listener)
    searchTerm: str = config["twitter"]["search_term"]

    if searchTerm:
        stream.filter(async = True,
                      follow = [str(stream.listener.user)],
                      track = [searchTerm])
    else:
        stream.filter(async = True, follow = [str(stream.listener.user)])

    return stream

def onTweet(currency) -> None:
    """
    The callback used when a desired tweet is successfully found.

    Parameters
    ----------
    currency
        The currency found in the tweet.

    Returns
    -------
    None
    """
    log.info(f"Currency | {currency['CurrencyLong']} ({currency['Currency']})")

def startLogger() -> logging.Logger:
    """
    Creates and starts a logger named 'TweetPnD'.

    Returns
    -------
    logging.Logger
        The logger which is created.
    """
    logger: logging.Logger = logging.getLogger("TweetPnD")
    logger.setLevel(logging.INFO)

    handler: logging.Handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] "
                                           "%(name)s: %(message)s"))
    logger.addHandler(handler)

    return logger

def main() -> None:
    global config
    global twitter
    global log
    config = loadConfig()
    twitter = getTwitterAPI()
    log = startLogger()

    stream: tweepy.Stream = startStream(onTweet)

    while True:
        inp: str = input("Enter 'exit' at any time to disconnect from the "
                         "stream.\n")

        if inp.lower() == "exit":
            log.info("Disconnecting from the stream.")
            stream.disconnect()
            break

    log.info("Steam has been disconnected. The program will now close.")

if __name__ == "__main__":
    main()
