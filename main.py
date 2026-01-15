from fastapi import FastAPI, Body, Header
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated
from datetime import datetime

app = FastAPI()

#회원가입
class CreateUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)
    nickname: str = Field(min_length=4, max_length=8)
    profile_image: Optional[str] = None

class UserResponse(BaseModel):
    email: EmailStr
    nickname: str
    profile_image: Optional[str] = None
    created_at: datetime

@app.post("/users/", response_model=UserResponse)
async def signup(user_in: CreateUser):
    return{
        "email": user_in.email,
        "nickname": user_in.nickname,
        "profile_image": user_in.profile_image,
        "created_at": datetime.now()
    }

# 로그인
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)


class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int = 3600
    sign_in_at: datetime

class LoginResponse(BaseModel):
    status: str
    data: TokenData

@app.post("/auth/token", response_model=LoginResponse)
async def login_access_token(
        token_in: LoginRequest,
        authorization: Annotated[str | None, Header()] = None
):

    return {
        "status": "success",
        "data": {
            "access_token": "temp_access_token",
            "refresh_token": "temp_refresh_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "sign_in_at": datetime.now()
        }
    }