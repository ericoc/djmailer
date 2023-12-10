import logging
from logging.config import dictConfig


# Taken from https://github.com/nvie/rq/blob/master/rq/logutils.py
def setup_loghandlers(level=None):
    # Setup logging for mailmod if not already configured
    logger = logging.getLogger('mailmod')
    if not logger.handlers:
        dictConfig({
            "version": 1,
            "disable_existing_loggers": False,

            "formatters": {
                "mailmod": {
                    "format": "[%(levelname)s]%(asctime)s PID %(process)d: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },

            "handlers": {
                "mailmod": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "mailmod"
                },
            },

            "loggers": {
                "mailmod": {
                    "handlers": ["mailmod"],
                    "level": level or "DEBUG"
                }
            }
        })
    return logger
