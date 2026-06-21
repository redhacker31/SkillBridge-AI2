SkillBridge AI – Portfolio Edition

Master Prompt v3.0

AI Career Mentor & Resume Intelligence Platform



ROLE

You are an expert Full-Stack Software Engineer, AI Engineer, UI/UX Designer, and Technical Architect.

Your job is to build a working, polished portfolio project, not an enterprise SaaS product.

The final application should be:

Fully functional

Easy to understand

Easy to demonstrate

Suitable for hackathons

Suitable for internship interviews

Suitable for placement interviews

Production-quality in code structure

Simple enough to complete within 4–8 weeks

Never over-engineer the solution.

Always choose the simplest architecture that satisfies the requirements.



PROJECT OVERVIEW

SkillBridge AI is an AI-powered web application that helps students understand how well their resume matches a chosen career path.

The application should allow users to:

Upload a resume (PDF).

Select a career goal.

Analyze the resume.

Detect existing skills.

Identify missing skills.

Calculate Resume Score.

Calculate ATS Score.

Generate a personalized learning roadmap.

Recommend projects.

Recommend courses.

Recommend internships.

Display everything in a clean dashboard.

The application should feel like a real product while remaining simple enough for a single developer to build.



PRIMARY GOAL

The objective is not to build the biggest AI platform.

The objective is to build a complete, polished, and deployable AI application that demonstrates:

Python programming

NLP

Machine Learning fundamentals

FastAPI backend

React frontend

Database design

REST APIs

Resume parsing

Recommendation systems



TARGET USERS

Primary users:

B.Tech Students

CSE Students

AI & ML Students

Data Science Students

Fresh Graduates

These users want to understand:

What skills they already have

What skills they are missing

Which projects to build

Which internships to apply for

Which courses to learn next



CORE FEATURES

The application will include only these major features.

Authentication

Register

Login

Logout



Resume Module

Upload Resume

Store Resume

Parse Resume



AI Analysis

Resume Score

ATS Score

Skill Extraction

Skill Gap Detection



Recommendations

Learning Roadmap

Courses

Projects

Internships



Dashboard

Display:

Resume Score

ATS Score

Existing Skills

Missing Skills

Recommended Courses

Recommended Projects

Recommended Internships

Personalized Roadmap



FEATURES NOT INCLUDED

Do not implement:

Payments

Subscription plans

Email verification

OAuth login

Admin dashboard

Notifications

Chatbot

AI agents

Redis

Microservices

Kubernetes

Background workers

Multi-tenancy

Enterprise analytics

These can be future improvements but are not part of Version 1.



TECHNOLOGY STACK

Frontend

React

TypeScript

Vite

Tailwind CSS

React Router

Axios

Backend

Python 3.12+

FastAPI

SQLAlchemy

Pydantic

Database

SQLite (default)

PostgreSQL (optional)

AI & NLP

PyMuPDF

spaCy

scikit-learn

Sentence Transformers

pandas

NumPy

Deployment

Frontend:

Vercel

Backend:

Render



PROJECT STRUCTURE

SkillBridge-AI/

backend/

frontend/

database/

docs/

tests/

README.md

Keep the folder structure simple and modular.



DEVELOPMENT PRINCIPLES

Always:

Write clean code.

Follow SOLID principles where practical.

Avoid unnecessary complexity.

Separate frontend, backend, AI, and database concerns.

Build one feature at a time.

Keep the application runnable after every phase.

Write code that is easy for a student to understand.



SUCCESS CRITERIA

The project is considered successful when a user can:

Register and log in.

Upload a PDF resume.

Receive AI-powered resume analysis.

View Resume Score.

View ATS Score.

See detected skills.

Understand missing skills.

Receive a personalized roadmap.

Receive project recommendations.

Receive course recommendations.

Receive internship recommendations.

View everything in a modern dashboard.

Run the application locally and deploy it successfully.



GENERAL RULES FOR THE AI CODING AGENT

Build only the requested phase.

Never generate the entire application at once.

Do not invent extra features.

Prefer clarity over cleverness.

Use reusable components and services.

Keep APIs RESTful.

Validate all user inputs.

Handle errors gracefully.

Ensure the application builds successfully before moving to the next phase.

At the end of every phase, summarize what was created and what remains.

This document serves as the master instruction set for the entire SkillBridge AI Portfolio Edition project.

SkillBridge AI – Portfolio Edition

PART 2 — SYSTEM ARCHITECTURE & PROJECT STRUCTURE



ROLE

Continue building SkillBridge AI following the instructions from Part 1.

This part defines the complete architecture that must be followed throughout the project.

Do not change the folder structure unless absolutely necessary.

The architecture should be simple, modular, and easy to maintain.



ARCHITECTURE OVERVIEW

The project consists of four major layers.

                    User

                      │

                      ▼

              React Frontend

                      │

              REST API (Axios)

                      │

                      ▼

            FastAPI Backend

                      │

        ┌─────────────┼─────────────┐

        │             │             │

        ▼             ▼             ▼

   AI Engine      Business Logic   Database

        │

        ▼

 Resume Analysis & Recommendations



PROJECT STRUCTURE

SkillBridge-AI/

│

├── backend/

│

├── frontend/

│

├── database/

│

├── docs/

│

├── tests/

│

├── README.md

│

├── .gitignore

│

└── docker-compose.yml

Only these top-level folders should exist in Version 1.



BACKEND STRUCTURE

backend/



app/



main.py



config.py



database.py



models/



schemas/



routers/



services/



ai/



utils/



requirements.txt



BACKEND RESPONSIBILITIES

main.py

Start FastAPI

Register routes

Configure middleware

Enable CORS



config.py

Store:

Database URL

Secret Key

Upload Folder

AI Configuration

Never hardcode configuration values.



database.py

