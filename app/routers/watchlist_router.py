from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import User, WatchlistItem
from app.schemas import WatchlistItemCreate, WatchlistItemUpdate, WatchlistItemOut
from app.auth import get_current_user

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.post("", response_model=WatchlistItemOut)
def create_watchlist_item(
    item_in: WatchlistItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = WatchlistItem(owner_id=current_user.id, **item_in.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=List[WatchlistItemOut])
def list_watchlist_items(
    trip_label: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(WatchlistItem).filter(WatchlistItem.owner_id == current_user.id)
    if trip_label:
        query = query.filter(WatchlistItem.trip_label == trip_label)
    if active_only:
        query = query.filter(WatchlistItem.active == True)  # noqa: E712
    return query.order_by(WatchlistItem.trip_label, WatchlistItem.rank).all()


def _get_owned_item(item_id: int, db: Session, current_user: User) -> WatchlistItem:
    item = (
        db.query(WatchlistItem)
        .filter(WatchlistItem.id == item_id, WatchlistItem.owner_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Watchlist item not found")
    return item


@router.get("/{item_id}", response_model=WatchlistItemOut)
def get_watchlist_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _get_owned_item(item_id, db, current_user)


@router.patch("/{item_id}", response_model=WatchlistItemOut)
def update_watchlist_item(
    item_id: int,
    item_update: WatchlistItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = _get_owned_item(item_id, db, current_user)
    for field, value in item_update.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_watchlist_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = _get_owned_item(item_id, db, current_user)
    db.delete(item)
    db.commit()
    return {"status": "deleted", "id": item_id}
