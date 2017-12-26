import json

import tweepy
from bittrex import Bittrex

import Globals as g
import Logging
from StreamListener import StreamListener

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
    apicfg = g.config["twitter"]["api"]
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

    Note
    -------
    Stream filter parameters behave like an OR rather than an AND. Therefore,
    the track parameter is not used. Instead, tweets are further filtered in the
    :class:`StreamListener`.

    Parameters
    ----------
    callback
        The function to execute when a desired tweet is successfully found.

    Returns
    -------
    tweepy.Stream
        The stream which is created.
    """
    user: int = g.twitter.get_user(g.config["twitter"]["user"]).id

    listener: StreamListener = StreamListener(user, callback)
    stream: tweepy.Stream = tweepy.Stream(auth = g.twitter.auth,
                                          listener = listener)
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
    g.log.info(f"Currency | {currency['CurrencyLong']} "
               f"({currency['Currency']})")
    # TODO: Check if currency is currently active.

def main() -> None:
    g.config = loadConfig()
    g.twitter = getTwitterAPI()
    g.bittrex = Bittrex(g.config["bittrex"]["key"],
                        g.config["bittrex"]["secret"],
                        api_version = "v2.0")

    stream: tweepy.Stream = startStream(onTweet)

    while stream.running:
        inp: str = input("Enter 'exit' at any time to disconnect from the "
                         "stream.\n")

        if inp.lower() == "exit":
            g.log.info("Disconnecting from the stream.")
            stream.disconnect()
            break

    g.log.info("Steam has been disconnected. The program will now close.")

if __name__ == "__main__":
    main()
