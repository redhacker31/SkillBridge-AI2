from typing import Any
from .skill_extractor import refine_skills
from .scorer import calculate_resume_score, calculate_ats_score
from .gap_detector import detect_skill_gap, get_career_data, load_careers_db
from .recommender import generate_recommendations

def generate_resume_summary(parsed_data: dict, gap_results: dict, career_goal: str, skill_intel: dict) -> str:
    """Module 15: Generate a personalized 3-5 sentence professional summary."""
    name = parsed_data.get("name") or "This candidate"
    edu = parsed_data.get("education", [])
    exp = parsed_data.get("experience", [])
    proj = parsed_data.get("projects", [])
    
    # Determine experience level
    if len(exp) > 3:
        level_desc = "an experienced professional"
    elif len(exp) > 0:
        level_desc = "a professional with early career experience"
    elif len(edu) > 0:
        level_desc = "a student or recent graduate"
    else:
        level_desc = "an entry-level candidate"
        
    # Build education context
    edu_context = ""
    if edu:
        first = edu[0]
        degree = first.get("degree") or ""
        branch = first.get("branch") or ""
        inst = first.get("institution") or ""
        parts = [p for p in [degree, branch] if p]
        if parts and inst:
            edu_context = f" with a {' in '.join(parts)} from {inst}"
        elif parts:
            edu_context = f" with a {' in '.join(parts)}"
    
    # Build skills context from the intelligence engine
    tech_skills = [s["skill"] for s in skill_intel.get("technical", [])]
    domain_skills = [s["skill"] for s in skill_intel.get("domain", [])]
    prof_skills = [s["skill"] for s in skill_intel.get("professional", [])]
    
    all_top = (tech_skills[:3] + domain_skills[:2])[:4]
    skills_text = ", ".join(all_top) if all_top else "foundational concepts"
    
    # Sentence 1: Identity
    summary = f"{name} is {level_desc}{edu_context}. "
    
    # Sentence 2: Skills
    if tech_skills or domain_skills:
        summary += f"The candidate demonstrates proficiency in {skills_text}. "
    else:
        summary += "The resume does not highlight specific technical or domain skills. "
        
    # Sentence 3: Experience/Projects
    if len(proj) > 0 and len(exp) > 0:
        summary += f"They have completed {len(proj)} project(s) and possess {len(exp)} professional experience record(s). "
    elif len(proj) > 0:
        summary += f"They have completed {len(proj)} project(s) but lack formal work experience. "
    elif len(exp) > 0:
        summary += f"They have {len(exp)} professional experience record(s) but no documented projects. "
    else:
        summary += "The resume lacks both project portfolio and professional experience. "
        
    # Sentence 4: Gap / Readiness
    missing = gap_results.get("missing", [])
    if len(missing) > 2:
        top_missing = [m["skill"] for m in missing[:2]]
        summary += f"To target a {career_goal} role, they should prioritize learning {' and '.join(top_missing)}."
    elif len(missing) > 0:
        summary += f"Minor skill gaps remain for the {career_goal} role, but the foundation is solid."
    else:
        summary += f"They are strongly aligned for a {career_goal} role."
        
    return summary

def generate_strengths_weaknesses(parsed_data: dict, gap_results: dict) -> tuple[list[str], list[str]]:
    strengths = []
    weaknesses = []
    
    if gap_results["skill_coverage_percentage"] > 80:
        strengths.append("Exceptional core skill coverage for the target role.")
    elif gap_results["skill_coverage_percentage"] > 50:
        strengths.append("Solid foundation in required technical skills.")
        
    if len(parsed_data.get("experience", [])) > 0:
        strengths.append("Possesses practical work experience or internships.")
    else:
        weaknesses.append("No professional experience found. Consider internships.")
        
    if len(parsed_data.get("projects", [])) >= 2:
        strengths.append("Good academic or personal project portfolio.")
    else:
        weaknesses.append("Lacks sufficient project portfolio to demonstrate skills.")
        
    if parsed_data.get("github"):
        strengths.append("GitHub profile is available for code review.")
    else:
        weaknesses.append("No GitHub profile linked. Hard to verify coding ability.")
        
    if not parsed_data.get("linkedin"):
        weaknesses.append("Weak or missing LinkedIn profile.")
        
    missing_critical = [m for m in gap_results["missing"] if m["priority"] == "Critical"]
    if missing_critical:
        weaknesses.append(f"Missing critical industry skills like {missing_critical[0]['skill']}.")
        
    return strengths, weaknesses

