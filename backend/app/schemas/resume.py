from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ResumeResponse(BaseModel):
    """Schema for returning resume metadata."""
    id: int
    user_id: int
    filename: str
    file_size: int
    content_type: str
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ──────────────────────────────────────────────
# Parsed Resume Response Models
# ──────────────────────────────────────────────

class EducationEntry(BaseModel):
    college: str = ""
    degree: str = ""
    year: str = ""


class ProjectEntry(BaseModel):
    title: str = ""
    technologies: str = ""


class ExperienceEntry(BaseModel):
    company: str = ""
    role: str = ""


class ParsedResumeResponse(BaseModel):
    """Structured JSON response from the resume parser."""
    name: str = ""
    email: str = ""
    phone: str = ""
    github: str = ""
    linkedin: str = ""
    education: list[EducationEntry] = []
    projects: list[ProjectEntry] = []
    experience: list[ExperienceEntry] = []
    skills: list[str] = []
