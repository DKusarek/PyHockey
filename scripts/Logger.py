import logging
import os


def make_logger(name, level, format):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.FileHandler(os.path.join('./logs/', name + '.log'), 'w')
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class Logger:
    _errlog = make_logger('ERROR', logging.ERROR, '%(asctime)s - %(name)s  - %(message)s')
    _warnlog = make_logger('WARNING', logging.WARNING, '%(asctime)s - %(name)s  - %(message)s')
    _infolog = make_logger('INFO', logging.INFO, '%(asctime)s - %(name)s  - %(message)s')
    _debuglog = make_logger('DEBUG', logging.DEBUG, '%(asctime)s - %(name)s - %(message)s')

    @staticmethod
    def info(msg, *args, **kwargs):
        Logger._infolog.info(msg, *args, **kwargs)

    @staticmethod
    def debug(msg, *args, **kwargs):
        Logger._debuglog.info(msg, *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        Logger._errlog.info(msg, *args, **kwargs)

    @staticmethod
    def warning(msg, *args, **kwargs):
        Logger._warnlog.info(msg, *args, **kwargs)

    def __init__(self):
        pass
