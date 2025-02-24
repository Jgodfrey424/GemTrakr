import firebase_admin
from firebase_admin import credentials, firestore
import os

# ✅ Explicitly set the path to credentials
GOOGLE_CREDS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/app/armortech-firebase-adminsdk-prgtn-de3fba45cf.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDS_PATH  # Ensure ADC is set

try:
    # ✅ Initialize Firebase Admin SDK
    if not firebase_admin._apps:
        cred = credentials.Certificate(GOOGLE_CREDS_PATH)
        firebase_admin.initialize_app(cred)

    # ✅ Initialize Firestore
    db = firestore.client()
    print(f"🔥 Firestore initialized successfully with credentials at {GOOGLE_CREDS_PATH}")
except Exception as e:
    print(f"🔥 Firestore Initialization Error: {e}")
