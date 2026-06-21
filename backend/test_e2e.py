import requests
import time
import json
import os

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_flow():
    # 1. Register/Login
    session = requests.Session()
    email = f"test_{int(time.time())}@test.com"
    res = session.post(f"{BASE_URL}/auth/register", json={
        "full_name": "E2E Test User",
        "email": email,
        "password": "testpassword123"
    })
    print(f"Register: {res.status_code}")
    if res.status_code != 201:
        print(res.text)
        
    res = session.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": "testpassword123"
    })
    print(f"Login: {res.status_code}")
    if res.status_code != 200:
        print(res.text)
        return
        
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Upload Resume
    # Create a dummy PDF file
    with open("dummy.pdf", "wb") as f:
        f.write(b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >>\nendobj\n4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n5 0 obj\n<< /Length 44 >>\nstream\nBT /F1 24 Tf 100 700 Td (Danielle Brasseur - Developer) Tj ET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000216 00000 n \n0000000304 00000 n \ntrailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n398\n%%EOF")

    with open("dummy.pdf", "rb") as f:
        res = session.post(
            f"{BASE_URL}/resume/upload", 
            files={"file": ("dummy.pdf", f, "application/pdf")},
            headers=headers
        )
    print(f"Upload: {res.status_code}")
    resume_id = res.json()["id"]
    
    # 3. Analyze
    res = session.post(f"{BASE_URL}/resume/{resume_id}/analyze", json={
        "career_goal": "Software Engineer"
    }, headers=headers)
    print(f"Analyze trigger: {res.status_code}")
    
    # 4. Poll
    for _ in range(30):
        time.sleep(1)
        res = session.get(f"{BASE_URL}/resume/analysis/{resume_id}/status", headers=headers)
        status = res.json()["status"]
        print(f"Status: {status}")
        if status in ["completed", "failed"]:
            break
            
    # 5. Fetch Dashboard
    res = session.get(f"{BASE_URL}/dashboard/summary", headers=headers)
    print(f"Dashboard: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        print("--- Dashboard Data ---")
        print(f"Name: {data.get('personal_info', {}).get('name')}")
        print(f"Domain: {data.get('domain')}")
        print(f"Completeness: {data.get('resume_completeness', {}).get('score')}")
        print(f"Resume Score: {data.get('resume_score')}")
        print(f"Debug Info present: {'debug_info' in data}")
        print(f"Summary: {data.get('resume_summary')}")
    else:
        print(res.text)

if __name__ == "__main__":
    test_flow()
