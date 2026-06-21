import sys
import json
import logging
from pathlib import Path

# Setup simple logging
logging.basicConfig(level=logging.INFO)

# Assuming backend directory is in path
sys.path.append(str(Path(__file__).parent))

from app.ai.resume_parser import extract_text
from app.ai.section_detector import detect_sections
from app.ai.information_extractor import extract_information
from app.ai.analyzer import analyze_resume

def main():
    # Find a sample resume
    uploads_dir = Path(__file__).parent / "uploads"
    if not uploads_dir.exists():
        print("No uploads directory found.")
        return
        
    pdfs = list(uploads_dir.glob("*.pdf"))
    if not pdfs:
        print("No PDF files found in uploads directory.")
        return
        
    sample_pdf = pdfs[0]
    print(f"Testing Analysis with: {sample_pdf.name}")
    
    print("1. Parsing Text...")
    raw_text = extract_text(str(sample_pdf))
    
    print("2. Detecting Sections...")
    sections = detect_sections(raw_text)
    
    print("3. Extracting Information...")
    parsed_data = extract_information(sections, raw_text)
    
    career_goal = "AI Engineer"
    print(f"\n4. Running Analysis against goal: {career_goal}...")
    
    try:
        analysis_result = analyze_resume(parsed_data, raw_text, career_goal)
        print("\n--- ANALYSIS RESULT ---")
        print(json.dumps(analysis_result, indent=2))
        print("-----------------------\n")
        print("[SUCCESS] Analysis pipeline completed successfully.")
    except Exception as e:
        print(f"[ERROR] Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
