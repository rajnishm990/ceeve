import requests

BASE_URL = "http://127.0.0.1:8000"

def signup(username, email, password):
    url = f"{BASE_URL}/auth/signup"
    payload = {
        "username": username,
        "email": email,
        "password": password
    }
    r = requests.post(url, json=payload)

    print("RAW RESPONSE:", r.text)   
    print("STATUS:", r.status_code)

    try:
        print("JSON:", r.json())
    except Exception as e:
        print("JSON PARSE ERROR:", e)

    return r


def login(email, password):
    url = f"{BASE_URL}/auth/login"
    payload = {
          
        "username": email,
        "password": password
    }
    r = requests.post(url, data=payload)
    print("Login:", r.status_code, r.json())
    if r.status_code == 200:
        return r.json()["access_token"]
    return None


def create_resume(token, title, file_name=None):
    url = f"{BASE_URL}/api/resumes"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "title": title,
        "file_name": file_name
    }
    r = requests.post(url, json=payload, headers=headers)
    print("Create Resume:", r.status_code, r.json())
    return r


def upload_resume_file(token, resume_id, file_path):
    url = f"{BASE_URL}/api/resumes/{resume_id}/upload"
    headers = {"Authorization": f"Bearer {token}"}

    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/octet-stream")}
        r = requests.post(url, files=files, headers=headers)

    print("Upload Resume:", r.status_code, r.json())
    return r


def main():
    # 1. Create a test user
    signup("raj", "raj@example.com", "secret123")

    # 2. Login and get JWT token
    token = login("raj@example.com", "secret123")
    if not token:
        print("Login failed — stopping.")
        return

    print("\nJWT Token:", token)

    # 3. Create resume
    res = create_resume(token, "Backend Resume", "resume.pdf")
    resume_id = res.json()["id"]

    print("\nCreated Resume ID:", resume_id)

    # 4. Upload file as new version
    file_path = "resume.pdf"   
    upload_resume_file(token, resume_id, file_path)


if __name__ == "__main__":
    main()
