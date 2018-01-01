from pathlib import Path
import json
import logging

import utils.globals as g

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
        with open("config.json", "r") as file:
            g.config = json.load(file)

        return True
    except EnvironmentError as e:
        g.log.error("An error occurred trying to load the configuration file "
                    f"from '{Path('config.json').resolve().absolute()}'. Ensure"
                    " it exists and the bot has adequate permissions to access "
                    f"the file: {e}")
    except json.decoder.JSONDecodeError as e:
        g.log.error("A JSON syntax error was encountered while trying to parse "
                    f"the configuration: {e}")
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
    formatter: logging.Formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] %(name)s: %(message)s")

    handler: logging.Handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    file_handler: logging.Handler = logging.FileHandler(
            filename = "log.txt",
            encoding = "utf-8",
            mode = "w")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    file_handler_debug: logging.Handler = logging.FileHandler(
            filename = "log_debug.txt",
            encoding = "utf-8",
            mode = "w")
    file_handler_debug.setLevel(logging.DEBUG)
    file_handler_debug.setFormatter(formatter)
    logger.addHandler(file_handler_debug)

    g.log = logger
