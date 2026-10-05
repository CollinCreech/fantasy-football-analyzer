import unittest
from unittest.mock import patch

from main import get_roster


class RosterScoringTests(unittest.TestCase):
    def get_player(self, stats):
        league = {
            "seasonId": 2026,
            "scoringPeriodId": 4,
            "teams": [{
                "id": 1,
                "roster": {
                    "entries": [{
                        "playerPoolEntry": {
                            "player": {
                                "id": 123,
                                "fullName": "Test Player",
                                "defaultPositionId": 2,
                                "proTeamId": 4,
                                "stats": stats,
                            }
                        }
                    }]
                },
            }],
        }

        with patch("main.fetch_league", return_value=league):
            return get_roster(1)["players"][0]

    def stat(self, points, **overrides):
        return {
            "seasonId": 2026,
            "scoringPeriodId": 4,
            "statSourceId": 0,
            "statSplitTypeId": 1,
            "appliedTotal": points,
            **overrides,
        }

    def test_selects_current_week_actual_points(self):
        player = self.get_player([
            self.stat(16.2, statSourceId=1),
            self.stat(58, scoringPeriodId=0, statSplitTypeId=0),
            self.stat(8.9, scoringPeriodId=3),
            self.stat(22, seasonId=2025),
            self.stat(99, statSplitTypeId=2),
            self.stat(19.1),
        ])

        self.assertEqual(player["points"], 19.1)
        self.assertEqual(player["scoringPeriodId"], 4)

    def test_preserves_zero_points(self):
        player = self.get_player([self.stat(0)])

        self.assertEqual(player["points"], 0)

    def test_missing_actual_points_are_unavailable(self):
        player = self.get_player([
            self.stat(16.2, statSourceId=1),
        ])

        self.assertIsNone(player["points"])


if __name__ == "__main__":
    unittest.main()