from pydantic import BaseModel

class GreetingRequest(BaseModel):
    request_id: int
    name: str

class GreetingResponse(BaseModel):
    request_id: int
    message: str
