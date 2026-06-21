import urllib.request
import urllib.error
import json
import uuid

base_url = "http://localhost:8000/api/v1"

unique_suffix = uuid.uuid4().hex[:6]
test_email = f"user_{unique_suffix}@example.com"
test_name = "Test User"
test_password = "password123"

def make_request(path, data=None, token=None, method="POST"):
    url = f"{base_url}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    req_data = None
    if data:
        req_data = json.dumps(data).encode("utf-8")
        
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            err_data = json.loads(body)
        except:
            err_data = body
        return e.code, err_data

print("--- STARTING AUTH API TESTS (URLLIB) ---")

# 1. Test registration
print("\n1. Testing User Registration...")
reg_payload = {
    "full_name": test_name,
    "email": test_email,
    "password": test_password
}
code, user_data = make_request("/auth/register", reg_payload)
assert code == 201, f"Registration failed ({code}): {user_data}"
print("Registration Success!", user_data)
assert user_data["email"] == test_email
assert user_data["full_name"] == test_name
assert "id" in user_data
assert "password_hash" not in user_data

# 2. Test duplicate registration
print("\n2. Testing Duplicate User Registration...")
code, err_data = make_request("/auth/register", reg_payload)
assert code == 400, f"Expected 400 for duplicate, got {code}: {err_data}"
print("Duplicate check passed. Got expected 400 Bad Request:", err_data["detail"])

# 3. Test correct login
print("\n3. Testing Successful Login...")
login_payload = {
    "email": test_email,
    "password": test_password
}
code, token_data = make_request("/auth/login", login_payload)
assert code == 200, f"Login failed ({code}): {token_data}"
print("Login Success! Token received:", token_data)
assert "access_token" in token_data
assert token_data["token_type"] == "bearer"
token = token_data["access_token"]

# 4. Test incorrect login
print("\n4. Testing Failed Login...")
bad_login_payload = {
    "email": test_email,
    "password": "wrong_password"
}
code, err_data = make_request("/auth/login", bad_login_payload)
assert code == 401, f"Expected 401 for bad password, got {code}: {err_data}"
print("Incorrect login check passed. Got expected 401 Unauthorized:", err_data["detail"])

# 5. Test get profile (/me) with valid token
print("\n5. Testing /me endpoint with valid token...")
code, me_data = make_request("/auth/me", token=token, method="GET")
assert code == 200, f"Me endpoint failed ({code}): {me_data}"
print("Me endpoint Success!", me_data)
assert me_data["email"] == test_email
assert me_data["full_name"] == test_name

# 6. Test get profile (/me) without valid token
print("\n6. Testing /me endpoint without token...")
code, err_data = make_request("/auth/me", method="GET")
assert code == 401, f"Expected 401 for no token, got {code}: {err_data}"
print("Token guard check passed. Got expected 401 Unauthorized:", err_data)

print("\n--- ALL AUTH API TESTS PASSED SUCCESSFULLY! ---")
