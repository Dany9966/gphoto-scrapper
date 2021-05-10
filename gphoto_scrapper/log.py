import logging


def get_logger():
    return logging.getLogger(__name__)

def configure_logging(log_file, debug=False):
    log_level = logging.DEBUG if debug else logging.INFO
    formatter = logging.Formatter()
    logger = get_logger()
    logger.setLevel(log_level)

    def add_handler(h):
        h.setFormatter(formatter)
        h.setLevel(log_level)
        logger.addHandler(h)

    handler = logging.StreamHandler()
    add_handler(handler)

    handler = logging.FileHandler(log_file)
    add_handler(handler)
