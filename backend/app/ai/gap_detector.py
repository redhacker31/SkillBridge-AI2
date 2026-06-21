import json
import os
import numpy as np

# Lazily load semantic model
_model = None

def get_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            print(f"Failed to load sentence-transformers model: {e}")
            _model = False
    return _model

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
            
    return {"required_skills": {}, "optional_skills": []}

def detect_skill_gap(user_skills: list[str], career_goal: str) -> dict:
    db = load_careers_db()
    career_data = get_career_data(career_goal, db)
    
    required_skills_dict = career_data.get("required_skills", {})
    required_skills = list(required_skills_dict.keys())
    optional_skills = career_data.get("optional_skills", [])
    
    present_skills = set()
    missing_skills_names = []
    
    user_skills_lower = [s.lower() for s in user_skills]
    
    unmatched_required = []
    for req_skill in required_skills:
        if req_skill.lower() in user_skills_lower:
            present_skills.add(req_skill)
        else:
            unmatched_required.append(req_skill)
            
    # Semantic matching for required skills
    model = get_model()
    if model and unmatched_required and user_skills:
        from sklearn.metrics.pairwise import cosine_similarity
        user_embeddings = model.encode(user_skills)
        req_embeddings = model.encode(unmatched_required)
        sim_matrix = cosine_similarity(req_embeddings, user_embeddings)
        
        THRESHOLD = 0.75
        for i, req_skill in enumerate(unmatched_required):
            best_match_idx = np.argmax(sim_matrix[i])
            best_match_score = sim_matrix[i][best_match_idx]
            if best_match_score >= THRESHOLD:
                present_skills.add(req_skill)
            else:
                missing_skills_names.append(req_skill)
    else:
        missing_skills_names = unmatched_required
        
    # Build MissingSkill objects with Priority
    missing_skills_objs = [
        {"skill": skill, "priority": required_skills_dict.get(skill, "Medium")}
        for skill in missing_skills_names
    ]
    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    missing_skills_objs.sort(key=lambda x: priority_order.get(x["priority"], 4))
    
    # Calculate coverage
    total = len(required_skills)
    found = len(present_skills)
    coverage = int((found / total * 100)) if total > 0 else 100
    
    # --- PHASE XII: Skill Categorization ---
    core_skills = list(present_skills)
    preferred_skills = []
    bonus_skills = []
    unrelated_skills = []
    
    # All required are in core. What about user skills not in required?
    for us in user_skills:
        if us in present_skills or us.lower() in [s.lower() for s in present_skills]:
            continue
            
        # Is it in optional?
        if us.lower() in [s.lower() for s in optional_skills]:
            preferred_skills.append(us)
            continue
            
        # If we have the model, check if it's semantically close to any optional
        is_preferred = False
        if model and optional_skills:
            from sklearn.metrics.pairwise import cosine_similarity
            us_emb = model.encode([us])
            opt_emb = model.encode(optional_skills)
            sims = cosine_similarity(us_emb, opt_emb)[0]
            if np.max(sims) > 0.70:
                is_preferred = True
                preferred_skills.append(us)
                
        if not is_preferred:
            # Check if it's a known tech skill from the entire DB vs just a random word
            is_tech = False
            for c_data in db.values():
                all_c_skills = list(c_data.get("required_skills", {}).keys()) + c_data.get("optional_skills", [])
                if us.lower() in [s.lower() for s in all_c_skills]:
                    is_tech = True
                    break
            
            if is_tech:
                bonus_skills.append(us)
            else:
                unrelated_skills.append(us)

    return {
        "present": sorted(list(present_skills)),
        "missing": missing_skills_objs,
        "skill_coverage_percentage": coverage,
        "total_required_skills": total,
        "skills_found_count": found,
        "skills_missing_count": len(missing_skills_objs),
        "skill_categories": {
            "core": sorted(core_skills),
            "preferred": sorted(preferred_skills),
            "bonus": sorted(bonus_skills),
            "unrelated": sorted(unrelated_skills)
        }
    }
