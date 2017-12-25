import tweepy
from bittrex import Bittrex

class StreamListener(tweepy.StreamListener):
    config: dict = {}
    bittrex: Bittrex = None

    def __init__(self, cfg, user, callback = None):
        global config
        global bittrex
        config = cfg
        bittrex = Bittrex(config["bittrex"]["key"],
                          config["bittrex"]["secret"],
                          api_version = "v2.0")

        super(StreamListener, self).__init__()

        self.user = user
        self.currencies = bittrex.get_currencies()
        self.callback = callback

        if not self.currencies["success"]:
            raise RuntimeError("The currencies could not be retrieved from "
                               "Bittrex.")

        self.currencies = self.currencies["result"]

    def on_status(self, status):
        print(f"{status.author.screen_name}\t{status.text}")

        # Only parses statuses by the author; ignores retweets, replies, etc.
        if status.author.id == self.user:
            print("Message by the author found.")

            # If a search term was specified, ignores statuses which don't
            # contain the search term.
            # if self.searchTerm and self.searchTerm.lower() not in status.text.lower():
            #     return

            # Finds the first currency whose long name is found in the text of
            # the status. None if no match is found.
            currency = next((currency for currency in self.currencies
                             if currency["CurrencyLong"] in status.text or
                             currency["Currency"] in status.text),
                            None)

            # Prints the name of currency market if one was found.
            if currency:
                self.callback(currency)

    def on_error(self, status_code):
        if status_code == 420:
            # TODO: Handle rate limiting properly instead of closing the stream.
            print("Being rate limited. Stream closing.")
            return False

        print(f"Error with code: {status_code}")
        return True

    def on_timeout(self):
        print("Stream timed out.")
        return True
