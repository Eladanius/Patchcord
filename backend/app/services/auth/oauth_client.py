from abc import ABC, abstractmethod
from starlette.requests import Request

class OAuthClient(ABC):
    @abstractmethod
    async def authorize_redirect(self, request: Request, redirect_uri: str):
        """Redirect user to auth page"""
        pass

    @abstractmethod
    async def authorize_access_token(self, request: Request):
        """Get access token after auth"""
        pass
