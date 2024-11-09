from authlib.integrations.starlette_client import OAuth
import os
from starlette.requests import Request
from app.services.auth.oauth_client import OAuthClient  # abstract class

class GoogleOAuthClient(OAuthClient):
    def __init__(self):
        self.oauth = OAuth()
        self.oauth.register(
            name='google',
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            client_kwargs={'scope': 'openid profile email'}
        )

    async def authorize_redirect(self, request: Request, redirect_uri: str):
        return await self.oauth.google.authorize_redirect(request, redirect_uri)

    async def authorize_access_token(self, request: Request):
        return await self.oauth.google.authorize_access_token(request)
