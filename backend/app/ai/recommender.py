import json
import os
from typing import Dict, List, Any

# Load careers database
def load_careers_db() -> dict:
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    try:
        with open(os.path.join(data_dir, "careers.json"), "r") as f:
            return json.load(f)
    except Exception:
        return {}

def get_career_data(career_goal: str, db: dict) -> dict:
    goal_lower = career_goal.lower()
    if goal_lower in db:
        return db[goal_lower]
        
    for key, data in db.items():
        if key in goal_lower or goal_lower in key:
            return data
            
    return {}

def generate_recommendations(missing_skills: List[Dict[str, str]], career_goal: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Dynamic Data-Driven Recommendation Engine.
    Filters the career's specialized courses and projects to match EXACTLY the missing skills.
    """
    db = load_careers_db()
    career_data = get_career_data(career_goal, db)
    
    if not career_data:
        return {"courses": [], "projects": [], "internships": []}
        
    missing_skill_names = [ms["skill"].lower() for ms in missing_skills]
    
    recommended_courses = []
    recommended_projects = []
    
    # Recommend courses that teach missing skills
    for course in career_data.get("courses", []):
        addressed = [s.lower() for s in course.get("addressed_skills", [])]
        if any(s in missing_skill_names for s in addressed):
            recommended_courses.append(course)
            
    # Recommend projects that use missing skills
    for project in career_data.get("projects", []):
        addressed = [s.lower() for s in project.get("addressed_skills", [])]
        if any(s in missing_skill_names for s in addressed):
            recommended_projects.append(project)
            
    # If the user has 0 missing skills, just give them some advanced projects anyway
    if not missing_skill_names:
        recommended_projects = career_data.get("projects", [])[:2]
        
    # Return all internships for the role
    internships = career_data.get("internships", [])
    
    # Optional: Fill up to 3 courses/projects if they are empty
    if len(recommended_courses) == 0 and career_data.get("courses"):
        recommended_courses = career_data.get("courses", [])[:2]
    if len(recommended_projects) == 0 and career_data.get("projects"):
        recommended_projects = career_data.get("projects", [])[:2]

    return {
        "courses": recommended_courses[:4],
        "projects": recommended_projects[:4],
        "internships": internships[:3],
        "roadmap": career_data.get("roadmap", []),
        "certifications": career_data.get("certifications", [])
    }
