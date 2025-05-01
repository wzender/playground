from fastapi import APIRouter
from app.models.greeting_models import GreetingRequest, GreetingResponse
from app.services.greeting_service import create_greeting

router = APIRouter()

@router.post("/greet", response_model=GreetingResponse)
async def greet(request: GreetingRequest):
    return create_greeting(request_id=request.request_id, name=request.name)
