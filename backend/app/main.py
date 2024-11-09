from fastapi import FastAPI
import os
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

from app.api.auth.auth_routes import router as AuthRouter
app.include_router(AuthRouter, tags=["auth"])