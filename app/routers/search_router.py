from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from app.schemas import CampgroundResult, CampsiteResult
from app.auth import get_current_user
from app.models import User
import app.search_service as search_service

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/campgrounds", response_model=List[CampgroundResult])
async def search_campgrounds(
    query: str,
    state: Optional[str] = None,
    current_user: User = Depends(get_current_user),
):
    """
    Search campgrounds by name/keyword, optionally narrowed by state.
    Currently covers Recreation.gov (most federal/national campgrounds).
    """
    try:
        return await search_service.search_campgrounds(query=query, state=state)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Search failed: {e}")


@router.get("/campsites", response_model=List[CampsiteResult])
async def list_campsites(
    facility_id: str,
    current_user: User = Depends(get_current_user),
):
    """
    List individual campsites within a campground, so a specific site
    can be added to the watchlist.
    """
    try:
        return await search_service.list_campsites(facility_id=facility_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Search failed: {e}")
import app.reservecalifornia_service as reservecalifornia_service


@router.get("/reservecalifornia/campgrounds", response_model=List[CampgroundResult])
def search_reservecalifornia_campgrounds(
    query: str,
    current_user: User = Depends(get_current_user),
):
    """
    Search California State Parks campgrounds by name/keyword.
    """
    try:
        return reservecalifornia_service.search_campgrounds(query=query)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Search failed: {e}")


@router.get("/reservecalifornia/campsites", response_model=List[CampsiteResult])
def list_reservecalifornia_campsites(
    facility_id: str,
    current_user: User = Depends(get_current_user),
):
    """
    List individual campsites within a California State Parks campground.
    """
    try:
        return reservecalifornia_service.list_campsites(facility_id=facility_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Search failed: {e}")