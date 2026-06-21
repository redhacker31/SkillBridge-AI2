import logging
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db, SessionLocal
from app.routers.auth import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import Analysis
from app.schemas.resume import ResumeResponse, ParsedResumeResponse
from app.services import resume_service
from app.ai.resume_parser import extract_text
from app.ai.section_detector import detect_sections
from app.ai.information_extractor import extract_information
from app.ai.analyzer import analyze_resume
from app.schemas.analysis import AnalysisRequest

logger = logging.getLogger("skillbridge.router.resume")

router = APIRouter()

def background_analyze(resume_id: int, user_id: int, career_goal: str, analysis_id: int):
    """
    Background worker to execute the long-running semantic analysis pipeline.
    """
    db = SessionLocal()
    try:
        resume_record = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume_record:
            return
            
        logger.info("Background analysis started for resume_id=%d", resume_id)
        
        raw_text = extract_text(resume_record.file_path)
        sections = detect_sections(raw_text)
        parsed_data = extract_information(sections, raw_text)
        
        analysis_result = analyze_resume(parsed_data, raw_text, career_goal)
        
        # Update the database
        db_analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if db_analysis:
            db_analysis.status = "completed"
            db_analysis.personal_info = analysis_result["personal_info"]
            db_analysis.resume_summary = analysis_result["resume_summary"]
            
            db_analysis.resume_score = analysis_result["resume_score"]
            db_analysis.resume_score_breakdown = analysis_result["resume_score_breakdown"]
            
            db_analysis.ats_score = analysis_result["ats_score"]
            db_analysis.ats_score_breakdown = analysis_result["ats_score_breakdown"]
            db_analysis.ats_suggestions = analysis_result["ats_suggestions"]
            
            db_analysis.skill_categories = analysis_result["skill_categories"]
            db_analysis.skill_coverage_percentage = analysis_result["skill_coverage_percentage"]
            db_analysis.total_required_skills = analysis_result["total_required_skills"]
            db_analysis.skills_found_count = analysis_result["skills_found_count"]
            db_analysis.skills_missing_count = analysis_result["skills_missing_count"]
            
            db_analysis.present_skills = analysis_result["present_skills"]
            db_analysis.missing_skills = analysis_result["missing_skills"]
            
            db_analysis.strengths = analysis_result["strengths"]
            db_analysis.weaknesses = analysis_result["weaknesses"]
            
            db_analysis.project_analysis = analysis_result["project_analysis"]
            db_analysis.experience_analysis = analysis_result["experience_analysis"]
            
            db_analysis.career_readiness = analysis_result["career_readiness"]
            db_analysis.interview_readiness = analysis_result["interview_readiness"]
            db_analysis.interview_probability = analysis_result["interview_probability"]
            db_analysis.visual_roadmap = analysis_result["visual_roadmap"]
            
            db_analysis.resume_completeness = analysis_result["resume_completeness"]
            db_analysis.domain = analysis_result["domain"]
            db_analysis.debug_info = analysis_result["debug_info"]
            
            db_analysis.roadmap = analysis_result["roadmap"]
            db_analysis.certifications = analysis_result.get("certifications", [])
            db_analysis.courses = analysis_result["courses"]
            db_analysis.projects = analysis_result["projects"]
            db_analysis.internships = analysis_result["internships"]
            db.commit()
            
        logger.info("Background analysis completed for resume_id=%d", resume_id)
        
    except Exception as e:
        logger.error("Background analysis failed: %s", e, exc_info=True)
        db_analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if db_analysis:
            db_analysis.status = "failed"
            db.commit()
    finally:
        db.close()


@router.post("/upload", response_model=ResumeResponse)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume_db = resume_service.upload_resume(db=db, user_id=current_user.id, file=file)
    return resume_db


@router.post("/{resume_id}/analyze")
def analyze_resume_endpoint(
    resume_id: int,
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Creates a pending analysis record and dispatches the job to the background.
    """
    resume_record = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.user_id == current_user.id)
        .first()
    )
    if not resume_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    # 1. Create a pending Analysis record
    db_analysis = Analysis(
        user_id=current_user.id,
        resume_id=resume_id,
        career_goal=request.career_goal,
        status="pending"
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    # 2. Dispatch to background
    background_tasks.add_task(
        background_analyze,
        resume_id=resume_id,
        user_id=current_user.id,
        career_goal=request.career_goal,
        analysis_id=db_analysis.id
    )

    return {"message": "Analysis started", "analysis_id": db_analysis.id, "status": "pending"}


@router.get("/analysis/{analysis_id}/status")
def get_analysis_status(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Poll the status of a background analysis job.
    """
    db_analysis = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id).first()
    if not db_analysis:
        raise HTTPException(status_code=404, detail="Analysis not found.")
        
    return {
        "id": db_analysis.id,
        "status": db_analysis.status
    }
