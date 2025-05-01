from functools import wraps
from app.logging.init_log import logger
from app.utils.truncate import truncate_value
import inspect

def log_io(func):
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            request_id = kwargs.get("request_id", "-")
            args_trunc = truncate_value(args)
            kwargs_trunc = truncate_value(kwargs)
            logger.info(f"Calling {func.__name__} with args={args_trunc}, kwargs={kwargs_trunc}", extra={"request_id": request_id})
            try:
                result = await func(*args, **kwargs)
                result_trunc = truncate_value(result)
                logger.info(f"{func.__name__} returned {result_trunc}", extra={"request_id": request_id})
                return result
            except Exception as e:
                logger.error(f"{func.__name__} raised an error: {e}", extra={"request_id": request_id})
                raise
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            request_id = kwargs.get("request_id", "-")
            args_trunc = truncate_value(args)
            kwargs_trunc = truncate_value(kwargs)
            logger.info(f"Calling {func.__name__} with args={args_trunc}, kwargs={kwargs_trunc}", extra={"request_id": request_id})
            try:
                result = func(*args, **kwargs)
                result_trunc = truncate_value(result)
                logger.info(f"{func.__name__} returned {result_trunc}", extra={"request_id": request_id})
                return result
            except Exception as e:
                logger.error(f"{func.__name__} raised an error: {e}", extra={"request_id": request_id})
                raise
        return sync_wrapper
