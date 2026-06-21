import re
import logging
from typing import Any, Optional

logger = logging.getLogger("skillbridge.ai.extractor")

# ──────────────────────────────────────────────
# Regex patterns
# ──────────────────────────────────────────────

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s\-]?)?(?:\(?\d{2,5}\)?[\s\-]?)(?:[\d\s\-]{5,12}\d)")
GITHUB_RE = re.compile(r"(?:https?://)?(?:www\.)?github\.com/\s*([a-zA-Z0-9\-_]+)", re.IGNORECASE)
LINKEDIN_RE = re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/in/\s*([a-zA-Z0-9\-_]+)", re.IGNORECASE)
PORTFOLIO_RE = re.compile(r"(?:https?://)?(?:www\.)?(?:[a-zA-Z0-9\-_]+\.)+(?:com|me|dev|io|net|org)(?:/[a-zA-Z0-9\-_]+)*", re.IGNORECASE)
DOB_RE = re.compile(r"\b(?:DOB|Date of Birth|Birth Date|Born)\s*[:\-]?\s*(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\b", re.IGNORECASE)
CGPA_RE = re.compile(r"(?:CGPA|GPA|Percentage|Score|Marks)\s*[:\-]?\s*(\d{1,3}(?:\.\d{1,2})?(?:\s*%|/10|/100|/4)?)", re.IGNORECASE)
YEAR_RE = re.compile(r"\b(20\d{2})\b")

DEGREE_RE = re.compile(
    r"\b("
    r"B\.?\s*Tech|B\.?\s*E\.?|B\.?\s*Sc|B\.?\s*S\.?|B\.?\s*C\.?\s*A|"
    r"M\.?\s*Tech|M\.?\s*E\.?|M\.?\s*Sc|M\.?\s*S\.?|M\.?\s*C\.?\s*A|M\.?\s*B\.?\s*A|"
    r"Ph\.?\s*D|"
    r"Bachelor(?:'?s)?|Master(?:'?s)?|Diploma|"
    r"B\.?\s*Com|M\.?\s*Com|"
    r"B\.?\s*A\.?|M\.?\s*A\.?|I\.?\s*T\.?\s*I\.?|"
    r"12th|10th|High\s*School|Intermediate|Matriculation|Secondary\s*School|Senior\s*Secondary"
    r")\b",
    re.IGNORECASE,
)

BRANCH_RE = re.compile(
    r"\b("
    r"Computer\s*Science|Information\s*Technology|Electrical|Mechanical|Civil|"
    r"Electronics|Communication|Data\s*Science|Artificial\s*Intelligence|Machine\s*Learning|"
    r"Business\s*Administration|Commerce|Arts|Science|Physics|Chemistry|Mathematics|"
    r"Electrical\s*(?:and|&)\s*Electronics|Computer\s*Applications"
    r")\b",
    re.IGNORECASE
)

# ──────────────────────────────────────────────
# Extraction functions
# ──────────────────────────────────────────────

def clean_value(val: Optional[str]) -> Optional[str]:
    if not val:
        return None
    val = val.strip()
    while True:
        prev_len = len(val)
        val = re.sub(r"^[•▪►■◆❖➢⮚✓✔\-\*▪\+\.．\s]+", "", val).strip()
        if len(val) == prev_len:
            break
    val = re.sub(r"[:\-—,\s]+$", "", val).strip()
    if val.endswith(".") and not val.endswith("Ltd.") and not val.endswith("Inc."):
        if not re.search(r"\b[A-Za-z]\.$", val):
            val = val[:-1].strip()
    return val if val else None

def _extract_name(header_text: str, full_text: str) -> Optional[str]:
    source = header_text if header_text else full_text
    excluded = {
        "resume", "cv", "curriculum vitae", "biodata", "portfolio", 
        "contact", "profile", "summary", "email", "phone", "address",
        "page", "personal"
    }
    for line in source.split("\n"):
        line = line.strip()
        if not line: continue
        if EMAIL_RE.search(line): continue
        if PHONE_RE.search(line): continue
        if re.search(r"https?://|www\.|github|linkedin|@", line, re.IGNORECASE): continue
        if re.search(r"^\d+\s", line): continue # Address
        if line.lower() in excluded or any(kw in line.lower() for kw in excluded): continue
        if not re.search(r"[a-zA-Z]", line): continue
        
        # Name should be short, 1-4 words, Title Cased or UPPERCASED
        words = line.split()
        if 1 <= len(words) <= 4 and len(line) < 40:
            name = re.sub(r"[^\w\s.\-']", "", line).strip()
            return clean_value(name)
    return None

