from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/api/team")
def get_team():
    league_id = "673677643"

    url = (
        "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/"
        f"seasons/2026/segments/0/leagues/{league_id}?view=mRoster"
    )

    response = requests.get(url)

    return response.json()