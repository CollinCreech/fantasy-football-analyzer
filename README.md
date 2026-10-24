# Fantasy Football Analyzer

A React and FastAPI dashboard for viewing private ESPN fantasy football league rosters and current-week scores.

## Features

- Select a league team and view its roster.
- Search players and filter by position.
- Display current-week actual fantasy points, including unavailable scores.
- Protect access with app login credentials and keep ESPN cookies on the backend.

Custom projections and lineup recommendations are planned features.

## Project layout

```text
.github/workflows/  Automated frontend and backend checks
frontend/          React application
backend/           FastAPI application, configuration template, and tests
Dockerfile         Combined frontend/backend production image
```

## Local setup

Use Python 3.12 and Node.js 22. Run these commands from the repository root.

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
python -m pip install -r backend/requirements-dev.txt
cp backend/.env.example backend/.env
```

On Windows PowerShell, activate with `./backend/.venv/Scripts/Activate.ps1` and copy the template using `Copy-Item backend/.env.example backend/.env`.

Fill in `backend/.env` with your app login, league ID, season, and ESPN cookies.
See [backend configuration](backend/README.md) for cookie setup. Never commit real credentials.

Start the backend:

```bash
python -m uvicorn main:app --app-dir backend --reload
```

In a second terminal:

```bash
cd frontend
npm ci
npm start
```

Open http://localhost:3000. The frontend proxies API requests to port 8000.
API documentation is available at http://localhost:8000/docs. Sign in with your configured app credentials.

## Demo mode

To explore fictional teams and scores without ESPN credentials, set this
in `backend/.env` and restart the backend:

```dotenv
DEMO_MODE=true
```

Start the backend and frontend using the local setup instructions.
Demo mode allows access without app login and never contacts ESPN,
even when ESPN credentials are configured.

For a public Docker demo:

```bash
docker build -t fantasy-football-analyzer .
docker run --rm -e DEMO_MODE=true -p 8000:10000 fantasy-football-analyzer
```

Open http://localhost:8000.

To return to your private league, set `DEMO_MODE=false`, configure app
login and ESPN credentials, and restart the backend.

## Tests and build

Backend, from the repository root with the virtual environment activated:

```bash
cd backend
python -m unittest discover -v
```

Frontend, in a separate terminal from the repository root:

```bash
cd frontend
npm test -- --watchAll=false --runInBand
npm run build
```

GitHub Actions runs backend tests, frontend tests, and the frontend build on pushes and pull requests.

## Docker

From the repository root:

```bash
docker build -t fantasy-football-analyzer .
docker run --rm --env-file backend/.env -p 8000:10000 fantasy-football-analyzer
```

Open http://localhost:8000. The container serves both the built frontend and API.
Credentials are supplied at runtime; environment files are excluded from the image.

For hosted deployments, set the build context to the repository root and the Dockerfile path to `Dockerfile`. Configure the same environment variables through your hosting service and use HTTPS. The container listens on `PORT`, defaulting to 10000.
