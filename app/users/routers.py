from fastapi import APIRouter, Depends, HTTPException, Response
from app.database import get_async_session
from app.users.schemas import UserRegister, UserLogin, UserInDBBase
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.dao import UserDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)


@router.post('/register')
async def register_user(user_data: UserRegister, db: AsyncSession = Depends(get_async_session)):
    get_user = await UserDAO.get_user_by_email(email=user_data.email, db=db)
    if get_user:
        raise HTTPException(status_code=500, detail="Пользователь с таким email уже присутствует")

    password_hash = get_password_hash(user_data.email)
    await UserDAO.create_user(db=db, email=user_data.email, hash_password=password_hash)


@router.post('/login')
async def login(user_data: UserLogin, response: Response, db: AsyncSession = Depends(get_async_session)) -> dict:
    user = await authenticate_user(email=user_data.email, password=user_data.password, db=db)
    if not user:
        HTTPException(status_code=400, detail="Неверный email или пароль")
    
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}


@router.get('/me', response_model=UserInDBBase)
async def get_me(db: AsyncSession = Depends(get_async_session), current_user: str = Depends(get_current_user)):
    user = await UserDAO.get_user_by_id(db=db, id=current_user)
    return user


@router.post('/logout')
async def logout(response: Response, current_user: str = Depends(get_current_user)):
    response.delete_cookie('access_token')
    return {'msg': 'Successfully logged out'}