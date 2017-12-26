from twitter.twitter import Twitter
from utils import globals as g, utils

def main() -> None:
    utils.get_logger("bot")

    if not utils.load_config():
        return

    twitter = Twitter()

    while twitter.stream.running:
        inp: str = input("Enter 'exit' at any time to disconnect from the "
                         "stream.\n")

        if inp.lower() == "exit":
            g.log.info("Disconnecting from the stream.")
            twitter.stream.disconnect()
            break

    g.log.info("Steam has disconnected. The program will now close.")

if __name__ == "__main__":
    main()
