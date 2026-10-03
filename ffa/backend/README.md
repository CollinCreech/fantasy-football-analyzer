# Private ESPN league access

Install dependencies from the `ffa` directory:

```powershell
.\backend\venv\Scripts\python.exe -m pip install -r backend/requirements.txt
```

Sign in to ESPN with an account that can view the league. In your browser's
developer tools, open Application (Chrome/Edge) or Storage (Firefox), then
Cookies. Find `SWID` and `espn_s2` for the ESPN site. Copy the complete values,
including braces if present in SWID. These cookies grant account access;
keep them out of Git, frontend code, screenshots, and chat.

Create `backend/.env` alongside `main.py` and paste the full values:

```dotenv
ESPN_SWID={your-full-SWID-value}
ESPN_S2=your-full-espn_s2-value
```

This file is ignored by Git. The backend loads it at startup, overriding any
older cookie values in your terminal environment. Restart the backend after
editing it.

Start the backend from the `ffa` directory:

```powershell
.\backend\venv\Scripts\python.exe -m uvicorn main:app --app-dir backend --reload
```

Open http://localhost:8000/docs and execute GET `/api/teams`. Successful access
returns team IDs and names. Missing cookies return 503; ESPN rejecting cookies
returns 502 with a specific message. If rejected, sign in again, refresh the
cookie values, and confirm that the account can view league `673677643` in 2026.
