from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisResponse

router = APIRouter()

@router.get("/summary", response_model=AnalysisResponse)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get the most recent analysis for the logged-in user to display on the dashboard.
    """
    latest_analysis = (
        db.query(Analysis)
        .filter(Analysis.user_id == current_user.id, Analysis.status == "completed")
        .order_by(desc(Analysis.created_at))
        .first()
    )

    if not latest_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No analysis found for this user."
        )

    # Clean personal_info to handle any None values from parsing
    personal_info = latest_analysis.personal_info or {}
    cleaned_personal_info = {
        "name": personal_info.get("name") or "",
        "email": personal_info.get("email") or "",
        "phone": personal_info.get("phone") or "",
        "github": personal_info.get("github") or "",
        "linkedin": personal_info.get("linkedin") or "",
        "college": personal_info.get("college") or "Not Specified",
        "degree": personal_info.get("degree") or "Not Specified",
        "graduation_year": personal_info.get("graduation_year") or "Not Specified"
    }

    # Convert the DB model back to the expected AnalysisResponse JSON structure
    return AnalysisResponse(
        personal_info=cleaned_personal_info,
        resume_summary=latest_analysis.resume_summary or "",
        domain=latest_analysis.domain or "Software Engineering",
        resume_completeness=latest_analysis.resume_completeness or {"score": 0, "breakdown": {}},
        debug_info=latest_analysis.debug_info or {},
        
        resume_score=latest_analysis.resume_score,
        resume_score_breakdown=latest_analysis.resume_score_breakdown or [],
        
        ats_score=latest_analysis.ats_score,
        ats_score_breakdown=latest_analysis.ats_score_breakdown or [],
        ats_suggestions=latest_analysis.ats_suggestions or [],
        
        skill_categories=latest_analysis.skill_categories or {},
        skill_coverage_percentage=latest_analysis.skill_coverage_percentage or 0,
        total_required_skills=latest_analysis.total_required_skills or 0,
        skills_found_count=latest_analysis.skills_found_count or 0,
        skills_missing_count=latest_analysis.skills_missing_count or 0,
        
        present_skills=latest_analysis.present_skills or [],
        missing_skills=latest_analysis.missing_skills or [],
        
        strengths=latest_analysis.strengths or [],
        weaknesses=latest_analysis.weaknesses or [],
        
        project_analysis=latest_analysis.project_analysis or [],
        experience_analysis=latest_analysis.experience_analysis or [],
        
        career_readiness=latest_analysis.career_readiness or [],
        interview_readiness=latest_analysis.interview_readiness or {},
        interview_probability=latest_analysis.interview_probability or [],
        
        visual_roadmap=latest_analysis.visual_roadmap or [],
        
        roadmap=latest_analysis.roadmap or [],
        certifications=latest_analysis.certifications or [],
        courses=latest_analysis.courses or [],
        projects=latest_analysis.projects or [],
        internships=latest_analysis.internships or []
    )
