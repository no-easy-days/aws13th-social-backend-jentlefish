from fastapi import FastAPI, Body, Header, Path
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
    nickname: str = Field(min_length=4, max_length=8)
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

# 프로필 조회
class ProfileResponseData(BaseModel):
    email: EmailStr
    nickname: str = Field(min_length=4, max_length=8)
    profile_image: Optional[str] = None
    created_at: datetime

class ProfileResponse(BaseModel):
    status: str
    data: ProfileResponseData

@app.get("/users/{nickname}", response_model=ProfileResponse)
async def get_profile(nickname: str):
    return {
        "status": "success",
        "data": {
            "email": "email",
            "nickname": nickname,
            "profile_image": "profile_image",
            "created_at": "created_at"
        }
    }


# 프로필 수정
class EditProfile(BaseModel):
    nickname: str = Field(min_length=4, max_length=8)
    profile_image: Optional[str] = None
    password: str = Field(min_length=8, max_length=16)

class EditProfileData(BaseModel):
    nickname: str = Field(min_length=4, max_length=8)
    profile_image: Optional[str] = None
    updated_at: datetime

class EditProfileResponse(BaseModel):
    status: str
    data: EditProfileData

@app.patch("/users/{nickname}", response_model=EditProfileResponse)
async def update_profile(nickname: str):
    return {
        "status": "success",
        "data": {
            "nickname": nickname,
            "profile_image": "profile_image",
            "updated_at": datetime.now()
        }
    }

# 회원 탈퇴
class DeleteProfileResponse(BaseModel):
    status: str
    message: str

@app.delete("/users/{nickname}", response_model=DeleteProfileResponse)
async def delete_profile(deleted_user: DeleteProfileResponse):
    return {
        "status": "success",
        "message": deleted_user.message
    }

# 특정 회원 조회
class SearchData(BaseModel):
    nickname: str = Field(min_length=4, max_length=8)
    profile_image: Optional[str] = None
    created_at: datetime

class SearchResponse(BaseModel):
    status: str
    data: SearchData

@app.get("/users/{nickname}", response_model=SearchResponse)
async def get_profile(
        nickname: Annotated[str, Path(min_length=4, max_length=8)],):
    return{
        "status": "success",
        "data": {
            "nickname": nickname,
            "profile_image": "profile_image",
            "created_at": datetime.now()
        }
    }