def _extract_email(text: str) -> Optional[str]:
    match = EMAIL_RE.search(text)
    return clean_value(match.group(0)) if match else None

def _extract_phone(text: str) -> Optional[str]:
    matches = PHONE_RE.findall(text)
    for m in matches:
        digits = re.sub(r"\D", "", m)
        if 7 <= len(digits) <= 15:
            return clean_value(m)
    return None

def _extract_github(text: str) -> Optional[str]:
    match = GITHUB_RE.search(text)
    return f"https://github.com/{clean_value(match.group(1))}" if match else None

def _extract_linkedin(text: str) -> Optional[str]:
    match = LINKEDIN_RE.search(text)
    return f"https://linkedin.com/in/{clean_value(match.group(1))}" if match else None

def _extract_portfolio(text: str) -> Optional[str]:
    # Exclude standard ones
    for match in PORTFOLIO_RE.finditer(text):
        url = match.group(0).lower()
        if "github.com" not in url and "linkedin.com" not in url:
            return clean_value(match.group(0))
    return None

def _extract_dob(text: str) -> Optional[str]:
    match = DOB_RE.search(text)
    return clean_value(match.group(1)) if match else None

def _extract_address(header_text: str) -> Optional[str]:
    # Very basic address heuristic: line starts with digits or contains street/city keywords
    address_kws = ["street", "st", "avenue", "ave", "road", "rd", "block", "nagar", "colony", "apartment", "apt", "city"]
    for line in header_text.split("\n"):
        line = line.strip().lower()
        if any(kw in line for kw in address_kws) and not EMAIL_RE.search(line):
            return clean_value(line.title())
    return None

def parse_education_block(block: str) -> dict[str, Optional[str]]:
    year = ""
    year_match = re.search(r"\b(20\d{2}\s*[-–]\s*(?:20\d{2}|present|date)|\b20\d{2}\b)", block, re.IGNORECASE)
    if year_match:
        year = year_match.group(0)
    
    cgpa = ""
    cgpa_match = CGPA_RE.search(block)
    if cgpa_match:
        cgpa = cgpa_match.group(1)
        
    degree = ""
    deg_match = DEGREE_RE.search(block)
    if deg_match:
        degree = deg_match.group(0)
        
    branch = ""
    branch_match = BRANCH_RE.search(block)
    if branch_match:
        branch = branch_match.group(0)
        
    # Institution is the rest of the text that looks like a name
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    institution = None
    for l in lines:
        if ("university" in l.lower() or "college" in l.lower() or "institute" in l.lower() or "school" in l.lower() or "academy" in l.lower()):
            institution = l
            break
            
    if not institution and lines:
        # Fallback to the first line if it's long enough and doesn't contain degree/year
        first = lines[0]
        if len(first) > 5 and not DEGREE_RE.search(first) and not YEAR_RE.search(first):
            institution = first

    # For 12th/10th, the board is often mentioned instead of university
    if not institution and ("12th" in degree or "10th" in degree):
        for l in lines:
            if "board" in l.lower() or "cbse" in l.lower() or "icse" in l.lower():
                institution = l
                break

    return {
        "institution": clean_value(institution),
        "degree": clean_value(degree),
        "branch": clean_value(branch),
        "year": clean_value(year),
        "cgpa": clean_value(cgpa)
    }

def _extract_education(education_text: str) -> list[dict]:
    if not education_text: return []
    # Split by double newlines or bullets that start a new entry
    blocks = re.split(r"\n\s*\n|(?=\n[•▪►\-\*]\s)", education_text)
    entries = []
    for block in blocks:
        if not block.strip(): continue
        parsed = parse_education_block(block)
        if parsed["degree"] or parsed["institution"]:
            entries.append(parsed)
    return entries

