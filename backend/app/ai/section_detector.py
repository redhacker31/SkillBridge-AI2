import re
import logging

logger = logging.getLogger("skillbridge.ai.section_detector")

# Extensive ATS-style resume section headings
SECTION_HEADINGS = [
    ("education", [
        r"education",
        r"academic\s*qualifications?",
        r"qualifications?",
        r"academic\s*background",
        r"academic\s*record",
    ]),
    ("experience", [
        r"experience",
        r"employment",
        r"work\s*experience",
        r"professional\s*experience",
        r"work\s*history",
        r"employment\s*history",
        r"professional\s*background",
        r"career\s*history",
    ]),
    ("projects", [
        r"projects",
        r"personal\s*projects",
        r"academic\s*projects",
        r"key\s*projects",
        r"internships?", # User requested internships under projects or as a distinct section
    ]),
    ("internships", [
        r"internships?",
    ]),
    ("skills", [
        r"skills",
        r"technical\s*skills",
        r"summary\s*of\s*skills",
        r"key\s*skills",
        r"professional\s*skills",
        r"core\s*skills",
        r"technical\s*expertise",
        r"areas?\s*of\s*expertise",
        r"core\s*competencies",
        r"technologies",
        r"tools?\s*(?:&|and)?\s*technologies",
        r"programming\s*languages",
        r"computer\s*knowledge",
    ]),
    ("certifications", [
        r"certificates?",
        r"certifications?",
        r"licenses?\s*(?:&|and)?\s*certifications?",
        r"professional\s*certifications?",
    ]),
    ("achievements", [
        r"achievements?",
        r"awards?",
        r"honors?",
        r"accomplishments?",
        r"extra\s*curricular",
        r"activities",
    ]),
    ("summary", [
        r"summary",
        r"profile",
        r"career\s*objective",
        r"objective",
        r"about\s*me",
        r"professional\s*summary",
    ]),
    ("personal", [
        r"personal\s*details?",
        r"personal\s*profile",
        r"personal\s*information",
        r"declaration",
        r"languages",
        r"interests",
        r"hobbies",
        r"references?",
    ]),
]

def _build_heading_pattern() -> re.Pattern:
    all_patterns: list[str] = []
    for _section_name, patterns in SECTION_HEADINGS:
        all_patterns.extend(patterns)

    combined = "|".join(all_patterns)
    # Match at start of line, allowing bullets/numbers, and requiring it to be alone on the line
    return re.compile(
        rf"^\s*(?:[\-•*#\d.)\]]*\s*)?({combined})(?:\s*\(.*?\))?\s*[:\-—]*\s*$",
        re.IGNORECASE | re.MULTILINE,
    )

HEADING_RE = _build_heading_pattern()

def _classify_heading(heading_text: str) -> str:
    heading_lower = heading_text.strip().lower()
    for section_name, patterns in SECTION_HEADINGS:
        for p in patterns:
            if re.fullmatch(p, heading_lower, re.IGNORECASE):
                # Map internships into projects section for simplicity if desired, or keep separate.
                # The prompt listed "Internships" next to Projects. We'll map it to 'experience' or 'projects'.
                # Let's map it to 'experience' as it's professional work, but projects is fine too.
                # Actually let's keep it as its own section and let information_extractor decide.
                if section_name == "internships":
                    return "experience"
                return section_name
    return "other"

def detect_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    matches = list(HEADING_RE.finditer(text))

    if not matches:
        logger.warning("No section headings detected in resume text.")
        sections["header"] = text
        return sections

    header_text = text[: matches[0].start()].strip()
    if header_text:
        sections["header"] = header_text

    for i, match in enumerate(matches):
        section_name = _classify_heading(match.group(1))
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section_text = text[start:end].strip()

        if section_name in sections:
            sections[section_name] += "\n" + section_text
        else:
            sections[section_name] = section_text

    logger.info("Detected %d sections: %s", len(sections), list(sections.keys()))
    return sections
