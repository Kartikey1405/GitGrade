from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze, auth, payment 

import uvicorn
import threading
import time
import requests #  REQUIRES 'requests' in requirements.txt
from app.config import Config
import logging

# --- Setup Logging for Keep-Alive ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# --- Keep-Alive Functions ---
def heartbeat_ping():
    # Use the URL you set in the Render environment variables
    url = Config.RENDER_EXTERNAL_URL
    if not url:
        logger.warning("RENDER_EXTERNAL_URL not set. Keep-Alive thread stopped.")
        return

    # Interval in seconds: 14 minutes * 60 seconds/minute = 840 seconds
    interval_seconds = 14 * 60 

    while True:
        try:
            # Send a simple GET request to your own service
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                logger.info(f" Keep-Alive ping successful. Status: {response.status_code}")
            else:
                # Log non-200 responses
                logger.warning(f" Keep-Alive ping failed. Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f" Keep-Alive exception: {e}")
            
        # Wait for the defined interval before pinging again
        time.sleep(interval_seconds)

def start_keep_alive_thread():
    """Starts the heartbeat_ping function in a background thread."""
    logger.info("Starting Keep-Alive background thread...")
    
    # Set daemon=True so the thread automatically exits when the main process exits
    thread = threading.Thread(target=heartbeat_ping, daemon=True)
    thread.start()
# ----------------------------


# Initialize the App
app = FastAPI(
    title="GitGrade API",
    description="Backend for GitHub Analysis Hackathon Project",
    version="2.0"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the Routers
app.include_router(analyze.router, prefix="/api/analyze", tags=["Analysis"])
app.include_router(payment.router, prefix="/api/payment", tags=["Payment"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])


@app.on_event("startup")
async def startup_event():
    #  Start the keep-alive thread when the application starts
    start_keep_alive_thread()
    # You may also want to ensure your email service is using the API method
    # and not the old smtplib method which was causing issues.

@app.get("/")
def home():
    return {"message": "GitGrade 2.0 Backend is Running Successfully!"}

if __name__ == "__main__":
    # Run the server on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
