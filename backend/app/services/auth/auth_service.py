from app.services.auth.oauth_client import OAuthClient  # abstract class
from app.services.auth.google_oauth import GoogleOAuthClient  # Implementation of Google OAuth
from app.utils.jwt_utils import create_jwt_token
from sqlalchemy.orm import Session

from app.services.auth.user_service import get_or_create_user

class AuthService:
    def __init__(self, oauth_client: OAuthClient = GoogleOAuthClient()):
        self.oauth_client = oauth_client

    async def google_authorize(self, request):
        redirect_uri = request.url_for("auth_google_callback")
        return await self.oauth_client.authorize_redirect(request, redirect_uri)

    async def google_callback(self, request, db: Session):
        token = await self.oauth_client.authorize_access_token(request)
        user_info = token.get('userinfo')
        if user_info:
            user = get_or_create_user(db, user_info)
            return {"access_token": create_jwt_token(user), "token_type": "bearer"}
        return None
