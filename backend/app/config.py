# import os
# from dotenv import load_dotenv

# # Load variables from .env file into the system
# load_dotenv()

# class Config:
#     # --- 1. Existing API Keys ---
#     GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#     PAYMENT_UPI_ID = os.getenv("PAYMENT_UPI_ID", "yourname@upi") # Default fallback

#     # --- 2. GitHub Headers (Automated) ---
#     GITHUB_HEADERS = {
#         "Authorization": f"token {GITHUB_TOKEN}",
#         "Accept": "application/vnd.github.v3+json"
#     } if GITHUB_TOKEN else {}

#     # --- 3. NEW: Google OAuth Configuration ---
#     GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
#     GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
#     # This URI must match what you set in Google Cloud Console
#     GOOGLE_REDIRECT_URI = "http://localhost:8000/api/auth/callback" 

#     # --- 4. NEW: JWT Security Configuration ---
#     # Used to sign the tokens we give to users
#     JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "please_change_this_to_a_random_string")
#     JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
#     ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # Token valid for 24 hours

#     # --- 5. NEW: Email (SMTP) Configuration ---
#     # Used to send the PDF reports
#     SMTP_EMAIL = os.getenv("SMTP_EMAIL")
#     SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
#     SMTP_SERVER = "smtp.gmail.com"
#     SMTP_PORT = 587

#     # --- 6. Validation ---
#     if not GEMINI_API_KEY:
#         print("WARNING: GEMINI_API_KEY is missing in .env")
#     if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
#         print("WARNING: Google OAuth keys are missing in .env")

import os
from dotenv import load_dotenv

# Load variables from .env file into the system
load_dotenv()

class Config:
    # --- 1. Existing API Keys ---
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PAYMENT_UPI_ID = os.getenv("PAYMENT_UPI_ID", "yourname@upi") # Default fallback

    # --- 2. GitHub Headers (Automated) ---
    GITHUB_HEADERS = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    } if GITHUB_TOKEN else {}

    # --- 3. Google OAuth Configuration ---
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    
    # 🚨 FIX 1: Read the LIVE REDIRECT URI from the environment (Render)
    GOOGLE_REDIRECT_URI = os.getenv(
        "GOOGLE_REDIRECT_URI", 
        "http://localhost:8000/api/auth/callback" # Fallback for local dev
    ) 

    # 🚨 FIX 2: Add the Frontend URL, which is needed for final redirect in auth.py
    FRONTEND_URL = os.getenv(
        "FRONTEND_URL", 
        "http://localhost:3000" # Fallback for local dev
    ) 

    # --- 4. JWT Security Configuration ---
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "please_change_this_to_a_random_string")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # Token valid for 24 hours

    # --- 5. Email (SMTP) Configuration ---
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_SERVER = "64.233.184.108"
    SMTP_PORT = 465

    # --- 6. Validation ---
    if not GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY is missing in .env")
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        print("WARNING: Google OAuth keys are missing in .env")
    # 🚨 FIX 3: Add validation for the new required URLs
    if not GOOGLE_REDIRECT_URI or not FRONTEND_URL:
        print("WARNING: GOOGLE_REDIRECT_URI or FRONTEND_URL is missing in .env/Render config")
