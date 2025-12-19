import httpx
from jose import jwt
from datetime import datetime, timedelta
from app.config import Config
from app.models import UserInfo

class AuthService:
    
    async def verify_google_token(self, code: str) -> UserInfo:
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": Config.GOOGLE_CLIENT_ID,
            "client_secret": Config.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": Config.GOOGLE_REDIRECT_URI
        }
        
        async with httpx.AsyncClient() as client:
           
            response = await client.post(token_url, data=data)
            if response.status_code != 200:
                raise Exception("Failed to verify Google code")
            
            google_tokens = response.json()
            access_token = google_tokens.get("access_token")
            
        
            user_info_resp = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            profile = user_info_resp.json()
            
            return UserInfo(
                email=profile.get("email"),
                name=profile.get("name"),
                picture=profile.get("picture")
            )

   
    def create_access_token(self, data: dict):
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        
       
        encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
        return encoded_jwt

   
    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            return payload
        except:
            return None
