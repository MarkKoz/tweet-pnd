import json

import tweepy
from tweepy import OAuthHandler

# Load configuration.
with open("Configuration.json", "r") as file:
    config = json.load(file)

# Twitter API
tcfg = config["twitter"]
auth = OAuthHandler(tcfg["api"]["key"], tcfg["api"]["secret"])
auth.set_access_token(tcfg["api"]["access_token"], tcfg["api"]["access_secret"])
api = tweepy.API(auth, wait_on_rate_limit = True)

# TODO: Specify since_id if it exists in the config.
for status in tweepy.Cursor(api.user_timeline, id = tcfg["user"]).items():
    # TODO: Handle truncated and/or extended tweets.
    text: str = status._json["text"].lower()

    if tcfg["search_term"] in text:
        # TODO: Search from list of available currencies on Bittrex.
        coin = text.find("rdd")
        # print(text[coin:coin + 3])
        break
