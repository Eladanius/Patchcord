from fastapi import HTTPException
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
        try:
            # Получаем токен доступа от Google
            token = await self.oauth_client.authorize_access_token(request)
            print("Access token:", token)  # Отладочное сообщение для токена

            # Получаем информацию о пользователе с помощью токена
            user_info = token.get('userinfo')
            if not user_info:
                raise HTTPException(status_code=400, detail="User info not found")

            print('User info:', user_info)
            # Логика создания или поиска пользователя в БД
            user = get_or_create_user(db, user_info)
            jwt_token = create_jwt_token(user)

            return {"access_token": jwt_token, "token_type": "bearer"}

        except Exception as e:
            print("Error in google_callback:", e)  # Отладочное сообщение для ошибки
            return None
