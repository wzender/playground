import logging
from app.logging.log_context import get_request_id

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = get_request_id()
        return True
