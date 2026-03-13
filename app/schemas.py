from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# ── User Schemas ──────────────────────────────────────────────

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Blog Schemas ──────────────────────────────────────────────

class BlogCreate(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


class BlogOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    updated_at: datetime
    author: UserOut

    model_config = {"from_attributes": True}


# ── Blog list response ────────────────────────────────────────

class BlogList(BaseModel):
    total: int
    blogs: List[BlogOut]
