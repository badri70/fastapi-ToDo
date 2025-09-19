from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserRegister(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True