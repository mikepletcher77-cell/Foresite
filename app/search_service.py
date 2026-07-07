"""
Search wrapper around Recreation.gov's official public API (RIDB).

Docs: https://ridb.recreation.gov/landing/docs
Get a free API key at https://ridb.recreation.gov/ (top-right "Get API Key").

NOTE: ReserveCalifornia (used for California State Parks like New Brighton)
does NOT have an official public API like this one. That integration is a
separate, later stage — see README for why it needs different handling.
"""

import httpx
from typing import List, Optional
from app.config import settings
from app.schemas import CampgroundResult, CampsiteResult

RIDB_BASE = "https://ridb.recreation.gov/api/v1"


def _headers():
    return {"apikey": settings.recreation_gov_api_key}


async def search_campgrounds(query: str, state: Optional[str] = None, limit: int = 20) -> List[CampgroundResult]:
    params = {"query": query, "limit": limit}
    if state:
        params["state"] = state

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(f"{RIDB_BASE}/facilities", params=params, headers=_headers())
        resp.raise_for_status()
        data = resp.json()

    results = []
    for item in data.get("RECDATA", []):
        results.append(
            CampgroundResult(
                provider="RecreationGov",
                facility_id=str(item.get("FacilityID")),
                name=item.get("FacilityName", "").strip(),
                state=(item.get("FacilityAddresses") or [{}])[0].get("AddressStateCode")
                if item.get("FacilityAddresses") else None,
                latitude=item.get("FacilityLatitude"),
                longitude=item.get("FacilityLongitude"),
            )
        )
    return results


async def list_campsites(facility_id: str, limit: int = 200) -> List[CampsiteResult]:
    params = {"limit": limit}
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(
            f"{RIDB_BASE}/facilities/{facility_id}/campsites", params=params, headers=_headers()
        )
        resp.raise_for_status()
        data = resp.json()

    results = []
    for item in data.get("RECDATA", []):
        results.append(
            CampsiteResult(
                provider="RecreationGov",
                facility_id=str(facility_id),
                campsite_id=str(item.get("CampsiteID")),
                site_number=item.get("CampsiteName"),
                site_type=item.get("CampsiteType"),
                loop=item.get("Loop"),
            )
        )
    return results
