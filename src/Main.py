import json

import tweepy
from tweepy import OAuthHandler

from StreamListener import StreamListener

# Loads the configuration file.
with open("Configuration.json", "r") as file:
    config = json.load(file)

# Twitter API Setup
tcfg = config["twitter"]
auth = OAuthHandler(tcfg["api"]["key"], tcfg["api"]["secret"])
auth.set_access_token(tcfg["api"]["access_token"], tcfg["api"]["access_secret"])
api = tweepy.API(auth, wait_on_rate_limit = True)

# Twitter Stream
listener = StreamListener(api.get_user(tcfg["user"]).id, tcfg["search_term"])
stream = tweepy.Stream(auth = api.auth, listener = listener, timeout = 60)
stream.filter(follow = [str(stream.listener.userID)])
# track = [tcfg["search_term"]] Better to use this but it doesn't seem to filter
# properly
