import requests

def request_seed(student_id: str, github_repo_url: str, api_url: str):
    """
    Request encrypted seed from instructor API

    Steps:
    1. Read student public key from PEM file
    2. Prepare HTTP POST request payload
    3. Send POST request to instructor API
    4. Parse JSON response
    5. Save encrypted seed to file
    """
    # 1. Read student public key
    with open("student_public.pem", "r") as f:
        public_key = f.read()  # keep BEGIN/END lines

    # 2. Prepare payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    # 3. Send POST request
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()  # raise error for HTTP errors
    except requests.RequestException as e:
        print("HTTP Request failed:", e)
        return

    # 4. Parse JSON response
    data = response.json()
    if data.get("status") == "success":
        encrypted_seed = data["encrypted_seed"]

        # 5. Save to file (do NOT commit this file)
        with open("encrypted_seed.txt", "w") as f:
            f.write(encrypted_seed)
        print("Encrypted seed saved to encrypted_seed.txt")
    else:
        print("Error from API:", data)

request_seed(
    student_id="24A95A6109",
    github_repo_url="https://github.com/sindhutej-6/secure_pki_2fa_microservice_task",
    api_url="https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
)

