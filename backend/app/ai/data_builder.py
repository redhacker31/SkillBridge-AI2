import json
import os

ROLES = [
    ("Frontend Developer (React)", ["html", "css", "javascript", "react"], ["typescript", "redux", "next.js"], "frontend_developer_react"),
    ("Backend Developer (Python)", ["python", "sql", "django", "flask"], ["fastapi", "docker", "redis", "postgresql"], "backend_developer_python"),
    ("Data Scientist", ["python", "sql", "machine learning", "pandas"], ["scikit-learn", "numpy", "tensorflow", "pytorch"], "data_scientist"),
    ("DevOps Engineer", ["linux", "docker", "kubernetes", "git"], ["aws", "terraform", "jenkins", "prometheus"], "devops_engineer"),
    ("Full Stack Developer", ["javascript", "react", "node.js", "sql"], ["typescript", "postgresql", "docker", "aws"], "fullstack_developer"),
    ("Machine Learning Engineer", ["python", "machine learning", "tensorflow", "pytorch"], ["sql", "docker", "kubernetes", "aws"], "machine_learning_engineer"),
    ("iOS Developer", ["swift", "xcode", "git"], ["objective-c", "core data", "uikit"], "ios_developer"),
    ("Android Developer", ["java", "kotlin", "android studio"], ["git", "sqlite", "firebase"], "android_developer"),
    ("UI/UX Designer", ["figma", "wireframing", "prototyping"], ["adobe xd", "sketch", "html", "css"], "ui_ux_designer"),
    ("Cloud Architect (AWS)", ["aws", "linux", "networking", "security"], ["terraform", "docker", "kubernetes", "python"], "cloud_architect_aws"),
    ("Cybersecurity Analyst", ["networking", "security", "linux", "wireshark"], ["python", "bash", "penetration testing"], "cybersecurity_analyst"),
    ("Data Analyst", ["excel", "sql", "tableau", "power bi"], ["python", "pandas", "statistics"], "data_analyst"),
    ("Database Administrator", ["sql", "postgresql", "mysql", "oracle"], ["linux", "backup/recovery", "performance tuning"], "database_administrator"),
    ("Blockchain Developer", ["solidity", "smart contracts", "ethereum", "javascript"], ["rust", "go", "cryptography"], "blockchain_developer"),
    ("Game Developer (Unity)", ["c#", "unity", "game design"], ["c++", "3d modeling", "git"], "game_developer_unity"),
    ("Game Developer (Unreal)", ["c++", "unreal engine", "blueprints"], ["c#", "3d modeling", "git"], "game_developer_unreal"),
    ("Site Reliability Engineer", ["linux", "python", "go", "docker"], ["kubernetes", "aws", "terraform", "monitoring"], "site_reliability_engineer"),
    ("Product Manager", ["agile", "scrum", "product strategy", "jira"], ["data analysis", "sql", "ux design"], "product_manager"),
    ("Quality Assurance Engineer", ["selenium", "testing", "python", "java"], ["cypress", "jenkins", "git"], "quality_assurance_engineer"),
    ("Data Engineer", ["python", "sql", "apache spark", "hadoop"], ["kafka", "aws", "airflow"], "data_engineer"),
    ("Cloud Engineer (Azure)", ["azure", "linux", "networking", "powershell"], ["docker", "kubernetes", "terraform"], "cloud_engineer_azure"),
    ("Cloud Engineer (GCP)", ["gcp", "linux", "networking", "python"], ["docker", "kubernetes", "terraform"], "cloud_engineer_gcp"),
    ("Frontend Developer (Angular)", ["html", "css", "javascript", "angular"], ["typescript", "rxjs", "ngrx"], "frontend_developer_angular"),
    ("Frontend Developer (Vue)", ["html", "css", "javascript", "vue"], ["vuex", "nuxt.js", "sass"], "frontend_developer_vue"),
    ("Backend Developer (Java)", ["java", "spring boot", "sql", "git"], ["hibernate", "maven", "docker"], "backend_developer_java"),
    ("Backend Developer (Go)", ["go", "sql", "linux", "git"], ["docker", "kubernetes", "gRPC"], "backend_developer_go"),
    ("Backend Developer (Node.js)", ["javascript", "node.js", "sql", "git"], ["typescript", "express", "mongodb"], "backend_developer_node"),
    ("Backend Developer (C# .NET)", ["c#", ".net", "sql server", "git"], ["azure", "entity framework", "docker"], "backend_developer_csharp"),
    ("Embedded Systems Engineer", ["c", "c++", "microcontrollers", "rtos"], ["python", "linux", "hardware design"], "embedded_systems_engineer"),
    ("AR/VR Developer", ["c#", "unity", "arcore", "arkit"], ["c++", "unreal engine", "3d math"], "ar_vr_developer"),
    ("Big Data Engineer", ["java", "scala", "hadoop", "spark"], ["python", "kafka", "nosql"], "big_data_engineer"),
    ("Computer Vision Engineer", ["python", "opencv", "machine learning", "deep learning"], ["c++", "tensorflow", "pytorch"], "computer_vision_engineer"),
    ("NLP Engineer", ["python", "nlp", "machine learning", "pytorch"], ["tensorflow", "transformers", "spacy"], "nlp_engineer"),
    ("Robotics Engineer", ["c++", "python", "ros", "linux"], ["machine learning", "control systems", "computer vision"], "robotics_engineer"),
    ("Business Intelligence Analyst", ["sql", "power bi", "tableau", "excel"], ["python", "data warehousing", "etl"], "bi_analyst"),
    ("IT Support Specialist", ["troubleshooting", "windows", "networking", "customer service"], ["linux", "active directory", "mac os"], "it_support_specialist"),
]

