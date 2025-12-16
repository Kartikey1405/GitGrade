from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    # We removed 'picture' to keep it clean
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship: One user can have many analyses
    analyses = relationship("Analysis", back_populates="owner")

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    github_url = Column(String)
    repo_name = Column(String)
    
    # Store the AI scores and summary
    overall_score = Column(Float)
    summary = Column(Text)
    
    # Store the full JSON result for caching (The Magic Column)
    full_json_result = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship link back to user
    owner = relationship("User", back_populates="analyses")