Responsible for:

Database connection

Session creation

ORM configuration



models/

Contains database models only.

Example:

User

Resume

AnalysisReport

Models should never contain business logic.



schemas/

Contains Pydantic request and response models.

Examples:

UserCreate

LoginRequest

ResumeResponse

AnalysisResponse



routers/

Each router handles one feature.

Example:

auth.py



resume.py



analysis.py



dashboard.py

Routers should only:

Receive requests

Validate input

Call services

Return responses



services/

Business logic belongs here.

Examples:

auth_service.py



resume_service.py



analysis_service.py



dashboard_service.py



ai/

Contains all AI-related modules.

resume_parser.py



skill_extractor.py



resume_scorer.py



ats_scorer.py



roadmap_generator.py



recommendation_engine.py

These modules must remain independent of FastAPI.



utils/

Contains reusable helper functions.

Examples:

File utilities

Date utilities

PDF helpers

Validation helpers



FRONTEND STRUCTURE

frontend/



src/



components/



pages/



layouts/



services/



hooks/



types/



utils/



assets/



App.tsx



main.tsx



FRONTEND RESPONSIBILITIES

components/

Reusable UI elements.

Examples:

Button

Card

ProgressBar

ScoreCard

SkillCard

Navbar



pages/

One page per screen.

Examples:

Login

Register

Dashboard

ResumeUpload

Analysis

Roadmap



layouts/

Common page layouts.

Examples:

MainLayout

AuthLayout



services/

API communication.

Example:

auth.ts



resume.ts



analysis.ts

All HTTP requests should be centralized here.



hooks/

Reusable React hooks.

Examples:

useAuth

useResume

useDashboard



types/

Shared TypeScript interfaces.

Example:

User



Resume



Skill



AnalysisReport



utils/

Formatting and helper functions.

Examples:

Date formatting

Score formatting

Validation helpers



DATABASE STRUCTURE

Only three tables are required in Version 1.

Users

Stores user accounts.



Resumes

Stores uploaded resumes.



AnalysisReports

Stores AI analysis results.

Avoid creating unnecessary tables until new features require them.



MODULE DEPENDENCY GRAPH

Authentication



↓



Resume Upload



↓



Resume Parser



↓



Skill Extraction



↓



Resume Score



↓



ATS Score



↓



Skill Gap



↓



Roadmap



↓



Recommendations



↓



Dashboard

A module should only be implemented after its dependencies are complete.



AI MODULE FLOW

Resume PDF



↓



Text Extraction



↓



Section Detection



↓



Skill Extraction



↓



Resume Score



↓



ATS Score



↓



Skill Gap



↓



Roadmap



↓



Recommendations



↓



Dashboard

Each AI module should have a single responsibility.



API FLOW

Frontend



↓



Axios



↓



FastAPI Router



↓



Service



↓



AI Module / Database



↓



Response



↓



Frontend

Business logic should never be placed inside route handlers.



FILE UPLOAD FLOW

Upload Resume



↓



Validate PDF



↓



Store File



↓



Extract Text



↓



Run AI Analysis



↓



Save Report



↓



Return Dashboard Data



CODING PRINCIPLES

Every module should:

Have one responsibility.

Be reusable.

Be independently testable.

Avoid duplicate code.

Be easy to understand.



BUILD ORDER

The project must be developed in this sequence.

Phase 1

Project Setup



Phase 2

Authentication



Phase 3

Resume Upload



Phase 4

Resume Parser



Phase 5

Skill Extraction



Phase 6

Resume Score

ATS Score



Phase 7

Skill Gap Detection



Phase 8

Roadmap Generator



Phase 9

Recommendation Engine



Phase 10

Dashboard



Phase 11

Testing



Phase 12

Deployment

Never skip phases.



DEFINITION OF DONE

A phase is complete only if:

✓ Code builds successfully.

✓ No runtime errors.

✓ APIs work correctly.

✓ UI renders correctly.

✓ Database operations succeed.

✓ Basic tests pass.

✓ Code is documented.

✓ Feature integrates with previous phases.



END OF PART 2

At the completion of this section, the AI coding agent understands the complete project structure, module responsibilities, dependency graph, data flow, and implementation order.

This architecture must remain the foundation for all future development unless explicitly revised.

SkillBridge AI – Portfolio Edition

PART 3 — DATABASE DESIGN & BACKEND FOUNDATION



ROLE

Continue building SkillBridge AI following Parts 1 and 2.

This section defines the complete backend foundation.

The backend should remain simple, modular, and easy to understand.

Do not introduce unnecessary enterprise patterns.

The backend must expose REST APIs for the frontend and AI modules.



BACKEND OBJECTIVES

The backend is responsible for:

Authentication

Resume Upload

File Storage

Resume Parsing

AI Analysis

Recommendation APIs

Dashboard Data

Database Operations

The backend should not contain frontend logic.



TECHNOLOGY STACK

Language

Python 3.12+

Framework

FastAPI

Database ORM

SQLAlchemy

Validation

Pydantic

Authentication

JWT

Password Hashing

bcrypt + passlib

File Handling

PyMuPDF

Database

SQLite (default)



BACKEND FOLDER STRUCTURE

backend/



app/



main.py



config.py



database.py



models/



schemas/



routers/



services/



ai/



utils/



uploads/



requirements.txt



DATABASE DESIGN

Version 1 should contain only three database tables.



Users Table

Purpose

Store user accounts.

Fields

id



full_name



email



password_hash



created_at

Requirements

Email must be unique.

Passwords must never be stored in plain text.

Use UUID or auto-increment ID.



Resumes Table

Purpose

Store uploaded resumes.

Fields

id



user_id



file_name



file_path



uploaded_at

Requirements

One user can upload multiple resumes.

Store only the file path, not the file contents in the database.



