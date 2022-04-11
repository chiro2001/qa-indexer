import logging
from colorlog import ColoredFormatter


def get_logger():
    if logger is None:
        logger_base = logging.getLogger(None)
        logger_base.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        color_formatter = ColoredFormatter(
            '%(log_color)s%(levelname)s [%(pathname)s:%(lineno)s %(module)s %(funcName)s]'
            ' %(message)s')
        stream_handler.setFormatter(color_formatter)
        logger_base.addHandler(stream_handler)
        logger_base.setLevel(logging.INFO)
        return logger_base
    else:
        return logger


logger = None
if logger is None:
    logger = get_logger()

if __name__ == '__main__':
    # logger = get_logger()
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')
