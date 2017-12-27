import logging

import tweepy

from twitter.stream_listener import StreamListener
import utils.globals as g

class Twitter:
    def __init__(self, callback = None):
        self._log: logging.Logger = logging.getLogger("bot.twitter.Twitter")
        self._api: tweepy.API = self._get_api()

        self.stream: tweepy.Stream = self._start_stream(callback)

    def _get_api(self) -> tweepy.API:
        """
        Creates a Tweepy API object from the configuration.

        Returns
        -------
        tweepy.API
            The API object.
        """
        config = g.config["twitter"]["api"]
        key: str = config["key"]
        secret: str = config["secret"]

        # TODO: Raise exceptions here, or better yet, when loading the config.
        if not key:
            self._log.warning("Client key is empty!")

        if not secret:
            self._log.warning("Client secret is empty!")

        auth = tweepy.OAuthHandler(key, secret)

        token: str = config["access_token"]
        secret = config["access_secret"]

        if token and secret:
            auth.set_access_token(token, secret)
        else:
            self._log.warning("Access tokens are empty.")

        return tweepy.API(auth, wait_on_rate_limit = True)

    def _start_stream(self, callback) -> tweepy.Stream:
        """
        Creates and starts an asynchronous :class:`stream<tweepy.Stream>` of the
        user's tweets which match the search term in the configuration.

        Note
        -------
        Stream filter parameters behave like an OR rather than an AND.
        Therefore, the track parameter is not used. Instead, tweets are further
        filtered in the :class:`StreamListener` using the search term.

        Parameters
        ----------
        callback
            The function to execute when a desired tweet is successfully found.

        Returns
        -------
        tweepy.Stream
            The stream which is created.
        """
        user: int = self.id_from_name(g.config["twitter"]["user"])

        listener: StreamListener = StreamListener(user, callback)
        stream: tweepy.Stream = tweepy.Stream(auth = self._api.auth,
                                              listener = listener)
        stream.filter(async = True, follow = [str(stream.listener.user)])

        return stream

    def id_from_name(self, name: str) -> int:
        """
        Retrieves the ID of a user using the user's screen name
        (twitter handle).

        Parameters
        ----------
        name
            The screen name (Twitter handle) of the user.

        Returns
        -------
            The ID of the user.
        """
        try:
            return self._api.get_user(name).id
        except tweepy.TweepError as e:
            if e.api_code == 50:
                self._log.error(f"The user '{name}' could not be found!")
            if e.api_code == 63:
                self._log.error(f"The user '{name}' has been suspended. It "
                                f"won't possible to retrieve information.")
            pass