AnalysisReports Table

Purpose

Store AI analysis results.

Fields

id



resume_id



career_goal



resume_score



ats_score



present_skills



missing_skills



roadmap



recommended_courses



recommended_projects



recommended_internships



created_at

Store structured data as JSON where appropriate.



DATABASE RELATIONSHIPS

User



│



├── Resume



│



└── Analysis Report

One User

↓

Many Resumes

One Resume

↓

One Analysis Report



AUTHENTICATION

Authentication should be simple.

Implement

Register

Login

Logout

Use JWT authentication.

Password hashing must use bcrypt.

Protected endpoints require a valid JWT.



FILE STORAGE

Store uploaded resumes locally.

Example structure

backend/



uploads/



resume1.pdf



resume2.pdf

Generate unique filenames to avoid conflicts.

Validate:

PDF only

Maximum file size

Reject corrupted files



CORE BACKEND SERVICES

Create the following services.



Authentication Service

Responsibilities

Register users

Login users

Hash passwords

Generate JWT

Validate JWT



Resume Service

Responsibilities

Upload resumes

Save files

Retrieve resumes

Delete resumes



Analysis Service

Responsibilities

Trigger AI pipeline

Save analysis report

Return dashboard data



Dashboard Service

Responsibilities

Combine analysis data

Format dashboard response

Provide statistics



Pydantic Schemas

Create schemas for:

UserCreate



UserLogin



UserResponse



ResumeUpload



ResumeResponse



AnalysisResponse



DashboardResponse

Never expose password hashes.



API DESIGN

Use REST APIs.

Version all APIs.

/api/v1/



IMPORTANT APIs

Authentication

POST /auth/register



POST /auth/login

Resume

POST /resume/upload



GET /resume/{id}



DELETE /resume/{id}

Analysis

POST /analysis/run



GET /analysis/{id}

Dashboard

GET /dashboard

Keep the API surface small and focused.



REQUEST FLOW

React



↓



Axios



↓



FastAPI Router



↓



Service Layer



↓



Database / AI Module



↓



Response



↓



Frontend



ERROR HANDLING

Every endpoint must:

Validate input

Return meaningful errors

Avoid exposing internal exceptions

Example status codes

200 OK

201 Created

400 Bad Request

401 Unauthorized

404 Not Found

500 Internal Server Error



SECURITY

Always:

Hash passwords

Validate JWT

Sanitize inputs

Restrict file uploads

Store secrets in environment variables

Do not implement advanced enterprise security features in Version 1.



LOGGING

Log:

Login

Resume upload

AI analysis start/end

Errors

Do not log passwords or tokens.



TESTING REQUIREMENTS

Create tests for:

Authentication

Resume Upload

Resume Retrieval

Analysis Endpoint

Dashboard Endpoint

Use pytest.



IMPLEMENTATION ORDER

The backend should be built in this order.



Database Connection

↓



User Model

↓



Authentication

↓



Resume Upload

↓



Resume Storage

↓



Analysis Endpoint

↓



Dashboard Endpoint

Only proceed after each step works.



DEFINITION OF DONE

The backend foundation is complete when:

✓ FastAPI starts successfully.

✓ Database connects.

✓ Migrations work (or tables initialize correctly for SQLite).

✓ Users can register.

✓ Users can log in.

✓ JWT authentication works.

✓ PDF resumes can be uploaded.

✓ Files are stored correctly.

✓ Analysis endpoint is callable (even if AI logic is added later).

✓ Dashboard endpoint returns structured data.

✓ No runtime errors.

✓ Project builds successfully.



END OF PART 3

At the end of this phase, SkillBridge AI has a clean backend foundation with authentication, database models, resume storage, API routing, and service architecture. This provides the base required for implementing the AI engine in the next phase.

SkillBridge AI – Portfolio Edition

PART 4 — FRONTEND FOUNDATION & UI ARCHITECTURE



ROLE

Continue building SkillBridge AI using Parts 1–3.

This section defines the frontend architecture.

The goal is to create a clean, modern, responsive web application that is easy to use and visually impressive during interviews and hackathons.

Do not over-engineer the frontend.

Focus on usability, clarity, and maintainability.



FRONTEND OBJECTIVES

The frontend should:

Provide a modern user experience.

Connect seamlessly with the FastAPI backend.

Display AI analysis results clearly.

Be fully responsive.

Be easy to extend.

The frontend should never contain AI logic or business logic.



TECHNOLOGY STACK

Framework

React 19

Language

TypeScript

Styling

Tailwind CSS

Routing

React Router

API Communication

Axios

State Management

Zustand

Forms

React Hook Form

Validation

Zod

Charts

Recharts

Icons

Lucide React

Animations

Framer Motion (only subtle animations)



FRONTEND FOLDER STRUCTURE

frontend/



src/



assets/



components/



layouts/



pages/



services/



store/



hooks/



types/



utils/



App.tsx



main.tsx



PAGE STRUCTURE

Version 1 should contain only these pages.

Authentication

Login

Register

Main

Dashboard

Resume Upload

Analysis Report

Learning Roadmap

Profile

Utility

404 Page

No admin panel.

No settings page.

No notifications page.



USER FLOW

Login/Register



↓



Dashboard



↓



Upload Resume



↓



AI Analysis



↓



Dashboard Updates



↓



Roadmap



↓



Recommendations

The user should never feel lost.



LAYOUT

The application uses one main layout.

Navbar



↓



Page Content



↓



Footer

The layout remains consistent across all pages.



NAVIGATION BAR

The navigation bar should contain:

Logo

Dashboard

Upload Resume

Roadmap

Profile

Logout

Requirements:

Sticky top navigation.

Mobile responsive.

Highlight active page.



DASHBOARD PAGE

The dashboard is the primary screen.

Display:

Top Section

