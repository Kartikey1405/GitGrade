# # from fastapi import APIRouter, HTTPException, Depends
# # from fastapi.responses import RedirectResponse
# # from app.models import GoogleAuthRequest, Token
# # from app.services.auth_service import AuthService
# # from app.config import Config  # ✅ FIXED: Import Config

# # router = APIRouter()
# # auth_service = AuthService()

# # # --- THE FIX: Redirect to Frontend (Dynamic) ---
# # @router.get("/callback")
# # async def auth_callback(code: str):
# #     # ✅ FIXED: Use the variable from Config, not a hardcoded string.
# #     # Locally, this will be "http://localhost:..."
# #     # On Cloud, this will be "https://git-grade-gamma.vercel.app"
# #     frontend_url = Config.FRONTEND_URL
    
# #     print(f"🔄 Redirecting to Frontend: {frontend_url}") 
    
# #     # Redirects browser to the correct frontend
# #     return RedirectResponse(f"{frontend_url}/auth/callback?code={code}")

# # # --- Existing Login Logic (Unchanged) ---
# # @router.post("/google", response_model=Token)
# # async def login_google(request: GoogleAuthRequest):
# #     """
# #     Exchanges the Google Authorization Code for a JWT Access Token.
# #     """
# #     try:
# #         user_info = await auth_service.verify_google_token(request.code)
# #         access_token = auth_service.create_access_token(
# #             data={"sub": user_info.email}
# #         )
# #         return {"access_token": access_token, "token_type": "bearer"}
        
# #     except Exception as e:
# #         print(f"Login Error: {e}")
# #         raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")



# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.responses import RedirectResponse
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app import entity
# from app.config import Config
# import httpx
# from pydantic import BaseModel
# import jwt
# from datetime import datetime, timedelta

# router = APIRouter(prefix="/api/auth", tags=["auth"])

# # Request schema for the Google login
# class LoginRequest(BaseModel):
#     code: str

# # Helper function to create JWT tokens
# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

# @router.post("/google")
# async def login_with_google(request: LoginRequest, db: Session = Depends(get_db)):
#     # 1. Exchange the Authorization Code for a Google Access Token
#     async with httpx.AsyncClient() as client:
#         token_url = "https://oauth2.googleapis.com/token"
#         data = {
#             "client_id": Config.GOOGLE_CLIENT_ID,
#             "client_secret": Config.GOOGLE_CLIENT_SECRET,
#             "code": request.code,
#             "grant_type": "authorization_code",
#             "redirect_uri": Config.GOOGLE_REDIRECT_URI,
#         }
#         response = await client.post(token_url, data=data)
        
#         if response.status_code != 200:
#             print(f"Google Token Error: {response.text}")
#             raise HTTPException(status_code=400, detail="Invalid Google code")
        
#         access_token = response.json().get("access_token")

#         # 2. Get User Info from Google (Email & Name)
#         user_info_response = await client.get(
#             "https://www.googleapis.com/oauth2/v2/userinfo",
#             headers={"Authorization": f"Bearer {access_token}"}
#         )
#         user_info = user_info_response.json()
    
#     email = user_info.get("email")
#     full_name = user_info.get("name")

#     if not email:
#         raise HTTPException(status_code=400, detail="Email not found in Google account")

#     # 3. Database Logic: Check if user exists, otherwise create them
#     user = db.query(entity.User).filter(entity.User.email == email).first()

#     if not user:
#         # Create new user
#         new_user = entity.User(
#             email=email,
#             full_name=full_name
#         )
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
#         print(f"Created new user in DB: {email}")
#         user = new_user
#     else:
#         print(f"User found in DB: {email}")

#     # 4. Create JWT token containing the Database User ID
#     access_token = create_access_token(data={"sub": user.email, "user_id": user.id})

#     return {"access_token": access_token, "token_type": "bearer"}

# @router.get("/callback")
# async def auth_callback(code: str):
#     # Dynamic redirect based on environment (Local vs Cloud)
#     frontend_url = Config.FRONTEND_URL
#     print(f"Redirecting to Frontend: {frontend_url}")
#     return RedirectResponse(f"{frontend_url}/auth/callback?code={code}")



from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import entity
from app.config import Config
import httpx
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

# ✅ FIX: Removed 'prefix="/api/auth"' to prevent double-URL error (404)
router = APIRouter(tags=["auth"])

# Request schema for the Google login
class LoginRequest(BaseModel):
    code: str

# Helper function to create JWT tokens
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

@router.post("/google")
async def login_with_google(request: LoginRequest, db: Session = Depends(get_db)):
    # 1. Exchange the Authorization Code for a Google Access Token
    async with httpx.AsyncClient() as client:
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": Config.GOOGLE_CLIENT_ID,
            "client_secret": Config.GOOGLE_CLIENT_SECRET,
            "code": request.code,
            "grant_type": "authorization_code",
            "redirect_uri": Config.GOOGLE_REDIRECT_URI,
        }
        response = await client.post(token_url, data=data)
        
        if response.status_code != 200:
            print(f"Google Token Error: {response.text}")
            raise HTTPException(status_code=400, detail="Invalid Google code")
        
        access_token = response.json().get("access_token")

        # 2. Get User Info from Google (Email & Name)
        user_info_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = user_info_response.json()
    
    email = user_info.get("email")
    full_name = user_info.get("name")

    if not email:
        raise HTTPException(status_code=400, detail="Email not found in Google account")

    # 3. Database Logic: Check if user exists, otherwise create them
    user = db.query(entity.User).filter(entity.User.email == email).first()

    if not user:
        # Create new user
        new_user = entity.User(
            email=email,
            full_name=full_name
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"Created new user in DB: {email}")
        user = new_user
    else:
        print(f"User found in DB: {email}")

    # 4. Create JWT token containing the Database User ID
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/callback")
async def auth_callback(code: str):
    # Dynamic redirect based on environment (Local vs Cloud)
    frontend_url = Config.FRONTEND_URL
    print(f"Redirecting to Frontend: {frontend_url}")
    return RedirectResponse(f"{frontend_url}/auth/callback?code={code}")