def generate_careers():
    careers_db = {}
    for name, core, secondary, key in ROLES:
        required_skills = {}
        for skill in core:
            required_skills[skill] = "Critical"
            
        optional_skills = []
        for skill in secondary:
            required_skills[skill] = "High" if len(required_skills) < 6 else "Medium"
            optional_skills.append(skill)
            
        # Generate specific courses
        courses = [
            {
                "title": f"Mastering {core[0].title()} for {name.split('(')[0].strip()}",
                "reason": f"Essential foundation in {core[0]}",
                "difficulty": "Beginner",
                "estimated_time": "4 weeks",
                "prerequisites": [],
                "addressed_skills": [core[0]]
            },
            {
                "title": f"Advanced {core[-1].title()} Architecture",
                "reason": f"Deep dive into {core[-1]} patterns",
                "difficulty": "Advanced",
                "estimated_time": "6 weeks",
                "prerequisites": [core[0]],
                "addressed_skills": [core[-1]]
            }
        ]
        
        # Generate specific projects
        projects = [
            {
                "title": f"Build a {name.split('(')[0].strip()} Portfolio Project",
                "reason": "Hands-on experience with core tools",
                "difficulty": "Intermediate",
                "estimated_time": "3 weeks",
                "prerequisites": [core[0], core[1]],
                "addressed_skills": [core[0], core[1]]
            },
            {
                "title": f"Enterprise-level {core[2].title()} Application",
                "reason": "Demonstrate production readiness",
                "difficulty": "Advanced",
                "estimated_time": "8 weeks",
                "prerequisites": core,
                "addressed_skills": core[2:]
            }
        ]
        
        if secondary:
            projects.append({
                "title": f"Integrating {secondary[0].title()} into {core[0].title()}",
                "reason": f"Shows ability to use {secondary[0]} effectively",
                "difficulty": "Intermediate",
                "estimated_time": "2 weeks",
                "prerequisites": [core[0]],
                "addressed_skills": [secondary[0]]
            })

        # Generate specific internships
        internships = [
            {
                "title": f"Junior {name} Intern",
                "reason": "Gain real-world experience",
                "difficulty": "Beginner",
                "estimated_time": "3 months",
                "prerequisites": core[:2],
                "addressed_skills": core
            }
        ]
        
        careers_db[key] = {
            "id": f"CAR_{key.upper()}",
            "name": name,
            "required_skills": required_skills,
            "optional_skills": optional_skills,
            "courses": courses,
            "projects": projects,
            "internships": internships,
            "roadmap": [f"Learn {s}" for s in core] + [f"Explore {s}" for s in secondary],
            "certifications": [f"Certified {name} Professional"]
        }
    return careers_db


if __name__ == "__main__":
    careers_db = generate_careers()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
        
    with open(os.path.join(data_dir, "careers.json"), "w") as f:
        json.dump(careers_db, f, indent=2)
        
    print(f"Generated {len(careers_db)} careers.")
