import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# Fetch Firebase credentials path
cred_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')

# Ensure credentials path exists
if not cred_path:
    raise FileNotFoundError("⚠️ FIREBASE_SERVICE_ACCOUNT_KEY is not set in .env")

if not os.path.exists(cred_path):
    raise FileNotFoundError(f"🚨 Firebase credentials file not found at: {cred_path}")

logging.info("✅ Firebase credentials found, initializing Firestore...")

# Initialize Firebase App (only if not already initialized)
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()
logging.info("🔥 Firestore client initialized successfully!")
