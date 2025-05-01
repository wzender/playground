from fastapi import FastAPI
from app.middleware.logging_middleware import PostLoggingMiddleware
from app.routes import greet

app = FastAPI()
app.add_middleware(PostLoggingMiddleware)
app.include_router(greet.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
