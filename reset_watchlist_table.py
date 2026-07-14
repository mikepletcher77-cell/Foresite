"""
One-time helper: drops and recreates the watchlist_items table so it
picks up new columns added to the WatchlistItem model.

Run this once with: python reset_watchlist_table.py
Safe to delete after running.
"""

from app.database import Base, engine
from app.models import WatchlistItem

print("Dropping watchlist_items table...")
WatchlistItem.__table__.drop(bind=engine, checkfirst=True)

print("Recreating watchlist_items table with the current model...")
Base.metadata.create_all(bind=engine)

print("Done. Your watchlist is now empty but ready to use with the new column.")