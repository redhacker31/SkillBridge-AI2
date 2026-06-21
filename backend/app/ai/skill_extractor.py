import re
import logging
from typing import TypedDict, List

logger = logging.getLogger("skillbridge.ai.skill_extractor")

class SkillMatch(TypedDict):
    skill: str
    confidence: int
    source: str
    category: str

# ──────────────────────────────────────────────
# 1. Technical Skills (150+ entries)
# ──────────────────────────────────────────────
TECHNICAL_SKILLS = {
    # Programming Languages
    "python": ["python", "python3", "python2"],
    "javascript": ["javascript", "js", "ecmascript", "es6", "es2015"],
    "java": ["java", "j2ee", "jdk", "jre"],
    "c++": ["c++", "cpp", "c plus plus"],
    "c#": ["c#", "csharp", "c sharp"],
    "c": ["c language", "ansi c"],
    "go": ["golang", "go lang"],
    "rust": ["rust", "rustlang"],
    "ruby": ["ruby"],
    "php": ["php"],
    "swift": ["swift"],
    "kotlin": ["kotlin"],
    "scala": ["scala"],
    "r": ["r programming", "r language"],
    "dart": ["dart"],
    "perl": ["perl"],
    "lua": ["lua"],
    "haskell": ["haskell"],
    "typescript": ["typescript", "ts"],
    "shell scripting": ["bash", "shell", "shell scripting", "zsh", "powershell"],
    "assembly": ["assembly", "asm", "x86"],
    
    # Frontend Frameworks
    "react": ["react", "reactjs", "react.js", "react js"],
    "angular": ["angular", "angularjs", "angular.js", "angular js"],
    "vue.js": ["vue.js", "vuejs", "vue", "vue js"],
    "svelte": ["svelte", "sveltekit"],
    "next.js": ["next.js", "nextjs", "next js"],
    "nuxt.js": ["nuxt.js", "nuxtjs"],
    "jquery": ["jquery"],
    "bootstrap": ["bootstrap"],
    "tailwind css": ["tailwind", "tailwindcss", "tailwind css"],
    "material ui": ["material ui", "mui"],
    
    # Backend Frameworks
    "node.js": ["node.js", "nodejs", "node js", "node"],
    "express.js": ["express.js", "expressjs", "express"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi", "fast api"],
    "spring boot": ["spring boot", "springboot", "spring"],
    "asp.net": ["asp.net", "dotnet", ".net", "asp net"],
    "ruby on rails": ["ruby on rails", "rails", "ror"],
    "laravel": ["laravel"],
    "nest.js": ["nest.js", "nestjs"],
    
    # Databases
    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres", "psql"],
    "mongodb": ["mongodb", "mongo"],
    "sqlite": ["sqlite"],
    "redis": ["redis"],
    "elasticsearch": ["elasticsearch", "elastic search"],
    "cassandra": ["cassandra"],
    "dynamodb": ["dynamodb", "dynamo db"],
    "firebase": ["firebase", "firestore"],
    "oracle db": ["oracle db", "oracle database", "oracle"],
    "mssql": ["mssql", "sql server", "microsoft sql server"],
    
    # Cloud & DevOps
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "google cloud": ["gcp", "google cloud", "google cloud platform"],
    "docker": ["docker", "containerization", "containers"],
    "kubernetes": ["kubernetes", "k8s"],
    "terraform": ["terraform", "iac"],
    "ansible": ["ansible"],
    "jenkins": ["jenkins"],
    "ci/cd": ["ci/cd", "ci cd", "continuous integration", "continuous deployment"],
    "nginx": ["nginx"],
    "apache": ["apache"],
    "linux": ["linux", "ubuntu", "centos", "debian", "redhat"],
    "heroku": ["heroku"],
    "vercel": ["vercel"],
    "netlify": ["netlify"],
    
    # Data Science & ML
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "tensorflow": ["tensorflow", "tf", "tensor flow"],
    "pytorch": ["pytorch"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "keras": ["keras"],
    "opencv": ["opencv", "cv2"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision"],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization"],
    "big data": ["big data"],
    "hadoop": ["hadoop"],
    "spark": ["spark", "pyspark", "apache spark"],
    "tableau": ["tableau"],
    "jupyter": ["jupyter", "jupyter notebook"],
    
    # Web Technologies
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "sass": ["sass", "scss"],
    "rest api": ["rest api", "rest apis", "restful", "restful api"],
    "graphql": ["graphql"],
    "websockets": ["websocket", "websockets"],
    "json": ["json"],
    "xml": ["xml"],
    "oauth": ["oauth", "oauth2"],
    
    # Mobile
    "android": ["android", "android development"],
    "ios": ["ios", "ios development"],
    "react native": ["react native"],
    "flutter": ["flutter"],
    "xamarin": ["xamarin"],
    
    # Version Control & Tools
    "git": ["git", "version control"],
    "github": ["github"],
    "gitlab": ["gitlab"],
    "bitbucket": ["bitbucket"],
    "jira": ["jira"],
    "postman": ["postman"],
    "swagger": ["swagger"],
    "figma": ["figma"],
    "vscode": ["vscode", "visual studio code"],
    
    # Testing
    "unit testing": ["unit testing", "unit test"],
    "selenium": ["selenium"],
    "jest": ["jest"],
    "pytest": ["pytest"],
    "cypress": ["cypress"],
    
    # Blockchain / Other
    "blockchain": ["blockchain"],
    "solidity": ["solidity"],
    "web3": ["web3"],
    "iot": ["iot", "internet of things"],
    "embedded systems": ["embedded systems", "embedded"],
    "microcontrollers": ["microcontrollers", "arduino", "raspberry pi"],
}

# ──────────────────────────────────────────────
# 2. Professional (Soft) Skills (30+ entries)
# ──────────────────────────────────────────────
PROFESSIONAL_SKILLS = {
    "leadership": ["leadership", "leading", "lead", "supervision", "supervisory"],
    "communication": ["communication", "verbal communication", "written communication", "interpersonal"],
    "teamwork": ["teamwork", "collaboration", "team player", "team work", "cooperative"],
    "problem solving": ["problem solving", "problem-solving", "troubleshooting", "analytical thinking"],
    "presentation": ["presentation", "public speaking", "presenting"],
    "project management": ["project management", "agile", "scrum", "kanban", "waterfall"],
    "time management": ["time management", "deadline management", "punctual"],
    "management": ["management", "people management", "team management"],
    "critical thinking": ["critical thinking", "logical reasoning", "decision making"],
    "creativity": ["creativity", "creative thinking", "innovative"],
    "adaptability": ["adaptability", "flexible", "adaptable"],
    "negotiation": ["negotiation", "negotiating"],
    "conflict resolution": ["conflict resolution", "dispute resolution"],
    "customer service": ["customer service", "customer support", "client relations"],
    "mentoring": ["mentoring", "coaching", "training others"],
    "attention to detail": ["attention to detail", "detail oriented", "meticulous"],
    "strategic planning": ["strategic planning", "strategic thinking"],
    "multitasking": ["multitasking", "multi-tasking"],
    "emotional intelligence": ["emotional intelligence", "empathy"],
    "networking": ["networking", "relationship building"],
    "writing": ["technical writing", "documentation", "content writing", "report writing"],
    "research": ["research", "research skills", "literature review"],
    "teaching": ["teaching", "tutoring", "instruction"],
    "sales": ["sales", "selling", "business development"],
    "organization": ["organization", "organizational skills", "organized"],
    "self motivation": ["self motivation", "self-motivated", "self motivated"],
    "work ethic": ["work ethic", "hard working", "dedicated"],
    "coordination": ["coordination", "coordinating"],
}

# ──────────────────────────────────────────────
# 3. Domain Skills (60+ entries)
# ──────────────────────────────────────────────
DOMAIN_SKILLS = {
    # Engineering
    "electrical engineering": ["electrical", "circuit design", "wiring", "electrical engineering", "power systems", "transformers"],
    "mechanical engineering": ["mechanical", "thermodynamics", "fluid mechanics", "mechanical engineering", "cad modeling"],
    "civil engineering": ["civil", "structural design", "construction", "civil engineering", "surveying"],
    "electronics": ["electronics", "pcb design", "vlsi", "signal processing"],
    "chemical engineering": ["chemical engineering", "process engineering"],
    
    # Manufacturing & Operations
    "manufacturing": ["manufacturing", "production", "assembly", "assembly line"],
    "industrial operations": ["industrial operations", "plant operations", "shift supervision", "plant management"],
    "quality control": ["quality control", "qa", "qc", "quality assurance", "iso", "six sigma", "lean manufacturing"],
    "supply chain": ["supply chain", "logistics", "inventory management", "procurement"],
    "safety management": ["safety management", "osha", "workplace safety", "ehs"],
    
    # Business & Finance
    "accounting": ["accounting", "bookkeeping", "taxation", "auditing", "tally", "gst"],
    "finance": ["finance", "financial analysis", "investment", "banking"],
    "marketing": ["marketing", "seo", "sem", "content marketing", "digital marketing", "social media marketing"],
    "human resources": ["human resources", "hr", "recruitment", "talent acquisition", "payroll"],
    "business analysis": ["business analysis", "business analyst", "requirements gathering"],
    "operations management": ["operations management", "operations"],
    "consulting": ["consulting", "management consulting"],
    
    # Office & Productivity
    "microsoft excel": ["microsoft excel", "ms excel", "excel", "spreadsheet", "vlookup", "pivot table"],
    "microsoft word": ["microsoft word", "ms word"],
    "microsoft powerpoint": ["powerpoint", "ms powerpoint", "ppt", "presentations"],
    "microsoft office": ["microsoft office", "ms office", "office suite"],
    "google workspace": ["google workspace", "google docs", "google sheets", "g suite"],
    "power bi": ["power bi", "powerbi"],
    "autocad": ["autocad", "cad", "auto cad"],
    "solidworks": ["solidworks", "solid works"],
    "matlab": ["matlab"],
    "labview": ["labview"],
    "sap": ["sap", "sap erp"],
    "erp": ["erp", "enterprise resource planning"],
    "crm": ["crm", "salesforce", "customer relationship management"],
    
    # Healthcare
    "healthcare": ["healthcare", "clinical", "patient care", "medical"],
    "nursing": ["nursing", "nurse", "rn"],
    "pharmacy": ["pharmacy", "pharmacist", "pharmaceutical"],
    
    # Design
    "graphic design": ["graphic design", "photoshop", "illustrator", "canva"],
    "ui/ux design": ["ui/ux", "ui design", "ux design", "user experience", "user interface"],
    "video editing": ["video editing", "premiere pro", "after effects", "davinci resolve"],
    
    # Other Technical
    "computer knowledge": ["computer knowledge", "basic computer skills", "computer proficiency", "computer literate"],
    "typing": ["typing", "typing speed", "wpm"],
    "data entry": ["data entry"],
    "networking (it)": ["networking", "tcp/ip", "lan", "wan", "cisco"],
    "cybersecurity": ["cybersecurity", "cyber security", "information security", "ethical hacking", "penetration testing"],
}


def _find_matches(text: str, skill_db: dict, category: str, source: str) -> List[SkillMatch]:
    """Find skill matches in the given text against a skill database."""
    matches = []
    text_lower = text.lower()
    
    for canonical, aliases in skill_db.items():
        for alias in aliases:
            pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
            if re.search(pattern, text_lower):
                confidence = 98 if alias == canonical else 90
                # Format name: Title case for long names, UPPER for abbreviations
                display_name = canonical.upper() if len(canonical) <= 3 and canonical.isalpha() else canonical.title()
                # Special casing
                special = {"sql": "SQL", "html": "HTML", "css": "CSS", "aws": "AWS", "gcp": "GCP",
                           "ci/cd": "CI/CD", "nlp": "NLP", "iot": "IoT", "erp": "ERP", "crm": "CRM",
                           "rest api": "REST API", "graphql": "GraphQL", "node.js": "Node.js",
                           "vue.js": "Vue.js", "next.js": "Next.js", "express.js": "Express.js",
                           "react native": "React Native", "ruby on rails": "Ruby on Rails",
                           "spring boot": "Spring Boot", "asp.net": "ASP.NET", "nest.js": "Nest.js",
                           "nuxt.js": "Nuxt.js", "scikit-learn": "Scikit-Learn", "opencv": "OpenCV",
                           "ui/ux design": "UI/UX Design", "microsoft excel": "Microsoft Excel",
                           "microsoft word": "Microsoft Word", "microsoft powerpoint": "Microsoft PowerPoint",
                           "microsoft office": "Microsoft Office", "power bi": "Power BI",
                           "google workspace": "Google Workspace", "c++": "C++", "c#": "C#",
                           "machine learning": "Machine Learning", "deep learning": "Deep Learning",
                           "artificial intelligence": "Artificial Intelligence",
                           "computer vision": "Computer Vision", "big data": "Big Data",
                           "react": "React", "angular": "Angular", "docker": "Docker",
                           "kubernetes": "Kubernetes", "tensorflow": "TensorFlow", "pytorch": "PyTorch",
                           "mongodb": "MongoDB", "postgresql": "PostgreSQL", "firebase": "Firebase",
                           "autocad": "AutoCAD", "solidworks": "SolidWorks", "matlab": "MATLAB",
                           "labview": "LabVIEW", "sap": "SAP",
                           }
                display_name = special.get(canonical, display_name)
                
                matches.append({
                    "skill": display_name,
                    "confidence": confidence,
                    "source": source,
                    "category": category
                })
                break
    return matches

def refine_skills(raw_skills_text: str, full_resume_text: str = "") -> dict:
    """
    Module 8: Skill Intelligence Engine
    Extracts and categorizes skills into Technical, Professional, and Domain.
    Normalizes aliases and returns categorized SkillMatch objects with confidence.
    """
    
    # 1. Extract from the skills section (higher confidence)
    tech = _find_matches(raw_skills_text, TECHNICAL_SKILLS, "Technical", "Skills Section")
    prof = _find_matches(raw_skills_text, PROFESSIONAL_SKILLS, "Professional", "Skills Section")
    dom = _find_matches(raw_skills_text, DOMAIN_SKILLS, "Domain", "Skills Section")
    
    # 2. Supplement from the full resume text (lower confidence)
    if full_resume_text:
        supp_tech = _find_matches(full_resume_text, TECHNICAL_SKILLS, "Technical", "Full Text")
        supp_prof = _find_matches(full_resume_text, PROFESSIONAL_SKILLS, "Professional", "Full Text")
        supp_dom = _find_matches(full_resume_text, DOMAIN_SKILLS, "Domain", "Full Text")
        
        tech = _merge_skills(tech, supp_tech)
        prof = _merge_skills(prof, supp_prof)
        dom = _merge_skills(dom, supp_dom)
    
    logger.info("Skills extracted: %d technical, %d professional, %d domain", len(tech), len(prof), len(dom))
        
    return {
        "technical": tech,
        "professional": prof,
        "domain": dom
    }

def _merge_skills(primary: List[SkillMatch], supplementary: List[SkillMatch]) -> List[SkillMatch]:
    """Merge skill lists, keeping primary (higher confidence) matches."""
    merged = {s["skill"]: s for s in primary}
    for s in supplementary:
        if s["skill"] not in merged:
            s["confidence"] = max(50, s["confidence"] - 15)
            merged[s["skill"]] = s
    return list(merged.values())
