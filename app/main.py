from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import auth_router, search_router, watchlist_router
from apscheduler.schedulers.background import BackgroundScheduler
import app.availability_checker as availability_checker
# Creates tables on first run if they don't exist yet (SQLite/Postgres both fine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Foresite API", version="0.1.0")

# Wide open for now so your web app frontend (any domain) can call this.
# Fine while building; worth tightening to your actual frontend URL later.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(search_router.router)
app.include_router(watchlist_router.router)
app.mount("/app", StaticFiles(directory="app/static", html=True), name="static")
scheduler = BackgroundScheduler()
scheduler.add_job(availability_checker.check_all_watchlist_items, "interval", minutes=15)
scheduler.start()

@app.get("/")
def root():
    return {"status": "ok", "service": "foresite-api"}