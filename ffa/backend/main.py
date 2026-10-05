import os
from pathlib import Path

import secrets

from dotenv import load_dotenv
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import requests


load_dotenv(Path(__file__).with_name(".env"), override=True)

app = FastAPI()

security = HTTPBasic(auto_error=False)

@app.middleware("http")
async def require_login(request: Request, call_next):
    username = os.environ.get("APP_USERNAME", "")
    password = os.environ.get("APP_PASSWORD", "")

    if not username or not password:
        return JSONResponse(
            status_code=503,
            content={"detail": "App login is not configured."},
        )

    try:
        credentials = await security(request)
    except HTTPException:
        credentials = None

    username_ok = secrets.compare_digest(
        (credentials.username if credentials else "").encode("utf-8"),
        username.encode("utf-8"),
    )
    password_ok = secrets.compare_digest(
        (credentials.password if credentials else "").encode("utf-8"),
        password.encode("utf-8"),
    )

    if not (username_ok and password_ok):
        return JSONResponse(
            status_code=401,
            content={"detail": "Authentication required."},
            headers={"WWW-Authenticate": 'Basic realm="Fantasy Football"'},
        )

    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    return response


def fetch_league(view):
    cookies = {
        "SWID": os.environ.get("ESPN_SWID", "").strip(),
        "espn_s2": os.environ.get("ESPN_S2", "").strip(),
    }
    if not all(cookies.values()):
        raise HTTPException(
            status_code=503,
            detail="Set ESPN_SWID and ESPN_S2 on the backend to access your private league.",
        )

    league_id = "673677643"
    url = (
        "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/"
        f"seasons/2026/segments/0/leagues/{league_id}?view={view}"
    )

    try:
        response = requests.get(url, cookies=cookies, timeout=10)
        if response.status_code in (401, 403):
            raise HTTPException(
                status_code=502,
                detail="ESPN denied league access. Check your backend cookies and account's league access.",
            )
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to load league data from ESPN.",
        ) from exc

POSITION_LABELS = {
      1: "QB",
      2: "RB",
      3: "WR",
      4: "TE",
      5: "K",
      16: "D/ST",
  }

@app.get("/api/team")
def get_team():
    return fetch_league("mRoster")


@app.get("/api/teams")
def get_teams():
    data = fetch_league("mTeam")
    return [
        {
            "id": team["id"],
            "name": team.get("name")
            or " ".join(
                filter(None, [team.get("location"), team.get("nickname")])
            )
            or f"Team {team['id']}",
        }
        for team in data.get("teams", [])
    ]


@app.get("/api/teams/{team_id}/roster")
def get_roster(team_id: int):
    data = fetch_league("mRoster")

    selected_team = next(
        (team for team in data.get("teams", []) if team["id"] == team_id),
        None,
    )

    if selected_team is None:
        raise HTTPException(status_code=404, detail="Team not found.")

    season_id = data["seasonId"]
    scoring_period_id = data["scoringPeriodId"]

    roster = []

    for entry in selected_team.get("roster", {}).get("entries", []):
        player = entry["playerPoolEntry"]["player"]
        actual_stats = next(
        (
            stat
            for stat in player.get("stats", [])
            if stat.get("seasonId") == season_id
            and stat.get("scoringPeriodId") == scoring_period_id
            and stat.get("statSourceId") == 0
            and stat.get("statSplitTypeId") == 1
        ),
        None,
        )

        points = (
            actual_stats.get("appliedTotal")
            if actual_stats is not None
            else None
        )

        roster.append({
            "id": player["id"],
            "name": player["fullName"],
            "position": POSITION_LABELS.get(
                player.get("defaultPositionId"), "UNKNOWN"),
            "proTeamId": player.get("proTeamId"),
            "points": points,
            "scoringPeriodId": scoring_period_id,
        })

    return {
        "teamId": team_id,
        "seasonId": data.get("seasonId"),
        "scoringPeriodId": data.get("scoringPeriodId"),
        "players": roster,
    }

build_directory = Path(__file__).resolve().parent.parent / "build"

if build_directory.is_dir():
    app.mount(
        "/",
        StaticFiles(directory=str(build_directory), html=True),
        name="frontend",
    )