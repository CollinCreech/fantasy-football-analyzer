from copy import deepcopy


SEASON = 2026
WEEK = 4


def make_player(player_id, name, position_id, points):
    stats = []
    if points is not None:
        stats.append({
            "seasonId": SEASON,
            "scoringPeriodId": WEEK,
            "statSourceId": 0,
            "statSplitTypeId": 1,
            "appliedTotal": points,
        })

    return {
        "playerPoolEntry": {
            "player": {
                "id": player_id,
                "fullName": name,
                "defaultPositionId": position_id,
                "stats": stats,
            }
        }
    }


DEMO_LEAGUE = {
    "seasonId": SEASON,
    "scoringPeriodId": WEEK,
    "teams": [
        {
            "id": 1,
            "name": "Demo Dragons",
            "roster": {
                "entries": [
                    make_player(101, "Alex Rivers", 1, 24.6),
                    make_player(102, "Jordan Brooks", 2, 18.2),
                    make_player(103, "Casey Morgan", 2, 0),
                    make_player(104, "Taylor Hayes", 3, 21.4),
                    make_player(105, "Cameron Reed", 3, 12.8),
                    make_player(106, "Drew Parker", 4, 9.5),
                    make_player(107, "Avery Stone", 5, 8),
                    make_player(108, "Demo City Defense", 16, 6),
                ]
            },
        },
        {
            "id": 2,
            "name": "Sample Sharks",
            "roster": {
                "entries": [
                    make_player(201, "Sam Carter", 1, 19.8),
                    make_player(202, "Riley Bennett", 2, 22.1),
                    make_player(203, "Jamie Ellis", 2, 11.3),
                    make_player(204, "Quinn Foster", 3, 17.6),
                    make_player(205, "Dakota Lane", 3, None),
                    make_player(206, "Reese Walker", 4, 14.2),
                    make_player(207, "Skyler Mason", 5, 10),
                    make_player(208, "Sample Bay Defense", 16, 4),
                ]
            },
        },
    ],
}


def get_demo_league():
    return deepcopy(DEMO_LEAGUE)