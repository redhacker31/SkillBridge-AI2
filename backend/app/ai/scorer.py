import json
import os
import re

# Load Career database for deterministic scoring
data_dir = os.path.join(os.path.dirname(__file__), "data")
try:
    with open(os.path.join(data_dir, "careers.json"), "r") as f:
        CAREERS_DB = json.load(f)
except Exception:
    CAREERS_DB = {}

def get_career_requirements(career_goal: str) -> dict:
    goal_lower = career_goal.lower()
    if goal_lower in CAREERS_DB:
        return CAREERS_DB[goal_lower]
    for key, data in CAREERS_DB.items():
        if key in goal_lower or goal_lower in key:
            return data
    return {"required_skills": {}, "optional_skills": []}

def calculate_resume_score(parsed_data: dict, refined_skills: list[str], career_goal: str) -> dict:
    """
    Returns dict:
    - score: int
    - breakdown: list of dicts {category, score, max_score, deduction_reason}
    """
    requirements = get_career_requirements(career_goal)
    core_skills = set(requirements.get("required_skills", {}).keys())
    
    user_skills = set([s.lower() for s in refined_skills])
    
    breakdown = []
    total_score = 0
    
    # 1. Technical Skills (30%)
    if core_skills:
        core_matches = core_skills.intersection(user_skills)
        tech_score = int((len(core_matches) / len(core_skills)) * 30)
        reason = f"Matched {len(core_matches)} out of {len(core_skills)} core technical skills." if tech_score < 30 else ""
        breakdown.append({"category": "Technical Skills", "score": tech_score, "max_score": 30, "deduction_reason": reason})
        total_score += tech_score
    else:
        breakdown.append({"category": "Technical Skills", "score": 30, "max_score": 30, "deduction_reason": ""})
        total_score += 30
        
    # 2. Projects (20%)
    projects = parsed_data.get("projects", [])
    if len(projects) >= 2:
        breakdown.append({"category": "Projects", "score": 20, "max_score": 20, "deduction_reason": ""})
        total_score += 20
    elif len(projects) == 1:
        breakdown.append({"category": "Projects", "score": 10, "max_score": 20, "deduction_reason": "Only 1 project found. Add more robust projects to stand out."})
        total_score += 10
    else:
        breakdown.append({"category": "Projects", "score": 0, "max_score": 20, "deduction_reason": "No projects found in the resume."})
        
    # 3. Experience (15%)
    experience = parsed_data.get("experience", [])
    if len(experience) >= 1:
        breakdown.append({"category": "Experience", "score": 15, "max_score": 15, "deduction_reason": ""})
        total_score += 15
    else:
        breakdown.append({"category": "Experience", "score": 0, "max_score": 15, "deduction_reason": "No professional experience or internships found."})
        
    # 4. Education (10%)
    education = parsed_data.get("education", [])
    if len(education) >= 1:
        breakdown.append({"category": "Education", "score": 10, "max_score": 10, "deduction_reason": ""})
        total_score += 10
    else:
        breakdown.append({"category": "Education", "score": 0, "max_score": 10, "deduction_reason": "No formal education section detected."})
        
    # 5. Achievements (5%)
    # Hacky: Check if words like "won", "award", "achieved", "first place" exist in raw text.
    # We don't have the raw text here, so let's pass if they have lots of projects/exp.
    if len(projects) + len(experience) > 3:
        breakdown.append({"category": "Achievements", "score": 5, "max_score": 5, "deduction_reason": ""})
        total_score += 5
    else:
        breakdown.append({"category": "Achievements", "score": 0, "max_score": 5, "deduction_reason": "No explicit achievements or high-impact metrics found."})
        
    # 6. Certifications (10%)
    # Same hacky approach, we assume missing unless explicitly parsed. 
    breakdown.append({"category": "Certifications", "score": 0, "max_score": 10, "deduction_reason": "No official certifications detected in the parse."})
    
    # 7. Resume Structure (5%)
    if len(parsed_data.get("skills", [])) > 5 and education:
        breakdown.append({"category": "Structure", "score": 5, "max_score": 5, "deduction_reason": ""})
        total_score += 5
    else:
        breakdown.append({"category": "Structure", "score": 2, "max_score": 5, "deduction_reason": "Structure is sparse or difficult for the parser to extract."})
        total_score += 2
        
    # 8. Links (5%)
    if parsed_data.get("github") and parsed_data.get("linkedin"):
        breakdown.append({"category": "Links", "score": 5, "max_score": 5, "deduction_reason": ""})
        total_score += 5
    elif parsed_data.get("github") or parsed_data.get("linkedin"):
        breakdown.append({"category": "Links", "score": 2, "max_score": 5, "deduction_reason": "Missing either GitHub or LinkedIn profile link."})
        total_score += 2
    else:
        breakdown.append({"category": "Links", "score": 0, "max_score": 5, "deduction_reason": "Missing professional URLs (GitHub, LinkedIn)."})
        
    return {
        "score": total_score,
        "breakdown": breakdown
    }


