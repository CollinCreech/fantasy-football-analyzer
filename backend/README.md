# Backend setup

Run these commands from the repository root.

## Install dependencies

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
python -m pip install -r backend/requirements-dev.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

## Configure the app

Copy `backend/.env.example` to `backend/.env`.

Set:

- `APP_USERNAME` and `APP_PASSWORD`: credentials for signing into this app.
- `ESPN_LEAGUE_ID`: the league ID from your ESPN fantasy league URL.
- `ESPN_SEASON`: the season year.
- `ESPN_SWID` and `ESPN_S2`: cookies from an ESPN account with league access.

To find the cookies, sign in to ESPN, open your browser's developer
tools, and inspect the ESPN site's cookies under Application or Storage.
Copy the complete `SWID` and `espn_s2` values, including any braces.

These cookies grant account access. Never commit them or include them
in screenshots, frontend code, or logs.

The backend loads `.env` at startup and overrides existing environment
values. Restart it after changing configuration.

## Start the backend

```bash
python -m uvicorn main:app --app-dir backend --reload
```

Open http://localhost:8000/docs and sign in using your app credentials.

Try `GET /api/teams`. A successful response contains team IDs and names.

- `401`: app credentials are missing or incorrect.
- `503`: required configuration is missing or invalid.
- `502`: ESPN access failed; check your cookies and league access.

## Run tests

From the repository root, with the virtual environment activated:

```bash
cd backend
python -m unittest discover -v
```

## Start the frontend

See the [root README](../README.md) for frontend and Docker instructions.

For a publicly hosted deployment, use HTTPS to protect app login
credentials in transit.
