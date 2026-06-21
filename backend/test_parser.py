"""Quick test: login and call the parse endpoint using urllib (no extra deps)."""
import urllib.request
import urllib.error
import json
import sqlite3

BASE = "http://localhost:8000/api/v1"


def post_json(url, data, headers=None):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers or {})
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def post_empty(url, headers=None):
    req = urllib.request.Request(url, data=b"", method="POST", headers=headers or {})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


# 1. Login
status, data = post_json(f"{BASE}/auth/login", {
    "email": "test_user_unique_123@example.com",
    "password": "Password123!"
})
if status != 200:
    print(f"Login failed ({status}): {data}")
    exit(1)

token = data["access_token"]
auth_headers = {"Authorization": f"Bearer {token}"}
print(f"Logged in. Token: {token[:20]}...")

# 2. Get user info
status, user = get_json(f"{BASE}/auth/me", auth_headers)
print(f"User: {user['full_name']} (id={user['id']})")

# 3. Find a resume owned by this user
conn = sqlite3.connect("skillbridge.db")
cur = conn.cursor()
cur.execute("SELECT id, filename, file_path FROM resumes WHERE user_id = ?", (user['id'],))
resumes = cur.fetchall()
conn.close()

if not resumes:
    print("No resumes found for this user.")
    exit(1)

resume_id = resumes[0][0]
print(f"Parsing resume id={resume_id}, filename={resumes[0][1]}")

# 4. Call parse endpoint
status, result = post_empty(f"{BASE}/resume/{resume_id}/parse", auth_headers)
print(f"\nStatus: {status}")
print(json.dumps(result, indent=2))
