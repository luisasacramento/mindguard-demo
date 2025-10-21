from fastapi import FastAPI
from app.middleware import exception_handler
from app.auth import router as auth_router

app = FastAPI()
app.add_exception_handler(Exception, exception_handler)

# registrar endpoints
app.include_router(auth_router)
