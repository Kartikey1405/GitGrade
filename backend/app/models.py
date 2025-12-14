from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict

# --- Sub-Models for Structured Data (NEW) ---
class RoadmapItem(BaseModel):
    title: str
    description: str
    category: Optional[str] = "General"

class TechStack(BaseModel):
    frontend: List[str] = []
    backend: List[str] = []
    infrastructure: List[str] = []

# --- 1. Analysis Models ---
class AnalyzeRequest(BaseModel):
    github_url: str

class RepoDetails(BaseModel):
    name: str
    owner: str
    description: Optional[str] = None
    stars: int
    forks: int
    open_issues: int
    language: Optional[str] = None

class AnalysisResult(BaseModel):
    details: RepoDetails
    score: int
    summary: str
    
    # UPDATED: Now a list of objects, not strings
    roadmap: List[RoadmapItem] 
    
    # ADDED: Optional tech stack field
    tech_stack: Optional[TechStack] = None 
    
    file_structure: List[str]

# --- 2. Payment Models ---
class PaymentRequest(BaseModel):
    amount: float
    currency: str = "INR"
    message: Optional[str] = "Great tool!"

class PaymentLinkResponse(BaseModel):
    payment_url: str
    transaction_id: str

# --- 3. Authentication Models ---
class GoogleAuthRequest(BaseModel):
    code: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserInfo(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    picture: Optional[str] = None

# --- 4. Email Report Models ---
class SendReportRequest(BaseModel):
    # This must match AnalysisResult structure exactly
    analysis_data: AnalysisResult