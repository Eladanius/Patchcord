from typing import Annotated
from fastapi import Depends, FastAPI
import os
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/google")


app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

from app.api.auth.auth_routes import router as AuthRouter
from app.api.user.user_routes import router as UserRouter

app.include_router(AuthRouter, tags=["auth"])
app.include_router(UserRouter, tags=["user"])
