import logging


def _get_handler():
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter())
    return handler


def get_logger(name: str):
    logger = logging.getLogger("GardeningLogger {}".format(name))
    logger.addHandler(_get_handler())
    return logger
