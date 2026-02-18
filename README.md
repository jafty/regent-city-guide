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
- `DJANGO_ALLOWED_HOSTS` = `*` (or your Railway domain/custom domain)

Optional when using PostgreSQL plugin:
- `DATABASE_URL` (Railway usually injects this automatically)

### 3) Build/Start behavior
This repo ships with:
- `requirements.txt` for Python detection.
- `Procfile` + `railway.json` using `./start.sh`.
- `start.sh` runs migrations, collectstatic, then gunicorn.

### 4) Common failure from your log
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