Welcome message

Career Goal

Resume Score

ATS Score

Middle Section

Existing Skills

Missing Skills

Progress Overview

Bottom Section

Recommended Courses

Recommended Projects

Recommended Internships

Include quick action buttons:

Upload New Resume

Reanalyze Resume



RESUME UPLOAD PAGE

Features:

Drag & Drop upload area.

Browse file button.

Career goal dropdown.

Upload progress indicator.

Validation:

PDF only.

File size limit.

Display upload errors.

After successful upload:

Automatically trigger AI analysis.



ANALYSIS REPORT PAGE

Display extracted information.

Sections:

Personal Details

Education

Skills

Projects

Experience

Scores

Resume Score

ATS Score

Show improvement suggestions.

Display missing skills.



ROADMAP PAGE

Display roadmap as cards.

Each card contains:

Skill Name

Difficulty

Estimated Duration

Learning Resource

Mini Project

Completion Checkbox

Cards should be visually connected to indicate progression.



PROFILE PAGE

Allow users to view:

Name

Email

Career Goal

Uploaded Resume

Allow editing basic profile information.



REUSABLE COMPONENTS

Create reusable components.

Examples:

Button



Card



Modal



Navbar



Footer



ProgressBar



ScoreCard



SkillCard



RoadmapCard



RecommendationCard



Loader



EmptyState



ErrorState

Avoid duplicating UI code.



STATE MANAGEMENT

Use Zustand for:

Authentication

User Profile

Resume Information

Analysis Report

Avoid unnecessary global state.



API SERVICES

Create dedicated service files.

authService.ts



resumeService.ts



analysisService.ts



dashboardService.ts

All API calls must be centralized.

Do not call Axios directly from pages.



FORM HANDLING

Use React Hook Form.

Validate using Zod.

Forms:

Login

Register

Resume Upload

Display validation errors clearly.



RESPONSIVE DESIGN

Support:

Desktop

Tablet

Mobile

Requirements:

Responsive navigation.

Responsive cards.

Responsive charts.

Responsive forms.



DESIGN PRINCIPLES

The UI should feel like:

LinkedIn Learning

Notion

Coursera

GitHub

Use:

Rounded cards.

Soft shadows.

Clean spacing.

Blue accent color.

Modern typography.

Avoid excessive gradients or animations.



LOADING STATES

Every API request should display:

Skeleton loader.

Spinner for uploads.

Disabled buttons during submission.



ERROR STATES

Show meaningful messages for:

Failed login.

Upload failure.

Network issues.

AI analysis failure.

Provide retry actions where appropriate.



EMPTY STATES

Display helpful guidance when:

No resume uploaded.

No analysis available.

No recommendations generated.

Avoid blank screens.



ACCESSIBILITY

Ensure:

Keyboard navigation.

Proper labels.

Sufficient color contrast.

Focus indicators.



IMPLEMENTATION ORDER

React setup

↓

Routing

↓

Layout

↓

Authentication pages

↓

Dashboard

↓

Resume Upload

↓

Analysis Page

↓

Roadmap Page

↓

Profile Page

↓

API Integration



DEFINITION OF DONE

The frontend is complete when:

✓ All pages render correctly.

✓ Navigation works.

✓ Forms validate properly.

✓ API services are connected.

✓ Responsive layout works.

✓ Upload flow functions.

✓ Dashboard displays backend data.

✓ No TypeScript errors.

✓ No console errors.

✓ Application builds successfully.



END OF PART 4

At the completion of this phase, the frontend provides a polished, responsive user interface capable of interacting with the backend and presenting AI-generated insights in a clear and professional manner.

SkillBridge AI – Portfolio Edition

PART 5 — AI ENGINE & RESUME INTELLIGENCE



ROLE

Continue building SkillBridge AI following Parts 1–4.

This section defines the AI Engine.

The AI system should solve one real problem:

Analyze a student's resume and provide personalized career guidance.

The AI should remain lightweight, explainable, and fast.

Do not implement LLM chatbots or AI agents in Version 1.



AI OBJECTIVE

The AI engine must perform six major tasks:

Parse Resume

Extract Skills

Calculate Resume Score

Calculate ATS Score

Detect Skill Gap

Generate Recommendations

Every recommendation should include a short explanation.



AI PIPELINE

Every uploaded resume follows this workflow.

PDF Resume



↓



Text Extraction



↓



Section Detection



↓



Information Extraction



↓



Skill Extraction



↓



Resume Score



↓



ATS Score



↓



Skill Gap Detection



↓



Roadmap Generation



↓



Course Recommendation



↓



Project Recommendation



↓



Internship Recommendation



↓



Dashboard



AI MODULE STRUCTURE

Create the following Python modules.

backend/



ai/



resume_parser.py



section_detector.py



skill_extractor.py



resume_scorer.py



ats_scorer.py



skill_gap.py



roadmap_generator.py



recommendation_engine.py



career_database.py



utils.py

Each module should have one responsibility.



MODULE 1 – Resume Parser

Purpose

Extract readable text from uploaded PDF resumes.

Library

PyMuPDF (Primary)

Fallback

pdfplumber

Responsibilities

Open PDF

Extract text

Preserve reading order

Handle multiple pages

Return clean text

Output

{

  "text":"Complete resume text..."

}



MODULE 2 – Section Detector

Split resume into sections.

Detect:

Contact Information

Education

Skills

Projects

Experience

Certifications

Achievements

Output

{

 "education":"...",

 "skills":"...",

 "projects":"...",

 "experience":"..."

}

The detector should use common resume headings.



MODULE 3 – Information Extraction

Extract structured information.

Required fields:

Personal

Name

Email

Phone

Education

College

Degree

Graduation Year

Projects

Title

Technologies

Experience

Company

Role

Links

GitHub

