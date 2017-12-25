import json

import tweepy

from StreamListener import StreamListener

config: dict = {}
twitter: tweepy.API = None

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
    print(f"{currency['CurrencyLong']}: "
          f"{currency['Currency']}")

def main():
    global config
    global twitter
    config = loadConfig()
    twitter = getTwitterAPI()

    stream = startStream(onTweet)

if __name__ == "__main__":
    main()
