import os
from dotenv import load_dotenv

# Load variables from .env file into the system
load_dotenv()

class Config:
    # --- 1. Existing API Keys ---
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PAYMENT_UPI_ID = os.getenv("PAYMENT_UPI_ID", "yourname@upi") 

    # --- 2. GitHub Headers (Automated) ---
    GITHUB_HEADERS = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.com.v3+json"
    } if GITHUB_TOKEN else {}

    # --- 3. Google OAuth Configuration ---
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    
    GOOGLE_REDIRECT_URI = os.getenv(
        "GOOGLE_REDIRECT_URI", 
        "http://localhost:8000/api/auth/callback"
    ) 

    FRONTEND_URL = os.getenv(
        "FRONTEND_URL", 
        "http://localhost:3000"
    ) 

    # --- 4. JWT Security Configuration ---
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "please_change_this_to_a_random_string")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 

    # --- 5. Email (SMTP) Configuration (SWITCHED TO SENDGRID PROTOCOL) ---
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") 
    
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.sendgrid.net")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 2525)) 
    
    # --- 6. RENDER KEEP-ALIVE CONFIGURATION (NEW) ---
    RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
    
    # --- 7. Validation ---
    if not GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY is missing in .env")
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        print("WARNING: Google OAuth keys are missing in .env")
    if not GOOGLE_REDIRECT_URI or not FRONTEND_URL:
        print("WARNING: GOOGLE_REDIRECT_URI or FRONTEND_URL is missing in .env/Render config")
