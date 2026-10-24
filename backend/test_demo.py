import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


class DemoModeTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(
            "os.environ",
            {"DEMO_MODE": "true"},
            clear=True,
        )
        environment.start()
        self.addCleanup(environment.stop)

        self.client = TestClient(app)
        self.addCleanup(self.client.close)

        self.espn_request = patch("main.requests.get")
        self.mock_get = self.espn_request.start()
        self.addCleanup(self.espn_request.stop)

    def tearDown(self):
        self.mock_get.assert_not_called()

    def test_demo_works_without_credentials(self):
        config = self.client.get("/api/config")
        self.assertEqual(config.status_code, 200)
        self.assertEqual(config.json(), {"demoMode": True})

        teams = self.client.get("/api/teams")
        self.assertEqual(teams.status_code, 200)
        self.assertEqual(len(teams.json()), 2)

        for team in teams.json():
            response = self.client.get(
                f"/api/teams/{team['id']}/roster"
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()["players"]), 8)

    def test_demo_preserves_zero_and_unavailable_scores(self):
        first = self.client.get("/api/teams/1/roster").json()
        second = self.client.get("/api/teams/2/roster").json()

        self.assertTrue(
            any(player["points"] == 0 for player in first["players"])
        )
        self.assertTrue(
            any(player["points"] is None for player in second["players"])
        )

    def test_unknown_demo_team_returns_404(self):
        response = self.client.get("/api/teams/999/roster")
        self.assertEqual(response.status_code, 404)

    def test_demo_never_uses_configured_private_credentials(self):
        with patch.dict(
            "os.environ",
            {
                "ESPN_SWID": "private-swid",
                "ESPN_S2": "private-cookie",
                "ESPN_LEAGUE_ID": "999999",
            },
        ):
            response = self.client.get("/api/team")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["teams"][0]["name"], "Demo Dragons")

    def test_disabling_demo_restores_login_requirement(self):
        with patch.dict("os.environ", {"DEMO_MODE": "false"}):
            response = self.client.get("/api/teams")

        self.assertEqual(response.status_code, 503)


if __name__ == "__main__":
    unittest.main()