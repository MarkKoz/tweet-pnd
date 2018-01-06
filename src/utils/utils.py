from pathlib import Path
import json
import logging

import utils.globals as g

def load_config() -> bool:
    """Loads a configuration from a file.

    Retrieves the configuration from :file:`Configuration.json`. The JSON is
    deserialised into a :class:`dictionary<dict>` and set as the
    :data:`global config<utils.globals.config>`.

    Returns
    -------
    bool
        :keyword:`True` if the configuration was successfully loaded;
        :keyword:`false` otherwise.
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
    """Creates the global Logger.

    Creates a :class:`Logger<logging.Logger>` named :any:`name` and sets it as
    the :data:`global logger<utils.globals.log>`. Messages are formatted using
    the format string ``"%(asctime)s - [%(levelname)s] %(name)s: %(message)s"``.

    The Logger uses three :class:`Handlers<logging.Handler>` to log to:

    * :abbr:`stdout (standard output)` stream with
      :attr:`logging level<logging.Handler.level>` :any:`level`.
    * :file:`log.txt` with logging level :attr:`~logging.INFO`.
    * :file:`log_debug.txt` with logging level :attr:`~logging.DEBUG`.

    Parameters
    ----------
    name: str
        The :attr:`~logging.Logger.name` of the Logger.
    level: int, optional
        The :attr:`logging level<logging.Handler.level>` of the ``stdout``
        :class:`StreamHandler<logging.StreamHandler>`.

    Returns
    -------
    logging.Logger
        The Logger which is created.
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
            filename = "log-debug.txt",
            encoding = "utf-8",
            mode = "w")
    file_handler_debug.setLevel(logging.DEBUG)
    file_handler_debug.setFormatter(formatter)
    logger.addHandler(file_handler_debug)

    g.log = logger
