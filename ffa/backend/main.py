import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import requests


load_dotenv(Path(__file__).with_name(".env"), override=True)

app = FastAPI()

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

    roster = []

    for entry in selected_team.get("roster", {}).get("entries", []):
        player = entry["playerPoolEntry"]["player"]

        roster.append({
            "id": player["id"],
            "name": player["fullName"],
            "position": POSITION_LABELS.get(
                player.get("defaultPositionId"), "UNKNOWN"),
            "proTeamId": player.get("proTeamId"),
        })

    return {
        "teamId": team_id,
        "seasonId": data.get("seasonId"),
        "scoringPeriodId": data.get("scoringPeriodId"),
        "players": roster,
    }
