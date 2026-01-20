import status
from fastapi import FastAPI, Header, Path, Depends, Query
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated, Literal, List
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


# 게시글 목록 조회
class SearchPostQuery(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    sort: Literal["created_at","updated_at"] = Field("created_at")

class PostItem(BaseModel):
    nickname: str = Field
    title: str
    created_at: datetime
    updated_at: datetime

class Pagination(BaseModel):
    page: int
    limit: int
    total: int

class PostListResponse(BaseModel):
    status: str
    data: List[PostItem]
    pagination: Pagination

@app.get("/posts", response_model=PostListResponse)
async def get_posts(
        params: SearchPostQuery = Depends()
):
    fetched_posts = []
    total_count = 0
    return{
        "status": "success",
        "data": fetched_posts,
        "pagination": {
            "page": params.page,
            "limit": params.limit,
            "total": total_count,
        }
    }


# 게시글 검색
class SearchDetailQuery(BaseModel):
    search: str = Field(min_length=1)
    search_type: Literal["title", "content"] = Field("title", description="검색 범위")

class PostDetailItem(BaseModel):
    nickname: str
    title: str
    post: str
    created_at: datetime

class PostDetailResponse(BaseModel):
    status: str
    data: PostDetailItem | None = None

@app.get("/posts/search", response_model=PostListResponse)
async def search_post(
    params: SearchDetailQuery = Depends()
):
    return{
        "status": "success",
        "data": None
    }

# 게시글 정렬
class Pagination(BaseModel):
    page: int
    limit: int
    total: int

class PostListItem(BaseModel):
    nickname: str
    title: str
    like_count: int
    created_post_at: datetime

class PostListResponse(BaseModel):
    status: str
    data: List[PostListItem]
    pagination: Pagination

@app.get("/posts", response_model=PostListResponse)
async def get_posts(
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100),
        sort: str = Query("created_at")
):
    return{
        "status": "success",
        "data": [
            {
                "nickname": "닉네임",
                "title": "게시글 제목",
                "like_count": "게시글 좋아요 수",
                "created_post_at": "datetime"
            }
        ],
        "pagination": {
            "page": 1,
            "limit": 20,
            "total": 100
        }
    }


# 게시글 상세 조회
class PostDetail(BaseModel):
    title: str
    post_id: int
    nickname: str
    post_content: str
    created_post_at: datetime
    post_updated_at: datetime

class PostDetailResponse(BaseModel):
    status: str
    data: PostDetailItem

@app.get("/posts/{post_id}")
async def get_post(

):
    return {
        "status": "success",
        "data": [
            {
                "post_id": 1234125,
                "nickname": "닉네임",
                "title": "게시글 제목",
                "post_content": "게시글 내용",
                "created_post_at": "datetime"
            }
        ]
    }


# 게시글 작성
class PostCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    post: str = Field(..., min_length=1, max_length=1000, alias="content") # 명세서 Body엔 post라 되어있으나 설명엔 content 혼용, 코드상 일치 필요

class PostCreateData(BaseModel):
    post_id: int
    title: str
    post: str
    created_post_at: str

class PostCreateResponse(BaseModel):
    status: str
    data: PostCreateData

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostCreateResponse)
async def create_post(
    request: PostCreateRequest,
    authorization: str = Header(..., description="Bearer {token}")
):
    return {
        "status": "success",
        "data": {
            "post_id": "124567890",
            "title": "새 게시글 제목",
            "post": "새 게시글 내용",
            "created_post_at": "2026-01-04T12:00:00Z"
        }
    }


# 게시글 수정
class PostUpdateRequest(BaseModel):
    post_title: str = Field(..., min_length=1, max_length=100)
    post_content: str = Field(..., min_length=1, max_length=1000, alias="content")

class PostUpdateData(BaseModel):
    title: str
    content: str
    nickname: str

class PostUpdateResponse(BaseModel):
    status: str
    data: PostUpdateData
    post_created_at: datetime
    post_updated_at: datetime

@app.patch("/users/{nickname}/posts/{post_id}")
async def update_post(
        request: PostUpdateRequest
):
    return{
        "status": "success",
        "data": {
            "nickname": "닉네임",
            "title": "변경된 게시글 제목",
            "content": "변견된 게시글 내용",
            "post_created_at": "datetime",
            "post_updated_at": datetime.now()
        }
    }


# 게시글 삭제
class DeletePost(BaseModel):
    status: str
    message: str

@app.delete("/posts/{nickname}", response_model=DeletePost)
async def delete_post(deleted_post: DeletePost):
    return {
        "status": "success",
        "message": deleted_post.message
    }


# 내가 쓴 게시물 목록
class PostsWriteData(BaseModel):
    post_id: int
    nickname: str
    title: str
    created_post_at: datetime

class PostWriteResponse(BaseModel):
    status: str
    data: PostsWriteData

@app.get("users/me/posts")
async def get_my_post(
        post_id: int
):
    return {
        "status": "success",
        "data": [
            {
                "post_id": 1234125,
                "nickname": "닉네임",
                "title": "게시글 제목",
                "created_post_at": "datetime"
            }
        ]
    }