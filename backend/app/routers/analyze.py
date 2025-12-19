from fastapi import APIRouter, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import entity  
from app.models import AnalyzeRequest, AnalysisResult, RepoDetails, SendReportRequest
from app.services.github_service import GitHubService
from app.services.scoring_service import ScoringService
from app.services.ai_service import AIService
from app.services.email_service import EmailService
from app.config import Config
import jwt

router = APIRouter(tags=["analyze"])


github_service = GitHubService()
scoring_service = ScoringService()
ai_service = AIService()
email_service = EmailService()


@router.post("/", response_model=AnalysisResult)
async def analyze_repo(
    request: AnalyzeRequest, 
    db: Session = Depends(get_db),      
    authorization: str = Header(None)   
):
    try:
      
        parts = request.github_url.rstrip("/").split("/")
        if len(parts) < 2:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")
        
        owner = parts[-2]
        repo_name = parts[-1]

        # 2. Fetch Data
        print(f"Fetching data for {owner}/{repo_name}...")
        repo_data = await github_service.fetch_repo_data(owner, repo_name)
        
        
        base_score = scoring_service.calculate_score(
            repo_data['metadata'], 
            repo_data['files'], 
            repo_data['readme']
        )

        
        print("Asking Gemini AI (2.5-Flash)...")
        ai_result = await ai_service.analyze_code_quality(
            repo_data['readme'], 
            repo_data['files'], 
            base_score
        )

        
        final_score = min(100, max(0, base_score + ai_result.get('quality_bonus', 0)))

      
        if authorization and authorization.startswith("Bearer "):
            try:
              
                token = authorization.split(" ")[1]
                payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
                user_email = payload.get("sub")
                
                
                user = db.query(entity.User).filter(entity.User.email == user_email).first()
                
                if user:
                    print(f" Saving report to Database for: {user.email}")
                    new_analysis = entity.Analysis(
                        user_id=user.id,
                        github_url=request.github_url,
                        repo_name=repo_name,
                        overall_score=final_score,
                        summary=ai_result.get("summary"),
                        full_json_result=ai_result  
                    )
                    db.add(new_analysis)
                    db.commit()
                else:
                    print(" User found in token but not in DB. Skipping save.")
            except Exception as e:
          
                print(f" Warning: Could not save to DB: {e}")

        
        return AnalysisResult(
            details=RepoDetails(
                name=repo_data['metadata'].get('name', repo_name),
                owner=repo_data['metadata'].get('owner', {}).get('login', owner),
                description=repo_data['metadata'].get('description') or "No description provided.",
                stars=repo_data['metadata'].get('stargazers_count', 0),
                forks=repo_data['metadata'].get('forks_count', 0),
                open_issues=repo_data['metadata'].get('open_issues_count', 0),
                language=repo_data['metadata'].get('language') or "Multi-language"
            ),
            score=final_score,
            summary=ai_result.get("summary", "Analysis complete."),
            roadmap=ai_result.get("roadmap", []),      
            tech_stack=ai_result.get("tech_stack"),    
            file_structure=repo_data['files'][:50]     
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"ERROR in analyze_repo: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Analysis failed: {str(e)}")



@router.post("/send-report")
async def send_report(
    request: SendReportRequest, 
    authorization: str = Header(None) 
):
    """
    Generates a PDF and emails it to the logged-in user.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = authorization.split(" ")[1]
    
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        user_email = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired. Please login again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token payload.")

    print(f" Generating PDF for {user_email}...")

    try:
        pdf_path = email_service.generate_pdf(request.analysis_data)
    except Exception as e:
        print(f" PDF Gen Error: {e}")
        raise HTTPException(status_code=500, detail=f"PDF Generation failed: {e}")

    print(f"Sending email to {user_email}...")
    success = email_service.send_email(user_email, pdf_path)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email via Gmail")
        
    return {"message": f"Report sent successfully to {user_email}"}
