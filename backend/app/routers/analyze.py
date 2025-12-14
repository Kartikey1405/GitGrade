from fastapi import APIRouter, HTTPException, Header, Depends
from app.models import AnalyzeRequest, AnalysisResult, RepoDetails, SendReportRequest, RoadmapItem, TechStack
from app.services.github_service import GitHubService
from app.services.scoring_service import ScoringService
from app.services.ai_service import AIService
from app.services.email_service import EmailService
from app.services.auth_service import AuthService

router = APIRouter()

# Initialize Services
github_service = GitHubService()
scoring_service = ScoringService()
ai_service = AIService()
# These two were missing in your snippet!
email_service = EmailService()
auth_service = AuthService()

# --- Endpoint 1: Analyze Repo (POST /api/analyze/) ---
@router.post("/", response_model=AnalysisResult)
async def analyze_repo(request: AnalyzeRequest):
    try:
        # 1. Parse Owner/Repo from URL
        parts = request.github_url.rstrip("/").split("/")
        if len(parts) < 2:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")
        
        owner = parts[-2]
        repo_name = parts[-1]

        # 2. Fetch Data from GitHub
        print(f"Fetching data for {owner}/{repo_name}...")
        repo_data = await github_service.fetch_repo_data(owner, repo_name)
        
        # 3. Calculate Logic Score (0-100)
        base_score = scoring_service.calculate_score(
            repo_data['metadata'], 
            repo_data['files'], 
            repo_data['readme']
        )

        # 4. Get AI Analysis (Detailed Roadmap & Tech Stack)
        print("Asking Gemini AI (2.5-Flash)...")
        ai_result = await ai_service.analyze_code_quality(
            repo_data['readme'], 
            repo_data['files'], 
            base_score
        )

        # 5. Construct Response
        final_score = min(100, max(0, base_score + ai_result.get('quality_bonus', 0)))

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


# --- Endpoint 2: Send Email Report (POST /api/analyze/send-report) ---
# THIS WAS MISSING
@router.post("/send-report")
async def send_report(
    request: SendReportRequest, 
    authorization: str = Header(None) # Expects "Bearer <token>"
):
    """
    Generates a PDF and emails it to the logged-in user.
    """
    # 1. Check Security (Is user logged in?)
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = authorization.split(" ")[1]
    payload = auth_service.decode_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Session expired. Please login again.")
    
    user_email = payload.get("sub") 

    print(f"📄 Generating PDF for {user_email}...")

    # 2. Generate PDF
    try:
        pdf_path = email_service.generate_pdf(request.analysis_data)
    except Exception as e:
        print(f"❌ PDF Gen Error: {e}")
        raise HTTPException(status_code=500, detail=f"PDF Generation failed: {e}")

    # 3. Send Email
    print(f"📧 Sending email to {user_email}...")
    success = email_service.send_email(user_email, pdf_path)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email via Gmail")
        
    return {"message": f"Report sent successfully to {user_email}"}