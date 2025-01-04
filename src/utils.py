import logging

def get_logger(name=None):
    logger = logging.getLogger(name or __name__)
    if not logger.hasHandlers():
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger
