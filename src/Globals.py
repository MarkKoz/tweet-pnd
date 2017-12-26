import logging

import tweepy
from bittrex import Bittrex

import Logging

config: dict = {}
log: logging.Logger = Logging.getLogger("TweetPnD")
twitter: tweepy.API = None
bittrex: Bittrex = None
