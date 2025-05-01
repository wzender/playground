import logging
from colorlog import ColoredFormatter
from app.logging.request_id_filter import RequestIdFilter
# from app.logging.cmres_log import setup_elastic_logger

formatter = ColoredFormatter(
    fmt="%(log_color)s%(levelname)-8s [%(asctime)s] [request_id=%(request_id)s] "
        "[%(threadName)s] %(filename)s:%(lineno)d in %(funcName)s() - %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
    datefmt="%Y-%m-%d %H:%M:%S"
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger = logging.getLogger("post_logger")
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)
logger.addFilter(RequestIdFilter())

# try:
#     es_handler = setup_elastic_logger()
#     logger.addHandler(es_handler)
# except Exception as e:
#     logger.warning(f"Could not attach Elasticsearch handler: {e}")

logger.propagate = False

