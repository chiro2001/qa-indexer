import logging
from colorlog import ColoredFormatter


def get_logger(name=__name__):
    logger_base = logging.getLogger(name)
    logger_base.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    color_formatter = ColoredFormatter('%(log_color)s%(levelname)s [%(pathname)s:%(lineno)s %(module)s %(funcName)s]'
                                       ' %(message)s')
    stream_handler.setFormatter(color_formatter)
    if not logger_base.hasHandlers():
        logger_base.addHandler(stream_handler)
    return logger_base


logger = None
if logger is None:
    logger = get_logger("spiders")

if __name__ == '__main__':
    # logger = get_logger(__name__)
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')
