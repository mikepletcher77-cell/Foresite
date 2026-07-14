"""
Checks whether watchlist items have become available, and emails the
owner when something opens up. Uses camply under the hood (same tool
used for ReserveCalifornia search) to check real availability.
"""

import re
from datetime import datetime

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import WatchlistItem, User
from app.email_service import send_email
import app.reservecalifornia_service as reservecalifornia_service


def _check_reservecalifornia(item: WatchlistItem) -> bool:
    """Returns True if this specific site/campground shows availability."""
    args = [
        "campsites",
        "--provider", "ReserveCalifornia",
        "--campground", item.facility_id,
        "--start-date", item.start_date,
        "--end-date", item.end_date,
        "--search-once",
    ]
    if item.campsite_id:
        args += ["--campsite", item.campsite_id]

    output = reservecalifornia_service._run_camply(args)
    # camply prints "0 Matching Campsites Found" when nothing's open
    match = re.search(r"(\d+)\s+Matching Campsites Found", output)
    if match:
        return int(match.group(1)) > 0
    return False


def check_all_watchlist_items():
    db: Session = SessionLocal()
    try:
        items = db.query(WatchlistItem).filter(
            WatchlistItem.active == True,  # noqa: E712
            WatchlistItem.notified_available == False,  # noqa: E712
        ).all()

        print(f"[{datetime.utcnow()}] Checking {len(items)} watchlist item(s)...")

        for item in items:
            try:
                if item.provider != "ReserveCalifornia":
                    continue  # Recreation.gov checking added later

                is_available = _check_reservecalifornia(item)

                if is_available:
                    owner = db.query(User).filter(User.id == item.owner_id).first()
                    if owner:
                        subject = f"🏕️ {item.facility_name} is available!"
                        body = (
                            f"Good news — a site you're watching just opened up:\n\n"
                            f"Campground: {item.facility_name}\n"
                            f"Site: {item.campsite_label or 'Any site'}\n"
                            f"Dates: {item.start_date} to {item.end_date}\n\n"
                            f"Go book it now before it's gone!"
                        )
                        send_email(owner.email, subject, body)
                        item.notified_available = True
                        db.commit()
                        print(f"  -> Notified {owner.email} about {item.facility_name}")
            except Exception as e:
                print(f"  -> Error checking item {item.id}: {e}")
    finally:
        db.close()