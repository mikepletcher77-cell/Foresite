"""
Search wrapper around ReserveCalifornia, using the open-source 'camply' CLI
tool as a subprocess (since camply needs an older library version that
conflicts with the rest of this app, it lives in its own separate
environment: camply_venv).
"""

import re
import os
import subprocess
import sys
from pathlib import Path
from typing import List

from app.schemas import CampgroundResult, CampsiteResult

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if sys.platform.startswith("win"):
    CAMPLY_BIN = PROJECT_ROOT / "camply_venv" / "Scripts" / "camply.exe"
else:
    CAMPLY_BIN = PROJECT_ROOT / "camply_venv" / "bin" / "camply"


def _run_camply(args: List[str]) -> str:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    result = subprocess.run(
        [str(CAMPLY_BIN)] + args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        env=env,
    )
    return result.stdout + result.stderr


def search_campgrounds(query: str) -> List[CampgroundResult]:
    output = _run_camply(
        ["campgrounds", "--search", query, "--state", "CA", "--provider", "ReserveCalifornia"]
    )
    matches = re.findall(r"🏕\s*(.+?)\(#(\d+)\)", output, re.DOTALL)

    results = []
    for name, facility_id in matches:
        results.append(
            CampgroundResult(
                provider="ReserveCalifornia",
                facility_id=facility_id,
                name=" ".join(name.split()),
                state="CA",
            )
        )
    return results


def list_campsites(facility_id: str) -> List[CampsiteResult]:
    output = _run_camply(
        ["list-campsites", "--campground", facility_id, "--provider", "ReserveCalifornia"]
    )
    matches = re.findall(r"⛺️\s*(.+?)\(#(\d+)\)", output)

    results = []
    for name, campsite_id in matches:
        clean_name = " ".join(name.split()).rstrip("- ").strip()
        results.append(
            CampsiteResult(
                provider="ReserveCalifornia",
                facility_id=facility_id,
                campsite_id=campsite_id,
                site_number=clean_name,
            )
        )
    return results
