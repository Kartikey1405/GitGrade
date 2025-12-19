

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze, auth, payment
from app.database import engine
from app import entity  

import uvicorn
import threading
import time
import requests 
from app.config import Config
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


entity.Base.metadata.create_all(bind=engine)


def heartbeat_ping():

    url = Config.RENDER_EXTERNAL_URL
    if not url:
        logger.warning("RENDER_EXTERNAL_URL not set. Keep-Alive thread stopped.")
        return

    
    interval_seconds = 14 * 60 

    while True:
        try:
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Keep-Alive ping successful. Status: {response.status_code}")
            else:
                
                logger.warning(f"Keep-Alive ping failed. Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Keep-Alive exception: {e}")
            
        
        time.sleep(interval_seconds)

def start_keep_alive_thread():
    """Starts the heartbeat_ping function in a background thread."""
    logger.info("Starting Keep-Alive background thread...")
    
    
    thread = threading.Thread(target=heartbeat_ping, daemon=True)
    thread.start()


app = FastAPI(
    title="GitGrade API",
    description="Backend for GitHub Analysis Hackathon Project",
    version="2.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(analyze.router, prefix="/api/analyze", tags=["Analysis"])
app.include_router(payment.router, prefix="/api/payment", tags=["Payment"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])


@app.on_event("startup")
async def startup_event():
   
    start_keep_alive_thread()

@app.get("/")
def home():
    return {"message": "GitGrade 2.0 Backend is Running Successfully!"}

if __name__ == "__main__":
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