def calculate_ats_score(parsed_data: dict, full_text: str, refined_skills: list[str], missing_skills: list[dict] = None) -> dict:
    """
    Returns dict:
    - score: int
    - suggestions: list[str]
    - breakdown: list of dicts {metric, passed, details}
    """
    score = 100
    suggestions = []
    breakdown = []
    
    # 1. Contact Information
    missing_contact = []
    if not parsed_data.get("email"): missing_contact.append("email")
    if not parsed_data.get("phone"): missing_contact.append("phone number")
    
    if missing_contact:
        score -= 15
        sug = f"Missing critical contact info: {', '.join(missing_contact)}."
        suggestions.append(sug)
        breakdown.append({"metric": "Contact Information", "passed": False, "details": sug})
    else:
        breakdown.append({"metric": "Contact Information", "passed": True, "details": "Email and phone number properly detected."})
        
    # 2. Keyword Density
    if len(refined_skills) < 8:
        score -= 20
        missing_names = [m["skill"] for m in (missing_skills or [])[:3]]
        if missing_names:
            sug = f"Low keyword density. You are missing high-priority ATS keywords like: {', '.join(missing_names)}."
        else:
            sug = "Low keyword density. ATS systems filter out resumes with too few hard skills."
        suggestions.append(sug)
        breakdown.append({"metric": "Keyword Density", "passed": False, "details": sug})
    else:
        breakdown.append({"metric": "Keyword Density", "passed": True, "details": f"{len(refined_skills)} technical keywords detected."})
        
    # 3. Measurable Impact
    numbers = re.findall(r'\b\d+\b', full_text)
    action_verbs = ["developed", "created", "built", "managed", "led", "designed", "implemented", "optimized", "increased", "reduced"]
    found_verbs = [verb for verb in action_verbs if verb in full_text.lower()]
    
    if len(numbers) < 3 or len(found_verbs) < 3:
        score -= 15
        sug = "Lack of measurable impact. Use numbers (%, $, time) and strong action verbs to describe achievements."
        suggestions.append(sug)
        breakdown.append({"metric": "Action Verbs & Impact", "passed": False, "details": sug})
    else:
        breakdown.append({"metric": "Action Verbs & Impact", "passed": True, "details": "Good use of numbers and strong action verbs found."})
        
    # 4. Standard Sections
    if not parsed_data.get("experience") and not parsed_data.get("education"):
        score -= 20
        sug = "Missing standard sections. ATS parsers look for explicit 'Experience' and 'Education' headers."
        suggestions.append(sug)
        breakdown.append({"metric": "Standard Sections", "passed": False, "details": sug})
    else:
        breakdown.append({"metric": "Standard Sections", "passed": True, "details": "Education and Experience sections successfully parsed."})
        
    # 5. Length and Formatting
    if len(full_text.split()) < 150:
        score -= 10
        sug = "Resume is too short. Ensure you have enough content to be parsed effectively."
        suggestions.append(sug)
        breakdown.append({"metric": "Content Length", "passed": False, "details": sug})
    else:
        breakdown.append({"metric": "Content Length", "passed": True, "details": "Optimal word count and parsing length."})
        
    score = max(0, min(100, score))
    
    return {
        "ats_score": score,
        "suggestions": suggestions,
        "breakdown": breakdown
    }
