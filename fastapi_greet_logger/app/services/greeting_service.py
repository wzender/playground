from app.logging.init_log import logger
from app.utils.decorators import log_io
from app.models.greeting_models import GreetingResponse

@log_io
def create_greeting(request_id: int, name: str) -> GreetingResponse:
    # logger.info(f"Creating greeting for request_id_: {request_id}, name: {name}")
    message = f"Hello, {name}!"
    return GreetingResponse(request_id=request_id, message=message)
