



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


router = APIRouter(tags=["auth"])


class LoginRequest(BaseModel):
    code: str


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

@router.post("/google")
async def login_with_google(request: LoginRequest, db: Session = Depends(get_db)):
 
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

       
        user_info_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = user_info_response.json()
    
    email = user_info.get("email")
    full_name = user_info.get("name")

    if not email:
        raise HTTPException(status_code=400, detail="Email not found in Google account")

   
    user = db.query(entity.User).filter(entity.User.email == email).first()

    if not user:
      
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

 
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/callback")
async def auth_callback(code: str):
    # Dynamic redirect based on environment (Local vs Cloud)
    frontend_url = Config.FRONTEND_URL
    print(f"Redirecting to Frontend: {frontend_url}")
    return RedirectResponse(f"{frontend_url}/auth/callback?code={code}")