def analyze_projects(projects: list[dict], gap_results: dict) -> list[dict]:
    analyzed = []
    for p in projects:
        tech = p.get("technologies", "Not specified")
        tech_list = [t.strip().lower() for t in tech.split(",")]
        
        complexity = "Basic"
        if len(tech_list) > 3 or any(k in tech for k in ["AWS", "Docker", "Machine Learning", "React", "Node"]):
            complexity = "Intermediate"
        if "Kubernetes" in tech or "Microservices" in tech or "Deep Learning" in tech:
            complexity = "Advanced"
            
        evaluation = f"A {complexity.lower()} project utilizing {tech}."
        suggestions = []
        if complexity == "Basic":
            suggestions.append("Add authentication or a database.")
            suggestions.append("Deploy the application online.")
        else:
            suggestions.append("Write comprehensive API documentation.")
            suggestions.append("Set up a CI/CD pipeline.")
            
        analyzed.append({
            "name": p.get("title", "Untitled Project"),
            "technologies": tech,
            "complexity": complexity,
            "evaluation": evaluation,
            "suggestions": suggestions,
            "relevant_roles": ["Software Engineer", "Full Stack Developer"] if complexity != "Basic" else ["Intern"]
        })
    return analyzed

def analyze_experience(experience: list[dict]) -> list[dict]:
    analyzed = []
    for e in experience:
        role = e.get("role") or "Unknown Role"
        company = e.get("company") or "Unknown Company"
        evaluation = f"Professional experience as a {role}."
        if "intern" in role.lower():
            evaluation = "Valuable internship experience demonstrating early career capability."
            
        analyzed.append({
            "role": role,
            "company": company,
            "duration": e.get("duration") or "Duration specified in resume",
            "evaluation": evaluation
        })
    return analyzed

def calculate_career_readiness(user_skills: list[str]) -> list[dict]:
    db = load_careers_db()
    results = []
    user_skills_lower = set([s.lower() for s in user_skills])
    
    for key, data in db.items():
        reqs = set(data.get("required_skills", {}).keys())
        if not reqs:
            continue
        matches = reqs.intersection(user_skills_lower)
        score = int((len(matches) / len(reqs)) * 100)
        results.append({
            "career": data.get("name", key),
            "match_percentage": score
        })
        
    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    return results[:5]

def calculate_interview_probability(resume_score: int, ats_score: int, exp_count: int, proj_count: int) -> list[dict]:
    base_score = (resume_score + ats_score) / 2
    probs = []
    
    # 1. FAANG / Top Tier
    p1 = int(base_score * 0.4 + (exp_count * 10) + (proj_count * 5))
    if p1 > 95: p1 = 95
    r1 = "Requires exceptional resume, multiple internships, and complex deployed projects."
    if exp_count == 0: r1 = "No internship experience significantly reduces probability."
    probs.append({"company": "Google SWE Internship", "probability": p1, "reason": r1})
    
    # 2. Tier 1 Tech
    p2 = int(base_score * 0.5 + (exp_count * 8) + (proj_count * 6))
    if p2 > 98: p2 = 98
    probs.append({"company": "Microsoft SDE Intern", "probability": p2, "reason": "Focuses heavily on core computer science foundations and academic projects."})
    
    # 3. Mass Recruiters / Services
    p3 = int(base_score * 0.9 + (proj_count * 5))
    if p3 > 99: p3 = 99
    probs.append({"company": "TCS Digital", "probability": p3, "reason": "High probability due to decent ATS score and foundational skills."})
    
    # 4. Another Services
    p4 = int(base_score * 0.95)
    if p4 > 99: p4 = 99
    probs.append({"company": "Accenture ASE", "probability": p4, "reason": "Matches basic filtering criteria for mass recruitment."})
    
    # 5. Startups
    p5 = int(base_score * 0.7 + (proj_count * 15))
    if p5 > 90: p5 = 90
    r5 = "Startups heavily weight practical project experience and modern tech stacks."
    if proj_count == 0: r5 = "Startups rarely hire without deployed project proof."
    probs.append({"company": "Startup AI/Dev Intern", "probability": p5, "reason": r5})
    
    return probs

