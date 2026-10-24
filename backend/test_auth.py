import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(
            "os.environ",
            {
                "APP_USERNAME": "test-user",
                "APP_PASSWORD": "test-password",
            },
        )
        self.environment.start()
        self.addCleanup(self.environment.stop)

        self.client = TestClient(app)
        self.addCleanup(self.client.close)

    def test_routes_require_login(self):
        for path in ["/", "/docs", "/api/team", "/api/teams",
                    "/api/teams/1/roster"]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 401)
                self.assertIn("Basic", response.headers["WWW-Authenticate"])

    def test_wrong_password_is_rejected(self):
        response = self.client.get(
            "/docs",
            auth=("test-user", "wrong-password"),
        )
        self.assertEqual(response.status_code, 401)

    def test_valid_login_reaches_api(self):
        with patch("main.fetch_league", return_value={"teams": []}):
            response = self.client.get(
                "/api/teams",
                auth=("test-user", "test-password"),
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_missing_configuration_blocks_access(self):
        with patch.dict("os.environ", {"APP_PASSWORD": ""}):
            response = self.client.get(
                "/docs",
                auth=("test-user", "test-password"),
            )

        self.assertEqual(response.status_code, 503)