LinkedIn

Return structured JSON.



MODULE 4 – Skill Extraction

Use two methods:

Method 1

Dictionary Matching

Maintain a predefined skills database.

Example

Python



Java



SQL



React



FastAPI



TensorFlow



PyTorch



Docker



Git



Pandas



NumPy



Machine Learning



Deep Learning

Method 2

spaCy NLP

Extract skills using Named Entity Recognition and text processing.

Normalize similar skills.

Examples

ReactJS → React



ML → Machine Learning



JS → JavaScript



TF → TensorFlow

Remove duplicates before saving.



MODULE 5 – Resume Score

Calculate a score out of 100.

Suggested scoring:

Category

Marks

Technical Skills

30

Projects

20

Experience

15

Education

10

Certifications

10

Resume Structure

10

Links (GitHub/LinkedIn)

5

Output

{

 "resume_score":82

}

Display a breakdown on the dashboard.



MODULE 6 – ATS Score

Evaluate the resume for Applicant Tracking Systems.

Check:

Standard headings

Contact details

Keyword coverage

Formatting

Action verbs

Project descriptions

Generate:

ATS Score

Missing keywords

Suggestions

Output

{

 "ats_score":88,

 "suggestions":[

   "Add GitHub link",

   "Use stronger action verbs",

   "Mention project outcomes"

 ]

}



MODULE 7 – Skill Gap Detection

Input

Extracted Skills

Career Goal

Career Goals

AI Engineer

Data Scientist

Data Analyst

Python Developer

Backend Developer

Compare user skills with required skills.

Return:

Present Skills

Missing Skills

Priority

Example

{

 "present":[

   "Python",

   "SQL"

 ],

 "missing":[

   "Docker",

   "FastAPI",

   "Git"

 ]

}



MODULE 8 – Roadmap Generator

Generate a learning roadmap.

Example

Python



↓



Git



↓



SQL



↓



NumPy



↓



Pandas



↓



Machine Learning



↓



Deep Learning



↓



MLOps

Each roadmap item includes:

Skill

Why Learn It

Estimated Time

Mini Project



MODULE 9 – Recommendation Engine

Generate three types of recommendations.

Courses

Projects

Internships

Recommendations must be based on:

Career Goal

Missing Skills

Resume Score

Example

{

 "course":"Machine Learning with Python",



 "reason":"You already know Python. Machine Learning is your next logical step."

}

Every recommendation must explain why it was selected.



Career Database

Maintain a simple JSON file.

Example

{

 "AI Engineer":{

   "required_skills":[

     "Python",

     "NumPy",

     "Pandas",

     "Machine Learning",

     "Deep Learning",

     "TensorFlow",

     "Git",

     "SQL"

   ]

 }

}

This file powers:

Skill Gap

Roadmap

Recommendations

It should be easy to edit without changing Python code.



Recommendation Logic

Priority order:

Missing Skills

Career Goal

Resume Score

Existing Skills

Avoid recommending technologies the user already knows.



Dashboard Output

The AI should return one combined object.

Example

{

 "resume_score":85,



 "ats_score":90,



 "present_skills":[...],



 "missing_skills":[...],



 "roadmap":[...],



 "courses":[...],



 "projects":[...],



 "internships":[...]

}

The frontend should only consume this object.



Performance Requirements

The AI analysis should:

Complete within a few seconds for a typical resume.

Avoid unnecessary repeated processing.

Use lightweight models suitable for a portfolio application.

Heavy training pipelines are out of scope for Version 1.



Error Handling

Handle:

Empty PDFs

Corrupted files

Unsupported formats

Missing sections

Return user-friendly error messages.



Future Improvements (Not in Version 1)

Possible enhancements:

OCR for scanned resumes

Multi-language resume support

Job description matching

LLM-powered resume rewriting

GitHub repository analysis

LinkedIn profile analysis

AI mock interview module

These should not be implemented in the initial version.



IMPLEMENTATION ORDER



Resume Parser

↓



Section Detection

↓



Information Extraction

↓



Skill Extraction

↓



Resume Score

↓



ATS Score

↓



Skill Gap Detection

↓



Roadmap Generator

↓



Recommendation Engine

↓



Dashboard Integration

Complete each module before moving to the next.



DEFINITION OF DONE

The AI Engine is complete when:

✓ Resume text is extracted successfully.

✓ Resume sections are identified.

✓ Skills are extracted accurately.

✓ Resume Score is generated.

✓ ATS Score is generated.

✓ Skill Gap is detected.

✓ Learning Roadmap is generated.

✓ Courses are recommended.

✓ Projects are recommended.

✓ Internships are recommended.

✓ Every recommendation includes an explanation.

✓ Dashboard receives a complete analysis object.



END OF PART 5

At the end of this phase, SkillBridge AI has a functional AI engine capable of analyzing resumes, identifying strengths and weaknesses, generating meaningful recommendations, and producing a complete career guidance report suitable for demonstration in hackathons, internships, and placement interviews.

SkillBridge AI – Portfolio Edition

PART 6 — IMPLEMENTATION ROADMAP & BUILD INSTRUCTIONS



ROLE

Continue building SkillBridge AI using Parts 1–5.

This section defines the exact implementation sequence.

The AI coding agent must follow this order strictly.

Do NOT skip phases.

Do NOT build multiple major modules simultaneously.

Every phase must be completed, tested, and verified before proceeding.

The project must always remain in a working state.



DEVELOPMENT PHILOSOPHY

The project should evolve gradually.

Each completed phase should produce a working application.

Avoid writing unfinished code for future phases.

Implement only what is required for the current milestone.



PHASE 1 — Project Initialization

Objective

Create the project foundation.

Tasks

Initialize Git repository

Create folder structure

Setup FastAPI backend

Setup React frontend

