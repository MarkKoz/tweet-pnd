import logging

def getLogger(name: str, level: int = logging.INFO) -> logging.Logger:
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

    return logger
