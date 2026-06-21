# SkillBridge AI: Interview & Demo Preparation Guide

This document is designed to help you confidently present the SkillBridge AI project to hackathon judges, technical interviewers, or college faculty.

## 1. Project Summary (Elevator Pitch)
"SkillBridge AI is an intelligent career guidance platform. Unlike typical Applicant Tracking Systems (ATS) that simply reject candidates based on keywords, SkillBridge acts as a mentor. It deeply analyzes a user's resume against their target career, detects critical skill gaps, and dynamically generates a personalized, multi-phase learning roadmap complete with tailored course and project recommendations. The entire AI engine runs locally using optimized NLP models, completely eliminating the latency and cost of external LLM APIs."

## 2. Architecture Overview
- **Frontend:** React + TypeScript + Vite. Uses Tailwind CSS for responsive styling, Recharts for data visualization, and Framer Motion for micro-animations.
- **Backend:** Python + FastAPI. Chosen for its high-performance asynchronous capabilities and native integration with PyDantic for strict API schema validation.
- **Database:** SQLite with SQLAlchemy ORM. Keeps the prototype portable and easy to run locally while maintaining relational integrity (Users -> Resumes).
- **AI Engine:** A fully custom NLP pipeline. Uses `PyMuPDF` for accurate text extraction, heavily optimized Regular Expressions for section chunking, and a proprietary matrix (`careers.json`) for skill gap analysis and roadmap generation.

## 3. Key Challenges Solved
1. **Unstructured Resume Data:** Resumes come in thousands of different formats.
   - *Solution:* Built a robust heuristic section detector (`section_detector.py`) that uses ATS-standard heading patterns to reliably chunk data before extraction.
2. **Skill Duplication & Aliases:** A user might write "ReactJS", "React.js", or "React".
   - *Solution:* Implemented a `skill_extractor.py` module with over 150 canonical skills and aliases to perfectly normalize and deduplicate data.
3. **API Latency:** Using external LLMs like OpenAI for resume parsing takes 10+ seconds and costs money.
   - *Solution:* Built the parsing and recommendation engine entirely locally using deterministic logic. Response times are <200ms.

## 4. Suggested Demo Flow (5 Minutes)
1. **[0:00 - 1:00] Registration:** Show the smooth registration and login flow. Explain that JWT tokens secure the session.
2. **[1:00 - 2:00] Resume Upload:** Navigate to the upload screen. Upload a sample PDF resume and set a target career (e.g., "Full Stack Developer").
3. **[2:00 - 3:30] Dashboard:** Walk through the parsed data. Show the Resume Score and the ATS Score. Hover over the "Skill Gaps" to show the AI's reasoning (e.g., "Why Docker is critical").
4. **[3:30 - 5:00] Roadmap:** Click into the Roadmap view. Show how the timeline dynamically grouped learning phases (Foundation -> Interview Ready) based *only* on the skills the candidate is actually missing.

## 5. Potential Interview Questions & Answers

**Q: Why did you choose FastAPI over Django or Express?**
*A:* FastAPI provides automatic Swagger documentation and native Pydantic validation, which ensures our AI engine outputs exact JSON structures. It's also significantly faster for Python workloads compared to Django.

**Q: How does the Skill Gap detection work?**
*A:* The `gap_detector.py` cross-references the normalized skills extracted from the resume against a target career profile stored in `careers.json`. It categorizes missing skills by priority (Critical/High) and outputs a personalized JSON array that the frontend consumes.

**Q: Is the application secure?**
*A:* Yes. Passwords are cryptographically hashed using `passlib` (bcrypt) before hitting the database. All API routes are protected by JWT Bearer tokens, and CORS is strictly limited to the frontend origin.

**Q: How would you scale this for production?**
*A:* I would migrate the SQLite database to PostgreSQL, containerize the FastAPI backend and React frontend using Docker, and deploy them to AWS (ECS) or Render. For the AI database, I would connect it to real-time job scraping APIs to keep the `careers.json` data fresh.
