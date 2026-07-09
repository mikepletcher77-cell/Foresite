# Foresite — Stage 1: Accounts + Campground Search

This is the foundation everything else (watchlist, push notifications,
ReserveCalifornia support) will build on top of. Right now it can:

- Let people create an account and log in (you and your friends/girlfriend
  each get your own separate login — nothing shared unless you choose to)
- Search campgrounds by name/state and list individual campsites within
  one, using Recreation.gov's official public data (covers most national
  forests, national parks, BLM, Army Corps campgrounds, etc.)

**Not in this stage yet:** ReserveCalifornia search (New Brighton and other
CA State Parks), the watchlist itself, and push notifications. Those come
next — this stage just needs to exist and be reachable first.

---

## 1. Get a free Recreation.gov API key
1. Go to https://ridb.recreation.gov/
2. Top right → "Get API Key" → fill out the short form
3. It emails you a key immediately — copy it

## 2. Get the code running somewhere (Render, free tier)
This needs to run continuously, so it lives on a hosting service rather
than your own computer.

1. Create a free account at https://render.com
2. This repo is already set up with all the project files
3. In Render: **New +** → **Web Service** → connect this GitHub repo
4. Render will detect it's Python. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Under **Environment**, add these:
   - `JWT_SECRET` → any long random string
   - `RECREATION_GOV_API_KEY` → the key from step 1
   - `DATABASE_URL` → leave unset for now, it'll default to a local SQLite file
6. Click **Create Web Service** — Render builds and gives you a live URL

## 3. Test that it's alive
Visit your Render URL — you should see `{"status": "ok", "service": "foresite-api"}`

Then test signup/login/search at `https://your-url.onrender.com/docs`

---

## What's next
Once this is live, next stage is the watchlist and then notifications.
ReserveCalifornia search slots in alongside Recreation.gov search once
that stage starts.


