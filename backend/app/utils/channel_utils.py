from fastapi import HTTPException, status

def is_channel_admin(user_id: str, channel) -> bool:
    if channel.admin_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the admin can perform this action"
        )
    return True
