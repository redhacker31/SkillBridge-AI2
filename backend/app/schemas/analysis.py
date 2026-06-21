from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AnalysisRequest(BaseModel):
    career_goal: str

class Recommendation(BaseModel):
    title: str
    reason: str
    difficulty: str
    estimated_time: str
    prerequisites: List[str] = []
    addressed_skills: List[str] = []

class MissingSkill(BaseModel):
    skill: str
    priority: str

class PersonalInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    github: str = ""
    linkedin: str = ""
    college: str = "Not Specified"
    degree: str = "Not Specified"
    graduation_year: str = "Not Specified"

class ScoreBreakdown(BaseModel):
    category: str
    score: int
    max_score: int
    deduction_reason: str = ""

class AtsBreakdown(BaseModel):
    metric: str
    passed: bool
    details: str

class SkillCategories(BaseModel):
    core: List[str] = []
    preferred: List[str] = []
    bonus: List[str] = []
    unrelated: List[str] = []

class ProjectAnalysis(BaseModel):
    name: str
    technologies: str
    complexity: str
    relevant_roles: List[str] = []
    evaluation: str
    suggestions: List[str] = []

class ExperienceAnalysis(BaseModel):
    duration: str = ""
    role: str
    company: str
    evaluation: str

class CareerReadiness(BaseModel):
    career: str
    match_percentage: int

class VisualRoadmapStep(BaseModel):
    step_number: int
    title: str
    estimated_duration: str
    resource: str
    mini_project: str

class InterviewProbability(BaseModel):
    company: str
    probability: int
    reason: str

class ResumeCompleteness(BaseModel):
    score: int
    breakdown: Dict[str, bool]

class AnalysisResponse(BaseModel):
    """Combined output from the AI Analysis module."""
    personal_info: PersonalInfo = PersonalInfo()
    resume_summary: str = ""
    domain: str = "Software Engineering"
    resume_completeness: ResumeCompleteness = ResumeCompleteness(score=0, breakdown={})
    debug_info: Dict[str, Any] = {}
    
    resume_score: int
    resume_score_breakdown: List[ScoreBreakdown] = []
    
    ats_score: int
    ats_score_breakdown: List[AtsBreakdown] = []
    ats_suggestions: List[str] = []
    
    skill_categories: SkillCategories = SkillCategories()
    skill_coverage_percentage: int = 0
    total_required_skills: int = 0
    skills_found_count: int = 0
    skills_missing_count: int = 0
    
    present_skills: List[str] = []
    missing_skills: List[MissingSkill] = []
    
    strengths: List[str] = []
    weaknesses: List[str] = []
    
    project_analysis: List[ProjectAnalysis] = []
    experience_analysis: List[ExperienceAnalysis] = []
    
    career_readiness: List[CareerReadiness] = []
    interview_readiness: Dict[str, Any] = {}
    interview_probability: List[InterviewProbability] = []
    
    visual_roadmap: List[VisualRoadmapStep] = []
    
    roadmap: List[str] = []
    certifications: List[str] = []
    courses: List[Recommendation] = []
    projects: List[Recommendation] = []
    internships: List[Recommendation] = []
