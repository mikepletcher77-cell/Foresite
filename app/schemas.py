from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ---- Auth ----
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    display_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---- Search ----
class CampgroundResult(BaseModel):
    provider: str
    facility_id: str
    name: str
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CampsiteResult(BaseModel):
    provider: str
    facility_id: str
    campsite_id: str
    site_number: Optional[str] = None
    site_type: Optional[str] = None
    loop: Optional[str] = None
