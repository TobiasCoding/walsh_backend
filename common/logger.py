# common/logger.py
import logging, sys, json


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "service": "file_service",  # o set dinámico desde env
            "message": record.getMessage(),
        }
        return json.dumps(log)


def get_logger(name="app", level=logging.INFO):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
