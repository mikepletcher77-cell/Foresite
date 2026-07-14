from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    display_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    watchlist_items = relationship(
        "WatchlistItem", back_populates="owner", cascade="all, delete-orphan"
    )


class WatchlistItem(Base):
    """
    One row = one campsite this user wants to be alerted about.
    Built now so the table exists; the search/notification stages
    plug into this without needing a schema change later.
    """
    __tablename__ = "watchlist_items"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    provider = Column(String, nullable=False)          # "RecreationGov" or "ReserveCalifornia"
    facility_id = Column(String, nullable=False)        # campground-level ID from the provider
    facility_name = Column(String, nullable=False)       # human-readable, e.g. "New Brighton SB"
    campsite_id = Column(String, nullable=True)          # specific site ID, if narrowed down
    campsite_label = Column(String, nullable=True)       # human-readable, e.g. "Site 45"

    start_date = Column(String, nullable=False)  # ISO date "2026-08-01"
    end_date = Column(String, nullable=False)

    rank = Column(Integer, default=1)   # 1 = top choice, 2 = fallback, etc.
    trip_label = Column(String, nullable=True)  # e.g. "Yosemite with the guys"
    active = Column(Boolean, default=True)
    notified_available = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="watchlist_items")
