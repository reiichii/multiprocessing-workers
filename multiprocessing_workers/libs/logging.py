import logging

from libs.settings import LOG_DESTINATION_PATH


def getLogger(name: str = None, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))

    return logger


def listener_configurer(queue):
    handler = logging.handlers.RotatingFileHandler(
        LOG_DESTINATION_PATH, mode="a", maxBytes=1024
    )
    formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)

    return logging.handlers.QueueListener(queue, handler)


def worker_configurer(queue):
    h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
    logger = getLogger()
    logger.addHandler(h)
    # send all messages, for demo; no other level or filter logic applied.
    logger.setLevel(logging.DEBUG)
