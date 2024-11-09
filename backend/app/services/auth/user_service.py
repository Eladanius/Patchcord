from sqlalchemy.orm import Session
from app.db.models.user import User

"""
A function to search for a user by Google ID or email.
If the user is not found, we create it based on the information received from Google.
"""

def get_or_create_user(db: Session, user_info: dict) -> User:
    google_id = user_info.get("sub")  # unique user's id by Google
    email = user_info.get("email")
    
    # search for a user by Google ID or email
    user = db.query(User).filter((User.google_id == google_id) | (User.email == email)).first()
    
    if not user:
        # If there is no user, create it
        user = User(
            google_id=google_id,
            email=email,
            username=user_info.get("name"),
            avatar_url=user_info.get("picture")
        )
        db.add(user)
        db.commit()
        db.refresh(user)  # update object for getting ID
    
    return user
