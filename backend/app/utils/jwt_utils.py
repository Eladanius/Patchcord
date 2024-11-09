import os
import jwt
from dotenv import load_dotenv


def create_jwt_token(user):
    load_dotenv()
    if not user:
        print("Error: user is None")
        return None
    
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    token = jwt.encode({"sub": str(user.id)}, SECRET_KEY, algorithm="HS256")
    print("Generated JWT token:", token)
    return token
