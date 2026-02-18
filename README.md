# Bistro Toulouse (Django)

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Deploy on Railway

### 1) Verify repository contents in Railway
If Railway logs show only `clap.txt`, Railway is not receiving the right branch/commit.

- In Railway service settings, confirm the selected repo and branch.
- Trigger a fresh deploy after pushing latest commit.
- Ensure the branch contains at least these files at root: `manage.py`, `requirements.txt`, `Procfile`, `start.sh`.

### 2) Required environment variables
Set these in Railway Variables:

- `DJANGO_SECRET_KEY` = strong random string
- `DJANGO_DEBUG` = `False`
- `DJANGO_ALLOWED_HOSTS` = `your-app.up.railway.app,your-custom-domain.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS` = `https://your-app.up.railway.app,https://your-custom-domain.com`

Database options (pick one):
- **Recommended:** PostgreSQL plugin with `DATABASE_URL` (Railway usually injects this automatically).
- **SQLite (single-user / simple use):** add a Railway Volume and set `DJANGO_SQLITE_PATH=/data/db.sqlite3` so the DB file survives deploys/restarts.


### 3) Persist superuser/data across deploys
- If your app uses the default filesystem SQLite path without a volume, data can be lost on new deploy instances.
- To persist data, either:
  1. Use Railway PostgreSQL (`DATABASE_URL`) **or**
  2. Use Railway Volume + SQLite (`DJANGO_SQLITE_PATH=/data/db.sqlite3`).
- After first deploy with persistent DB configured, create admin once:
  - `python manage.py createsuperuser`

### 4) Build/Start behavior
This repo ships with:
- `requirements.txt` for Python detection.
- `Procfile` + `railway.json` using `./start.sh`.
- `start.sh` runs migrations, collectstatic, then gunicorn.

### 5) Common failure from your log
Error:
- `Script start.sh not found`
- `The app contents ... contains: ./ clap.txt`

Cause:
- Railway built a snapshot that did not include your Django files (wrong branch/repo, or deploy before pushing).

Fix:
1. Push latest branch containing Django files.
2. Reconnect/select correct branch in Railway.
3. Redeploy.

## Notes
- Static files are served with WhiteNoise.
- Production server is Gunicorn.
