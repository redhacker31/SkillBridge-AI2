from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base

class Analysis(Base):
    """Database model for storing resume analysis results."""
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    career_goal = Column(String, nullable=False)
    
    status = Column(String, nullable=False, default="pending")
    
    resume_score = Column(Integer, nullable=True)
    ats_score = Column(Integer, nullable=True)
    
    # Store lists/objects as JSON
    personal_info = Column(JSON, nullable=True)
    resume_summary = Column(String, nullable=True)
    resume_score_breakdown = Column(JSON, nullable=True)
    ats_score_breakdown = Column(JSON, nullable=True)
    
    skill_categories = Column(JSON, nullable=True)
    
    strengths = Column(JSON, nullable=True)
    weaknesses = Column(JSON, nullable=True)
    project_analysis = Column(JSON, nullable=True)
    experience_analysis = Column(JSON, nullable=True)
    
    career_readiness = Column(JSON, nullable=True)
    interview_readiness = Column(JSON, nullable=True)
    interview_probability = Column(JSON, nullable=True)
    visual_roadmap = Column(JSON, nullable=True)
    
    # Phase XIII Fields
    resume_completeness = Column(JSON, nullable=True)
    domain = Column(String, nullable=True)
    debug_info = Column(JSON, nullable=True)
    
    # Existing Fields
    ats_suggestions = Column(JSON, nullable=True)
    present_skills = Column(JSON, nullable=True)
    missing_skills = Column(JSON, nullable=True)
    
    # Gap Metrics
    skill_coverage_percentage = Column(Integer, nullable=True)
    total_required_skills = Column(Integer, nullable=True)
    skills_found_count = Column(Integer, nullable=True)
    skills_missing_count = Column(Integer, nullable=True)
    
    roadmap = Column(JSON, nullable=True)
    courses = Column(JSON, nullable=True)
    projects = Column(JSON, nullable=True)
    internships = Column(JSON, nullable=True)
    certifications = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Analysis id={self.id} user_id={self.user_id} resume_score={self.resume_score}>"
