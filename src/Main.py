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
    Dict
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
    auth.set_access_token(apicfg["access_token"],
                          apicfg["access_secret"])

    return tweepy.API(auth, wait_on_rate_limit = True)

def startStream(callback) -> tweepy.Stream:
    """
    Creates and starts a :class:`stream<tweepy.Stream>` of the user's tweets
    which match the search term in the configuration and contain a Bittrex
    currency.

    Returns
    -------
    None
    """
    listener = StreamListener(config,
                              log,
                              twitter.get_user(config["twitter"]["user"]).id,
                              callback)
    stream = tweepy.Stream(auth = twitter.auth,
                           listener = listener)
    searchTerm: str = config["twitter"]["search_term"]

    if searchTerm:
        stream.filter(async = True,
                      follow = [str(stream.listener.user)],
                      track = [searchTerm])
    else:
        stream.filter(async = True, follow = [str(stream.listener.user)])

    return stream

def onTweet(currency: dict) -> None:
    log.info(f"Currency | {currency['CurrencyLong']} ({currency['Currency']})")

def startLogger() -> logging.Logger:
    logger: logging.Logger = logging.getLogger("TweetPnD")
    logger.setLevel(logging.INFO)

    handler: logging.Handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] "
                                           "%(name)s: %(message)s"))
    logger.addHandler(handler)

    return logger

def main():
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