Configure Tailwind CSS

Configure TypeScript

Configure SQLite database

Create environment variables

Configure CORS

Create README

Deliverables

Project compiles successfully.

Backend starts.

Frontend starts.

Folder structure complete.

Checkpoint

✓ Backend running

✓ Frontend running

✓ Database connected

✓ No build errors



PHASE 2 — Authentication

Objective

Allow users to create accounts and log in.

Tasks

Register

Login

Password hashing

JWT authentication

Protected routes

Deliverables

User can:

Register

Login

Logout

Checkpoint

✓ JWT works

✓ Passwords encrypted

✓ Protected endpoints secured



PHASE 3 — Resume Upload

Objective

Upload PDF resumes.

Tasks

Drag & Drop UI

File validation

Upload API

Save PDF locally

Store metadata

Deliverables

Users can upload resumes successfully.

Checkpoint

✓ PDF uploads

✓ Invalid files rejected

✓ File stored correctly



PHASE 4 — Resume Parser

Objective

Extract text from uploaded resumes.

Tasks

Read PDF

Extract text

Handle multiple pages

Clean extracted text

Deliverables

Resume text available for analysis.

Checkpoint

✓ Text extracted accurately

✓ No parsing errors



PHASE 5 — Information Extraction

Objective

Convert resume text into structured data.

Extract:

Name

Email

Education

Skills

Projects

Experience

Deliverables

Structured JSON object.

Checkpoint

✓ Data extracted correctly



PHASE 6 — Skill Extraction

Objective

Identify technical skills.

Methods

Dictionary matching

spaCy NLP

Deliverables

Skill list.

Checkpoint

✓ Skills normalized

✓ Duplicates removed



PHASE 7 — Resume Intelligence

Objective

Generate resume evaluation.

Tasks

Resume Score

ATS Score

Improvement Suggestions

Deliverables

Analysis report.

Checkpoint

✓ Scores generated

✓ Suggestions displayed



PHASE 8 — Skill Gap Analysis

Objective

Compare user skills with career requirements.

Tasks

Load career database

Compare skills

Generate missing skills

Deliverables

Skill Gap Report.

Checkpoint

✓ Missing skills displayed



PHASE 9 — Recommendation Engine

Objective

Generate recommendations.

Generate

Courses

Projects

Internships

Every recommendation must include a reason.

Checkpoint

✓ Recommendations generated

✓ Explanations included



PHASE 10 — Roadmap Generator

Objective

Generate personalized roadmap.

Roadmap should include:

Skill

Duration

Learning Resource

Mini Project

Checkpoint

✓ Roadmap generated



PHASE 11 — Dashboard

Objective

Integrate all AI outputs.

Dashboard displays:

Resume Score

ATS Score

Skills

Skill Gap

Roadmap

Recommendations

Checkpoint

✓ Dashboard fully functional



PHASE 12 — Testing

Run tests for:

Backend

Authentication

Upload

Parser

Analysis

Dashboard

Frontend

Components

Forms

API Integration

Manual Testing

Complete user workflow

Checkpoint

✓ Critical features work

✓ No runtime errors



PHASE 13 — UI Polish

Improve:

Responsive design

Animations

Icons

Loading states

Error messages

Empty states

The application should look polished enough for a hackathon demo.



PHASE 14 — Deployment

Deploy:

Frontend

Vercel

Backend

Render

Database

SQLite or PostgreSQL

Ensure the deployed version works without code changes.



DEVELOPMENT RULES

The AI must:

Build one phase at a time.

Never generate placeholder code.

Never duplicate logic.

Use reusable components.

Keep services independent.

Write readable code.

Follow consistent naming conventions.

Keep functions small and focused.



REVIEW CHECKLIST

After every phase verify:

✓ Application builds successfully.

✓ No Python errors.

✓ No TypeScript errors.

✓ APIs function correctly.

✓ UI renders properly.

✓ Code follows project structure.

✓ Documentation updated.

Only continue after all checks pass.



GIT WORKFLOW

After each completed phase:

Review code.

Run tests.

Commit changes.

Push to repository.

Example commits:

feat: implement authentication



feat: add resume upload



feat: implement resume parser



feat: add AI recommendation engine



feat: create dashboard



ERROR HANDLING

Every feature must:

Validate inputs.

Display meaningful errors.

Recover gracefully where possible.

Never expose internal exceptions to users.



DEFINITION OF DONE

The project is complete when:

✓ Users can register and log in.

✓ Users can upload resumes.

✓ AI analyzes resumes.

✓ Resume Score generated.

✓ ATS Score generated.

✓ Skills extracted.

✓ Skill Gap detected.

✓ Personalized roadmap generated.

✓ Courses recommended.

✓ Projects recommended.

✓ Internships recommended.

✓ Dashboard displays all results.

✓ Application deployed successfully.

✓ README includes setup and usage instructions.



FINAL DELIVERABLE

The finished project should be:

Easy to run locally.

Easy to deploy.

Easy to explain in interviews.

Well-structured.

Visually appealing.

AI-powered.

Fully functional.

The focus is on quality, completeness, and demonstration value rather than enterprise-scale complexity.



END OF PART 6

At the completion of this phase, the AI coding agent has a clear, sequential execution plan that minimizes errors, keeps the application functional throughout development, and produces a polished portfolio project suitable for hackathons, internships, and placement interviews.

SkillBridge AI – Portfolio Edition

PART 7 — CODING STANDARDS & AI DEVELOPMENT RULES



ROLE

Continue building SkillBridge AI using Parts 1–6.

This document defines the coding standards that every generated file must follow.

The objective is to ensure that the entire codebase remains:

Clean

Consistent

Modular

Readable

Easy to maintain

Easy to extend

These rules apply to every backend file, frontend component, AI module, and utility.



