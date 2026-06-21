export interface AnalysisRequest {
  career_goal: string;
}

export interface Recommendation {
  title: string;
  reason: string;
  difficulty: string;
  estimated_time: string;
  prerequisites: string[];
  addressed_skills: string[];
}

export interface MissingSkill {
  skill: string;
  priority: string;
  reason?: string;
}

export interface PersonalInfo {
  name: string;
  email: string;
  phone: string;
  github: string;
  linkedin: string;
  college: string;
  degree: string;
  graduation_year: string;
}

export interface ScoreBreakdown {
  category: string;
  score: number;
  max_score: number;
  deduction_reason: string;
}

export interface AtsBreakdown {
  metric: string;
  passed: boolean;
  details: string;
}

export interface SkillCategories {
  core: string[];
  preferred: string[];
  bonus: string[];
  unrelated: string[];
}

export interface ProjectAnalysis {
  name: string;
  technologies: string;
  complexity: string;
  relevant_roles: string[];
  evaluation: string;
  suggestions: string[];
}

export interface ExperienceAnalysis {
  duration: string;
  role: string;
  company: string;
  evaluation: string;
}

export interface CareerReadiness {
  career: string;
  match_percentage: number;
}

export interface VisualRoadmapStep {
  step_number: number;
  title: string;
  estimated_duration: string;
  resource: string;
  mini_project: string;
}

export interface InterviewProbability {
  company: string;
  probability: number;
  reason: string;
}

export interface InterviewReadiness {
  overall: number;
  technical_readiness: number;
  project_readiness: number;
  resume_readiness: number;
  reason: string;
}

export interface ResumeCompleteness {
  score: number;
  breakdown: Record<string, boolean>;
}

export interface AnalysisResponse {
  personal_info: PersonalInfo;
  resume_summary: string;
  domain: string;

  resume_score: number;
  resume_score_breakdown: ScoreBreakdown[];

  ats_score: number;
  ats_score_breakdown: AtsBreakdown[];
  ats_suggestions: string[];

  skill_categories: SkillCategories;
  skill_coverage_percentage: number;
  total_required_skills: number;
  skills_found_count: number;
  skills_missing_count: number;

  present_skills: string[];
  missing_skills: MissingSkill[];

  strengths: string[];
  weaknesses: string[];

  project_analysis: ProjectAnalysis[];
  experience_analysis: ExperienceAnalysis[];

  career_readiness: CareerReadiness[];
  interview_readiness: InterviewReadiness;
  interview_probability: InterviewProbability[];

  visual_roadmap: VisualRoadmapStep[];

  roadmap: string[];
  certifications: string[];
  courses: Recommendation[];
  projects: Recommendation[];
  internships: Recommendation[];
  
  resume_completeness: ResumeCompleteness;
  debug_info: any;
}
