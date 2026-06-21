<div align="center">
  <h1>🚀 SkillBridge AI</h1>
  <p><strong>AI-Powered Career Mentor & Resume Intelligence Platform</strong></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  </p>
</div>

<br />

## 🌟 Overview
SkillBridge AI is a complete, full-stack career guidance platform designed to bridge the gap between academic learning and industry expectations. Unlike traditional ATS checkers that simply reject candidates, SkillBridge AI deeply analyzes your resume, detects your precise skill gaps relative to your dream job, and automatically generates a personalized, phased learning roadmap.

All AI logic runs completely **locally**, utilizing advanced NLP chunking, semantic heuristics, and strict PyDantic data modeling. Zero cloud LLMs. Zero latency.

## ✨ Key Features
- 📄 **Advanced Resume Parsing:** Accurately extracts Name, Contact, Education, Experience, Projects, and 150+ Technical Skills from unstructured PDFs.
- 🎯 **ATS & Resume Scoring:** Provides deep explainability on keyword density, action verbs, and structural resume flaws.
- 🧠 **Skill Gap Intelligence:** Cross-references extracted skills with an internal `careers.json` database to pinpoint exactly what you are missing and *why* it matters.
- 🗺️ **Dynamic Career Roadmaps:** Groups your missing skills into a phased timeline (Foundation ➔ Interview Ready) complete with mini-project ideas.
- 🔒 **Secure Authentication:** Complete JWT-based authentication system with salted password hashing.

## 🏗️ Architecture
```
SkillBridge-AI/
├── backend/                  # Python FastAPI Server
│   ├── app/
│   │   ├── ai/               # Local NLP Engine & Gap Detectors
│   │   ├── models/           # SQLAlchemy Database Models
│   │   ├── routers/          # API Endpoints (Auth, Resume, Dashboard)
│   │   └── schemas/          # PyDantic Validation Types
├── frontend/                 # React + TypeScript + Vite Client
│   ├── src/
│   │   ├── components/       # Reusable UI (Cards, Timeline, Layout)
│   │   ├── pages/            # Core Views (Dashboard, Roadmap, Upload)
│   │   └── services/         # Axios API Handlers
```

## 🚀 Quick Setup (Local Development)

### 1. Clone the repository
```bash
git clone https://github.com/your-username/SkillBridge-AI.git
cd SkillBridge-AI
```

### 2. Start the Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
*The API will be available at `http://localhost:8000`*

### 3. Start the Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```
*The App will be available at `http://localhost:5173`*

## 📚 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Register a new user |
| `POST` | `/api/v1/auth/login` | Obtain a JWT Bearer Token |
| `POST` | `/api/v1/resume/upload` | Upload and parse a PDF resume |
| `GET`  | `/api/v1/dashboard/summary` | Fetch the AI-generated JSON career report |

## 🧪 Testing
The frontend can be built for production testing using:
```bash
cd frontend
npm run build
```

## 🔐 Security Considerations
- JWT Tokens are utilized for session management.
- User passwords are encrypted using `bcrypt` (via `passlib`).
- File uploads strictly validate the `.pdf` MIME type and enforce a 5MB size limit.

## 🚀 Cloud Deployment

SkillBridge AI is designed to be easily deployed to modern cloud hosting platforms.

### 1. Backend & Database (Render)
The backend service and PostgreSQL database are configured to deploy using Render Blueprints.
1. Log in to your [Render Dashboard](https://dashboard.render.com).
2. Click **New** ➔ **Blueprint**.
3. Select your connected GitHub repository.
4. Render will parse the `render.yaml` file and prompt you to create:
   * `skillbridge-db` (PostgreSQL Database)
   * `skillbridge-backend` (FastAPI Web Service)
5. Click **Apply**. Render will deploy both services. Note down the public backend URL generated.

### 2. Frontend (Vercel)
The React client is fully optimized for static deployment on Vercel.
1. Log in to your [Vercel Dashboard](https://vercel.com).
2. Click **Add New** ➔ **Project** and import your repository.
3. Edit the project settings:
   * **Framework Preset:** Vite
   * **Root Directory:** `frontend`
4. Add the following **Environment Variable**:
   * **Key:** `VITE_API_BASE_URL`
   * **Value:** `https://<your-render-backend-url>/api/v1` (replace with your Render backend URL)
5. Click **Deploy**. Vercel will build the frontend, apply SPA rewrite rules (`vercel.json`), and launch the client app.

## 🔮 Future Scope

- **Job Board Integration:** Connect the gap analyzer to real-time scraping APIs to keep the target skills continuously updated.
- **Multilingual Support:** Support resume parsing in languages other than English.

---
*Built as a professional prototype for hackathons and software engineering portfolios.*
