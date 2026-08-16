import json
import logging
from datetime import datetime, timezone
from pathlib import Path


class JsonLineFormatter(logging.Formatter):
    """Format each log record as one JSON object for easy parsing."""

    _standard_fields = set(logging.makeLogRecord({}).__dict__)

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        log_entry.update(
            {
                key: value
                for key, value in record.__dict__.items()
                if key not in self._standard_fields and not key.startswith("_")
            }
        )
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry, default=str, ensure_ascii=False)


def get_logger(name: str) -> logging.Logger:
    """Return a logger that writes JSON Lines to <project-root>/logs/app.jsonl."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logs_directory = Path(__file__).resolve().parents[2] / "logs"
    logs_directory.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(logs_directory / "app.jsonl", encoding="utf-8")
    handler.setFormatter(JsonLineFormatter())
    logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JsonLineFormatter())
    logger.addHandler(console_handler)

    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