def parse_experience_block(block: str) -> dict:
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    date_range = ""
    company = None
    role = None
    
    # Extract date
    date_re = re.compile(r"\b((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\s*\d{0,4}\s*(?:to|-|–)\s*(?:\d{4}|present|till date|current|now))\b", re.IGNORECASE)
    
    for line in lines:
        d_match = date_re.search(line)
        if d_match and not date_range:
            date_range = d_match.group(1)
            
        # Role heuristic
        if ("engineer" in line.lower() or "developer" in line.lower() or "manager" in line.lower() or "intern" in line.lower() or "analyst" in line.lower()):
            if not role and len(line) < 60:
                role = clean_value(line.replace(date_range, ""))
                
        # Company heuristic
        if any(s in line.lower() for s in ["pvt", "ltd", "corp", "inc", "co.", "technologies", "services"]):
            if not company and len(line) < 60:
                company = clean_value(line.replace(date_range, ""))

    if not company and lines:
        company = clean_value(lines[0])
    
    return {
        "company": company,
        "role": role,
        "duration": clean_value(date_range),
        "current_company": "present" in date_range.lower() or "now" in date_range.lower() or "current" in date_range.lower()
    }

def _extract_experience(experience_text: str) -> list[dict]:
    if not experience_text: return []
    blocks = re.split(r"\n\s*\n|(?=\n[•▪►\-\*]\s)", experience_text)
    entries = []
    for block in blocks:
        if not block.strip(): continue
        # Only process block if it has a date or company identifier
        if re.search(r"20\d{2}", block) or any(s in block.lower() for s in ["ltd", "inc", "corp", "intern", "developer"]):
            parsed = parse_experience_block(block)
            if parsed["company"] or parsed["role"]:
                entries.append(parsed)
    return entries

def _extract_projects(projects_text: str) -> list[dict]:
    if not projects_text: return []
    blocks = re.split(r"\n\s*\n", projects_text)
    entries = []
    for block in blocks:
        if not block.strip(): continue
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        title = lines[0] if len(lines[0]) < 60 else None
        
        tech_match = re.search(r"(?:tech(?:nolog(?:y|ies))?|stack|tools?|built\s*with)\s*[:\-]\s*(.+)", block, re.IGNORECASE)
        techs = clean_value(tech_match.group(1)) if tech_match else None
        
        if not techs:
            # Look for common tech
            found_techs = re.findall(r"\b(React|Node|Python|Java|SQL|MongoDB|Express|Firebase|AWS|Docker|Git|C\+\+)\b", block, re.IGNORECASE)
            if found_techs:
                techs = ", ".join(list(set(found_techs)))
                
        if title:
            entries.append({
                "title": clean_value(title.replace("Project", "").replace(":", "")),
                "technologies": techs
            })
    return entries

def extract_information(sections: dict[str, str], full_text: str) -> dict[str, Any]:
    header = sections.get("header", "")
    personal = sections.get("personal", "")
    combined_info = header + "\n" + personal

    result: dict[str, Any] = {
        "name": _extract_name(header, full_text),
        "email": _extract_email(full_text),
        "phone": _extract_phone(combined_info if combined_info else full_text),
        "address": _extract_address(combined_info),
        "dob": _extract_dob(combined_info),
        "github": _extract_github(full_text),
        "linkedin": _extract_linkedin(full_text),
        "portfolio": _extract_portfolio(full_text),
        "education": _extract_education(sections.get("education", "")),
        "projects": _extract_projects(sections.get("projects", "")),
        "experience": _extract_experience(sections.get("experience", "")),
        "raw_skills": sections.get("skills", ""), # Send raw text to the skill_extractor
        "summary_text": sections.get("summary", ""),
    }

    # Calculate Confidence
    fields = [result["name"], result["email"], result["phone"]]
    extracted_count = sum(1 for f in fields if f is not None)
    
    if result["education"]: extracted_count += 1
    if result["experience"]: extracted_count += 1
    if result["raw_skills"]: extracted_count += 1
    
    result["parsing_confidence"] = int((extracted_count / 6) * 100)
    
    logger.info(
        "ATS Extracted: name=%s, email=%s, confidence=%d%%",
        result["name"], result["email"], result["parsing_confidence"]
    )

    return result
