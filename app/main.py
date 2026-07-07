from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth_router, search_router

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


@app.get("/")
def root():
    return {"status": "ok", "service": "foresite-api"}
