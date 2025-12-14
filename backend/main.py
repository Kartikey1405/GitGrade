from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze, auth, payment  # Ensure these files exist in app/routers/
import uvicorn

# Initialize the App
app = FastAPI(
    title="GitGrade API",
    description="Backend for GitHub Analysis Hackathon Project",
    version="2.0"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Safe for hackathon)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the Routers
# The prefix "/api/analyze" combined with @router.post("/") creates "/api/analyze/"
app.include_router(analyze.router, prefix="/api/analyze", tags=["Analysis"])
app.include_router(payment.router, prefix="/api/payment", tags=["Payment"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

@app.get("/")
def home():
    return {"message": "GitGrade 2.0 Backend is Running Successfully!"}

if __name__ == "__main__":
    # Run the server on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)