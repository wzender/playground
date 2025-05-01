import logging
from colorlog import ColoredFormatter
from app.logging.request_id_filter import RequestIdFilter

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)s: [request_id=%(request_id)s] %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger("post_logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addFilter(RequestIdFilter())  # Inject request_id from context
logger.propagate = False
