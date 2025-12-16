# from fastapi import APIRouter, HTTPException, Depends
# from fastapi.responses import RedirectResponse
# from app.models import GoogleAuthRequest, Token
# from app.services.auth_service import AuthService

# router = APIRouter()
# auth_service = AuthService()

# # --- THE FIX: Redirect to Live Vercel Site ---
# # This catches the user returning from Google and sends them 
# # to your deployed Vercel frontend, not Localhost.
# @router.get("/callback")
# async def auth_callback(code: str):
#     # 👇 This is your live Vercel URL
#     frontend_url = "https://git-grade-gamma.vercel.app"
    
#     # Redirects browser to: https://git-grade-gamma.vercel.app/auth/callback?code=...
#     return RedirectResponse(f"{frontend_url}/auth/callback?code={code}")

# # --- Existing Login Logic (Unchanged) ---
# @router.post("/google", response_model=Token)
# async def login_google(request: GoogleAuthRequest):
#     """
#     Exchanges the Google Authorization Code for a JWT Access Token.
#     """
#     try:
#         # 1. Verify code with Google & Get User Info
#         user_info = await auth_service.verify_google_token(request.code)
        
#         # 2. Create a Session Token (JWT) containing their email
#         access_token = auth_service.create_access_token(
#             data={"sub": user_info.email}
#         )
        
#         return {"access_token": access_token, "token_type": "bearer"}
        
#     except Exception as e:
#         # It's often helpful to print the error to the console for debugging
#         print(f"Login Error: {e}")
#         raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")




from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from app.models import GoogleAuthRequest, Token
from app.services.auth_service import AuthService
from app.config import Config  # ✅ FIXED: Import Config

router = APIRouter()
auth_service = AuthService()

# --- THE FIX: Redirect to Frontend (Dynamic) ---
@router.get("/callback")
async def auth_callback(code: str):
    # ✅ FIXED: Use the variable from Config, not a hardcoded string.
    # Locally, this will be "http://localhost:..."
    # On Cloud, this will be "https://git-grade-gamma.vercel.app"
    frontend_url = Config.FRONTEND_URL
    
    print(f"🔄 Redirecting to Frontend: {frontend_url}") 
    
    # Redirects browser to the correct frontend
    return RedirectResponse(f"{frontend_url}/auth/callback?code={code}")

# --- Existing Login Logic (Unchanged) ---
@router.post("/google", response_model=Token)
async def login_google(request: GoogleAuthRequest):
    """
    Exchanges the Google Authorization Code for a JWT Access Token.
    """
    try:
        user_info = await auth_service.verify_google_token(request.code)
        access_token = auth_service.create_access_token(
            data={"sub": user_info.email}
        )
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        print(f"Login Error: {e}")
        raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")