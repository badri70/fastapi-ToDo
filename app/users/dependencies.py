from fastapi import Depends, Request, HTTPException
from app.users.auth import decode_jwt_token
from app.users.dao import UserDAO

def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=401)

    return token


async def get_current_user(token: str = Depends(get_token)):
    user_id = int(decode_jwt_token(token=token)['sub'])
    return user_id