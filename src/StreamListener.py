import tweepy

class StreamListener(tweepy.StreamListener):
    def __init__(self, userID, searchTerm = None):
        super(StreamListener, self).__init__()

        self.userID = userID
        self.searchTerm = searchTerm
        self.markets = [] # TODO: Get available markets from Bittrex.

    def on_status(self, status):
        print(f"{status.author.screen_name}\t{status.text}")

        # Only parses statuses by the author; ignores retweets, replies, etc.
        if str(status.author.id) == self.userID:
            print("Message by the author found.")

            # If a search term was specified, ignores statuses which don't
            # contain the search term.
            if self.searchTerm and self.searchTerm not in status.text:
                return

            # Finds the first market whose long name is found in the text of the
            # status. None if no match is found.
            market = next((market for market in self.markets
                           if market["MarketCurrencyLong"] in status.text),
                          None)

            # Prints the name of the market if one was found.
            if market:
                print(f"{market['MarketCurrencyLong']}: "
                      f"{market['MarketCurrency']}")

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
