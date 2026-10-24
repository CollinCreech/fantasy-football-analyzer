import unittest
from unittest.mock import Mock, patch

from fastapi import HTTPException

from main import fetch_league


class LeagueConfigurationTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(
            "os.environ",
            {
                "ESPN_SWID": "test-swid",
                "ESPN_S2": "test-cookie",
                "ESPN_LEAGUE_ID": "123456",
                "ESPN_SEASON": "2026",
            },
            clear=True,
        )
        environment.start()
        self.addCleanup(environment.stop)

    @patch("main.requests.get")
    def test_requests_configured_league_and_season(self, mock_get):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"teams": []}
        mock_get.return_value = response

        result = fetch_league("mTeam")

        self.assertEqual(result, {"teams": []})
        mock_get.assert_called_once_with(
            "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/"
            "seasons/2026/segments/0/leagues/123456?view=mTeam",
            cookies={"SWID": "test-swid", "espn_s2": "test-cookie"},
            timeout=10,
        )

    @patch("main.requests.get")
    def test_invalid_configuration_does_not_contact_espn(self, mock_get):
        for variable in ("ESPN_LEAGUE_ID", "ESPN_SEASON"):
            for value in ("", "invalid"):
                with self.subTest(variable=variable, value=value):
                    with patch.dict("os.environ", {variable: value}):
                        with self.assertRaises(HTTPException) as raised:
                            fetch_league("mTeam")

                    self.assertEqual(raised.exception.status_code, 503)

        mock_get.assert_not_called()


if __name__ == "__main__":
    unittest.main()