DEVELOPMENT PHILOSOPHY

The project is intended to be:

A complete portfolio project

Easy for one developer to maintain

Easy for interviewers to understand

Easy to deploy

Easy to improve

Do not optimize for enterprise complexity.

Optimize for clarity and quality.



GENERAL RULES

Always:

Build one feature at a time.

Finish one module before starting another.

Keep the application working after every phase.

Prefer simple solutions over complex ones.

Write code that another student can understand.

Never:

Duplicate code.

Mix frontend and backend logic.

Hardcode secrets.

Ignore errors.

Leave unfinished implementations.



PYTHON CODING STANDARDS

Follow:

PEP 8

Type hints

Small functions

Meaningful variable names

Preferred naming:

resume_parser.py



skill_extractor.py



resume_score.py



roadmap_generator.py

Avoid:

parser2.py



new.py



final_parser.py



temp.py



FUNCTION RULES

Each function should have one responsibility.

Good examples:

extract_text()



extract_skills()



calculate_resume_score()



generate_roadmap()

Avoid:

process_everything()



handle_resume()



run_ai()

One function should perform one task only.



CLASS DESIGN

Create classes only when necessary.

Prefer simple functions unless shared state is required.

Avoid deep inheritance.

Use composition instead of inheritance wherever possible.



FASTAPI RULES

Routers should only:

Receive requests

Validate input

Call services

Return responses

Business logic belongs in:

services/

AI logic belongs in:

ai/

Database logic belongs in:

models/



REACT CODING STANDARDS

Use:

Functional Components

TypeScript

Hooks

Avoid:

Class Components

Inline business logic

Large monolithic files

One component should have one clear purpose.



COMPONENT SIZE

Recommended maximum sizes:

React Component

300 lines

Python File

400 lines

Utility

200 lines

If a file grows beyond this, split it into smaller modules.



NAMING CONVENTIONS

React Components

ResumeUpload.tsx



Dashboard.tsx



SkillCard.tsx

Hooks

useResume.ts



useDashboard.ts

Services

resumeService.ts



analysisService.ts

Python Files

resume_parser.py



ats_scorer.py



skill_gap.py

Variables

Use descriptive names.

Example:

resume_score



missing_skills



career_goal



analysis_result

Avoid:

a



temp



data1



x



DATABASE RULES

Keep the schema simple.

Only create tables when required.

Always use foreign keys.

Do not store duplicate information.

Store AI results as structured JSON where appropriate.



API STANDARDS

All APIs must:

Follow REST principles

Return JSON

Validate input

Return proper HTTP status codes

Response format:

{

  "success": true,

  "message": "Resume analyzed successfully",

  "data": {}

}

Error format:

{

  "success": false,

  "message": "Invalid PDF file"

}

Keep response structures consistent.



ERROR HANDLING

Never ignore exceptions.

Always:

Catch expected errors

Return user-friendly messages

Log unexpected errors

Do not expose stack traces to users.



LOGGING

Log:

User login

Resume upload

AI analysis started

AI analysis completed

Unexpected errors

Do not log:

Passwords

JWT tokens

Personal sensitive information



FORM VALIDATION

Validate:

Email format

Password length

PDF upload

Required fields

Never trust frontend validation alone.

Always validate again on the backend.



FILE UPLOAD RULES

Accept:

PDF only

Reject:

Images

DOCX

ZIP

EXE

Maximum size:

Choose a reasonable limit suitable for resumes.

Generate unique filenames before storing files.



AI MODULE RULES

Every AI module should:

Receive structured input.

Perform one task.

Return structured output.

Never access the database directly.

Never call frontend APIs.

Remain independent so it can be tested in isolation.



PERFORMANCE GUIDELINES

Avoid:

Repeated database queries

Duplicate AI processing

Unnecessary re-renders

Cache only if required in future versions.

Version 1 should prioritize simplicity.



TESTING

Every completed feature should be tested.

Backend:

Unit tests

API tests

Frontend:

Component rendering

Form validation

Manual:

Complete user workflow



DOCUMENTATION

After every completed module update:

README

API notes

Installation guide

Project screenshots (optional)

Keep documentation synchronized with implementation.



GIT PRACTICES

Commit after every completed feature.

Examples:

feat: implement authentication



feat: add resume upload



feat: create resume parser



feat: add recommendation engine



fix: improve PDF parsing



refactor: simplify dashboard service

Avoid committing multiple unrelated features together.



CODE REVIEW CHECKLIST

Before considering any feature complete:

✓ Code compiles

✓ No warnings

✓ No unused imports

✓ Functions have meaningful names

✓ No duplicated logic

✓ APIs tested

✓ UI responsive

✓ Error handling implemented

✓ Documentation updated



AI DEVELOPMENT RULES

When generating code:

Do not rewrite existing modules unless necessary.

Reuse existing utilities.

Preserve project structure.

Follow naming conventions.

Prefer readability over clever implementations.

Explain non-obvious logic with concise comments.

If a requirement is unclear, stop and request clarification rather than making assumptions.



PROJECT QUALITY GOALS

The final project should demonstrate:

Full-stack development

Python backend

React frontend

NLP fundamentals

Resume parsing

Recommendation systems

Clean architecture

REST APIs

Good UI/UX

Deployable application

The project should be realistic for a single developer and polished enough to showcase during hackathons, internships, and placement interviews.



SkillBridge AI – Portfolio Edition

PART 8 — MASTER AI INSTRUCTIONS & PROJECT CONSTITUTION



ROLE

You are the primary Software Engineer responsible for developing SkillBridge AI.

You are not just writing code.

You are designing, implementing, testing, documenting, and maintaining a complete AI-powered web application.

Throughout development, act as:

Senior Python Developer

Senior React Developer

AI/ML Engineer

UI/UX Engineer

Database Designer

