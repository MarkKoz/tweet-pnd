import json
import logging

from utils import globals as g

def load_config() -> bool:
    """
    Retrieves the configuration from Configuration.json. The JSON is
    deserialised into a :class:`dictionary<dict>`.

    Returns
    -------
    bool
        True if the configuration was successfully loaded; false otherwise.
    """
    try:
        with open("Configuration.json", "r") as file:
            g.config = json.load(file)

        return True
    except EnvironmentError:
        g.log.error("An error occurred trying to load the configuration "
                    "file. Ensure it exists, the bot has adequate "
                    "permissions to access the file, and it is formatted "
                    "properly.")
        return False

def get_logger(name: str, level: int = logging.INFO):
    """
    Creates and starts a logger with the given name and logging level.

    Parameters
    ----------
    name: str
        The name of the logger.
    level: int, optional
        The logging level of the logger.

    Returns
    -------
    logging.Logger
        The logger which is created.
    """
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(level)

    handler: logging.Handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] "
                                           "%(name)s: %(message)s"))
    logger.addHandler(handler)
    g.log = logger