def generate_visual_roadmap(career_goal: str, missing_skills: list[dict]) -> list[dict]:
    db = load_careers_db()
    career_data = get_career_data(career_goal, db)
    base_roadmap = career_data.get("roadmap", [])
    
    steps = []
    # If there are missing skills, interleave them as specific roadmap steps
    missing_names = [m["skill"] for m in missing_skills]
    
    phases = ["Foundation", "Intermediate", "Advanced", "Interview Ready"]
    for i, step_text in enumerate(base_roadmap):
        resource = "SkillBridge Curated Guide"
        mini_proj = f"Implement a basic concept using {step_text.split()[-1]}"
        
        # If this roadmap step mentions a missing skill, highlight it
        for m in missing_names:
            if m.lower() in step_text.lower():
                resource = f"Interactive Course on {m}"
                mini_proj = f"Build a {m} microservice"
                
        phase_idx = min(i // 2, 3)
        steps.append({
            "step_number": i + 1,
            "title": f"[{phases[phase_idx]}] {step_text.title()}",
            "estimated_duration": "2 weeks",
            "resource": resource,
            "mini_project": mini_proj
        })
        
    if not steps:
        steps = [
            {"step_number": 1, "title": "Learn Fundamentals", "estimated_duration": "4 weeks", "resource": "Documentation", "mini_project": "Hello World"}
        ]
        
    return steps

def analyze_resume(parsed_data: dict, full_text: str, career_goal: str) -> dict[str, Any]:
    """
    Phase XII: Orchestrates the AI Career Intelligence Report
    """
    
    # Phase XIII: Skill Intelligence Engine
    raw_skills = parsed_data.get("raw_skills", "")
    skill_intelligence = refine_skills(raw_skills, full_text)
    
    # Flatten technical and domain skills for scoring and gap detection
    refined_skills = [s["skill"] for s in skill_intelligence["technical"]] + \
                     [s["skill"] for s in skill_intelligence["domain"]]
    
    # Module 3: Resume Type Detection
    domain = "Software Engineering"
    if skill_intelligence["domain"]:
        domain = "Non-Software / Specialized"
        # Can be refined further based on the specific domain skills found
        
    # Module 14: Resume Completeness
    completeness_fields = {
        "Personal Details": bool(parsed_data.get("name") and parsed_data.get("email")),
        "Education": len(parsed_data.get("education", [])) > 0,
        "Projects": len(parsed_data.get("projects", [])) > 0,
        "Experience": len(parsed_data.get("experience", [])) > 0,
        "Skills": len(refined_skills) > 0,
        "Professional Links": bool(parsed_data.get("github") or parsed_data.get("linkedin") or parsed_data.get("portfolio"))
    }
    completed_count = sum(1 for v in completeness_fields.values() if v)
    completeness_score = int((completed_count / len(completeness_fields)) * 100)
    
    resume_completeness = {
        "score": completeness_score,
        "breakdown": completeness_fields
    }
    
    # 2. Score Breakdowns
    resume_score_data = calculate_resume_score(parsed_data, refined_skills, career_goal)
    gap_results = detect_skill_gap(refined_skills, career_goal)
    
    # Inject intelligence reasoning into missing skills
    for m in gap_results["missing"]:
        m["reason"] = f"A {m['priority'].lower()} requirement for {career_goal} roles."
        
    ats_score_data = calculate_ats_score(parsed_data, full_text, refined_skills, gap_results["missing"])
    
    # 4. Intelligence Generation
    summary = generate_resume_summary(parsed_data, gap_results, career_goal, skill_intelligence)
    strengths, weaknesses = generate_strengths_weaknesses(parsed_data, gap_results)
    
    proj_analysis = analyze_projects(parsed_data.get("projects", []), gap_results)
    exp_analysis = analyze_experience(parsed_data.get("experience", []))
    
    career_readiness = calculate_career_readiness(refined_skills)
    
    interview_prob = calculate_interview_probability(
        resume_score_data["score"], 
        ats_score_data["ats_score"], 
        len(parsed_data.get("experience", [])), 
        len(parsed_data.get("projects", []))
    )
    
    visual_roadmap = generate_visual_roadmap(career_goal, gap_results["missing"])
    
    # 5. Recommendations
    recommendations = generate_recommendations(gap_results["missing"], career_goal)
    
    # Build Personal Info
    edu_list = parsed_data.get("education", [])
    first_edu = edu_list[0] if edu_list else {}
    
    personal_info = {
        "name": parsed_data.get("name", ""),
        "email": parsed_data.get("email", ""),
        "phone": parsed_data.get("phone", ""),
        "github": parsed_data.get("github", ""),
        "linkedin": parsed_data.get("linkedin", ""),
        "college": first_edu.get("institution") if first_edu.get("institution") else "Not Specified",
        "degree": first_edu.get("degree") if first_edu.get("degree") else "Not Specified",
        "graduation_year": first_edu.get("year") if first_edu.get("year") else "Not Specified"
    }
    
    # Module 17: Parser Debug Mode
    import time
    debug_info = {
        "domain_detected": domain,
        "parsing_confidence": parsed_data.get("parsing_confidence", 0),
        "skill_intelligence": skill_intelligence,
        "raw_parsed_data": parsed_data
    }
    
    # Interview Readiness
    tech_ready = gap_results["skill_coverage_percentage"]
    proj_ready = min(100, len(parsed_data.get("projects", [])) * 25)
    res_ready = resume_score_data["score"]
    overall = int((tech_ready + proj_ready + res_ready) / 3)
    
    interview_readiness = {
        "overall": overall,
        "technical_readiness": tech_ready,
        "project_readiness": proj_ready,
        "resume_readiness": res_ready,
        "reason": f"Overall score of {overall}% based on {tech_ready}% tech, {proj_ready}% projects, and {res_ready}% resume strength."
    }

    # Build the Analysis object
    analysis_result = {
        "personal_info": personal_info,
        "resume_summary": summary,
        
        "resume_score": resume_score_data["score"],
        "resume_score_breakdown": resume_score_data["breakdown"],
        
        "ats_score": ats_score_data["ats_score"],
        "ats_score_breakdown": ats_score_data["breakdown"],
        "ats_suggestions": ats_score_data["suggestions"],
        
        "skill_categories": gap_results["skill_categories"],
        "skill_coverage_percentage": gap_results["skill_coverage_percentage"],
        "total_required_skills": gap_results["total_required_skills"],
        "skills_found_count": gap_results["skills_found_count"],
        "skills_missing_count": gap_results["skills_missing_count"],
        
        "present_skills": gap_results["present"],
        "missing_skills": gap_results["missing"],
        
        "strengths": strengths,
        "weaknesses": weaknesses,
        
        "project_analysis": proj_analysis,
        "experience_analysis": exp_analysis,
        
        "career_readiness": career_readiness,
        "interview_readiness": interview_readiness,
        "interview_probability": interview_prob,
        
        "visual_roadmap": visual_roadmap,
        
        "roadmap": recommendations.get("roadmap", []),
        "certifications": recommendations.get("certifications", []),
        "courses": recommendations["courses"],
        "projects": recommendations["projects"],
        "internships": recommendations["internships"],
        
        "resume_completeness": resume_completeness,
        "domain": domain,
        "debug_info": debug_info
    }
    
    return analysis_result
