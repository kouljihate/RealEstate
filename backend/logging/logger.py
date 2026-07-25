import json
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from shared.constants import LOG_DATE_FORMAT, LOG_FORMAT

_LOG_CONFIGURED = False


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record, LOG_DATE_FORMAT),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra_data"):
            log_entry["extra"] = record.extra_data
        return json.dumps(log_entry)


class StructuredLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, **kwargs):
        if extra is None:
            extra = {}
        if "extra_data" not in extra:
            extra["extra_data"] = {}
        super()._log(level, msg, args, exc_info=exc_info, extra=extra)


logging.setLoggerClass(StructuredLogger)


def get_logger(name: str) -> StructuredLogger:
    logger = logging.getLogger(name)
    return logger  # type: ignore


def setup_logging(log_file: str = "logs/app.log", level: str = "DEBUG") -> None:
    global _LOG_CONFIGURED
    if _LOG_CONFIGURED:
        return

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    log_level = getattr(logging, level.upper(), logging.DEBUG)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
    root_logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10_485_760,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(JSONFormatter(LOG_DATE_FORMAT))
    root_logger.addHandler(file_handler)

    _LOG_CONFIGURED = True
    logger = get_logger(__name__)
    logger.info("Logging initialized", extra={"extra_data": {"log_file": log_file, "level": level}})
