import os
import tempfile
from google.cloud import secretmanager

# ✅ Load initial GOOGLE_APPLICATION_CREDENTIALS from local storage
GOOGLE_CREDS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/app/armortech-firebase-adminsdk-prgtn-de3fba45cf.json")

# ✅ Ensure ADC is set (Google Services use this)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDS_PATH

print(f"🔐 Using initial GOOGLE_APPLICATION_CREDENTIALS from: {GOOGLE_CREDS_PATH}")

# ✅ Initialize Google Secret Manager client (only once)
client = secretmanager.SecretManagerServiceClient()

def get_secret(secret_name):
    """Fetch a secret from Google Secret Manager."""
    project_id = os.getenv("PROJECT_ID", "armortech")
    secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"

    try:
        response = client.access_secret_version(request={"name": secret_path})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        raise RuntimeError(f"🔥 Error retrieving secret '{secret_name}': {e}")

# ✅ Attempt to retrieve Firebase credentials from Google Secret Manager
try:
    firebase_credentials_json = get_secret("FIREBASE_SERVICE_ACCOUNT_KEY")
    print("✅ Successfully retrieved FIREBASE_SERVICE_ACCOUNT_KEY from Secret Manager.")
except RuntimeError as e:
    print(f"⚠️ Warning: Using local credentials because Secret Manager retrieval failed.\n{e}")
    firebase_credentials_json = None

# ✅ Store credentials in a temp file (only if fetched)
if firebase_credentials_json:
    temp_dir = tempfile.gettempdir()
    FIREBASE_CREDENTIALS_PATH = os.path.join(temp_dir, "firebase_creds.json")

    with open(FIREBASE_CREDENTIALS_PATH, "w") as f:
        f.write(firebase_credentials_json)

    # ✅ Update GOOGLE_APPLICATION_CREDENTIALS to use fetched credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = FIREBASE_CREDENTIALS_PATH
    print(f"👌 Credentials retrieved from Secret Manager and stored at {FIREBASE_CREDENTIALS_PATH}")
else:
    print("⚠️ Using local GOOGLE_APPLICATION_CREDENTIALS as Firebase credentials.")

# ✅ Final confirmation of which credentials are active
print(f"🚀 Final GOOGLE_APPLICATION_CREDENTIALS in use: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")

