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


# ---- Watchlist ----
class WatchlistItemCreate(BaseModel):
    provider: str
    facility_id: str
    facility_name: str
    campsite_id: Optional[str] = None
    campsite_label: Optional[str] = None
    start_date: str
    end_date: str
    rank: Optional[int] = 1
    trip_label: Optional[str] = None
    notes: Optional[str] = None


class WatchlistItemUpdate(BaseModel):
    campsite_id: Optional[str] = None
    campsite_label: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    rank: Optional[int] = None
    trip_label: Optional[str] = None
    notes: Optional[str] = None
    active: Optional[bool] = None


class WatchlistItemOut(BaseModel):
    id: int
    provider: str
    facility_id: str
    facility_name: str
    campsite_id: Optional[str] = None
    campsite_label: Optional[str] = None
    start_date: str
    end_date: str
    rank: int
    trip_label: Optional[str] = None
    notes: Optional[str] = None
    active: bool
    created_at: datetime

    class Config:
        from_attributes = True