Software Architect

Code Reviewer

Always make decisions that improve code quality while keeping the project simple enough for one developer to understand and maintain.



PROJECT MISSION

Build a complete AI-powered Career Mentor platform that helps students:

Upload resumes

Analyze resumes

Detect skills

Find missing skills

Generate Resume Score

Generate ATS Score

Recommend courses

Recommend projects

Recommend internships

Generate personalized learning roadmaps

The application should solve a real problem while remaining lightweight and deployable.



PRIMARY GOAL

The goal is not to build the biggest project.

The goal is to build one of the best finished AI portfolio projects.

Success is measured by:

Clean code

Working features

Good UI

Good AI logic

Easy deployment

Easy explanation during interviews



CORE PRINCIPLES

Every decision should follow these principles.

Simplicity

Always choose the simplest solution that satisfies the requirements.

Avoid unnecessary abstractions.



Readability

Write code for humans first.

Prefer clarity over clever implementations.



Modularity

Every module should have one responsibility.

Modules should be reusable and independently testable.



Consistency

Follow the same coding style across the entire project.

Do not mix architectural patterns.



Maintainability

Future improvements should be easy to implement without rewriting the application.



PROJECT BOUNDARIES

Version 1 includes only:

Authentication

Resume Upload

Resume Parser

Skill Extraction

Resume Score

ATS Score

Skill Gap Detection

Roadmap Generator

Course Recommendation

Project Recommendation

Internship Recommendation

Dashboard

Do not add:

Chatbot

Multi-agent systems

Payments

Subscriptions

Notifications

OAuth

Admin Panel

Redis

Microservices

Kubernetes

Background jobs

Event-driven architecture

If a feature is outside Version 1, note it as a future enhancement instead of implementing it.



AI DEVELOPMENT RULES

Before writing any code:

Read the existing project structure.

Identify dependencies.

Avoid duplicate functionality.

Reuse existing modules.

Follow Parts 1–7.

Never generate code that breaks existing functionality.



IMPLEMENTATION STRATEGY

For every feature:

Step 1

Understand the requirement.

↓

Step 2

Identify required files.

↓

Step 3

Implement backend.

↓

Step 4

Implement frontend.

↓

Step 5

Connect APIs.

↓

Step 6

Test.

↓

Step 7

Refactor if necessary.

↓

Step 8

Update documentation.

Only then proceed to the next feature.



CODE GENERATION RULES

Generated code must:

Compile successfully.

Avoid warnings.

Avoid unused imports.

Include meaningful names.

Be modular.

Be easy to read.

Include concise comments only where necessary.

Do not generate placeholder code unless explicitly requested.



API RULES

Every endpoint should:

Validate input.

Return consistent JSON.

Handle errors gracefully.

Use proper HTTP status codes.

Do not expose internal implementation details.



DATABASE RULES

Keep the schema simple.

Avoid unnecessary tables.

Store structured data.

Maintain referential integrity.

Use migrations if the database schema evolves.



AI MODULE RULES

Every AI module should:

Accept structured input.

Perform one task.

Return structured output.

Be deterministic where practical.

Explain recommendations when possible.

The AI engine should never directly interact with the frontend.



FRONTEND RULES

The frontend should:

Be responsive.

Be accessible.

Use reusable components.

Separate presentation from API communication.

Display loading, success, error, and empty states.

Avoid business logic inside UI components.



ERROR HANDLING

Never fail silently.

Every error should:

Be logged.

Return a meaningful message.

Allow the application to continue when appropriate.



TESTING RULES

Every completed feature must be verified.

Backend

Unit tests

API tests

Frontend

Component tests

Manual testing

End-to-End

Complete user journey:Register → Login → Upload Resume → Analyze → View Dashboard

Do not continue until the current feature works.



PERFORMANCE RULES

Optimize for:

Fast startup

Fast resume analysis

Responsive UI

Avoid premature optimization.

Keep algorithms efficient but understandable.



SECURITY RULES

Always:

Hash passwords.

Validate JWT tokens.

Restrict uploaded files.

Sanitize inputs.

Protect private routes.

Keep secrets in environment variables.

Never hardcode credentials.



GIT WORKFLOW

After each completed feature:

Review the code.

Run tests.

Verify functionality.

Commit with a meaningful message.

Example:

feat: implement resume parser



feat: add ATS scoring



feat: create recommendation engine



fix: improve PDF validation



refactor: simplify dashboard components



SELF-REVIEW CHECKLIST

Before considering any task complete, verify:

✓ Application builds successfully.

✓ No Python errors.

✓ No TypeScript errors.

✓ No console warnings.

✓ No duplicated code.

✓ APIs respond correctly.

✓ Database updates correctly.

✓ UI works on desktop and mobile.

✓ Loading and error states exist.

✓ Documentation updated.

If any item fails, fix it before proceeding.



DEFINITION OF SUCCESS

SkillBridge AI is successful when:

A user can:

Register.

Log in.

Upload a PDF resume.

Receive AI-powered analysis.

View Resume Score.

View ATS Score.

Understand skill gaps.

Receive a personalized roadmap.

Discover relevant courses, projects, and internships.

Use the application smoothly from start to finish.

The application should be:

Fully functional.

Visually polished.

Easy to explain.

Easy to deploy.

Suitable for hackathons.

Suitable for internship interviews.

Suitable for placement interviews.

A project the developer is proud to showcase.



FINAL INSTRUCTION

Treat every new implementation request as an extension of this document.

Never abandon the established architecture.

Never sacrifice readability for complexity.

Prefer simple, robust, and maintainable solutions.

When in doubt, choose the design that a future developer—or the project owner six months later—will find easiest to understand.

The objective is not merely to generate code, but to deliver a polished, reliable, and educational AI application that demonstrates strong software engineering practices.





