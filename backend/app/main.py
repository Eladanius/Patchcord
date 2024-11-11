from typing import Annotated
from fastapi import Depends, FastAPI
import os
from fastapi.exceptions import RequestValidationError
from starlette.middleware.sessions import SessionMiddleware

from app.core.exceptions import validation_exception_handler


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))
app.add_exception_handler(RequestValidationError, validation_exception_handler)

from app.api.auth_routes import router as AuthRouter
from app.api.user_routes import router as UserRouter
from app.api.user_statuses_routes import router as UserStatusesRouter
from app.api.channel_routers import router as ChannelRouter

app.include_router(AuthRouter, prefix='/auth', tags=["auth"])
app.include_router(UserRouter, prefix='/user', tags=["user"])
app.include_router(UserStatusesRouter, prefix='/user_statuses', tags=["user statuses"])
app.include_router(ChannelRouter, prefix='/channel', tags=["channel"])
