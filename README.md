# 🎓 PathFinder AI – AI-Powered Personalized Learning Path Generator

**PathFinder AI** is an AI-powered personalized learning platform designed to help students and fresh graduates identify skill gaps and build structured learning roadmaps based on their career goals, existing skills, and learning preferences.

Instead of following generic learning plans, users receive customized roadmaps with recommended topics, learning resources, practical projects, milestones, and progress tracking.

## 🚀 Key Features

- **Student Profile:** Add educational background, existing skills, career interests, and learning preferences.
- **Skill Assessment:** Take predefined assessments to evaluate your knowledge.
- **Skill Gap Analysis:** Identify strong skills, intermediate skills, and areas that need improvement.
- **Personalized Learning Roadmap:** Generate a structured learning plan based on your assessment results and career goals.
- **Learning Resources:** Access recommended tutorials, documentation, courses, and other learning materials.
- **Progress Tracking:** Monitor completed topics, milestones, and overall learning progress.
- **Dashboard:** View learning statistics and roadmap progress.

## 🛠️ Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React.js, Vite, Tailwind CSS |
| Backend | Python, Flask |
| Database | SQLite |
| AI Integration | Amazon Bedrock |
| Cloud Storage | Amazon S3 |
| Serverless Processing | AWS Lambda |
| API Integration | Amazon API Gateway |
| Visualization | Recharts |
| Version Control | Git, GitHub |

## ☁️ AWS Integration

The project is designed to integrate with the following AWS services:

- **Amazon Bedrock:** Generates personalized learning roadmaps.
- **Amazon S3:** Stores learning resources and related files.
- **AWS Lambda:** Processes student inputs and AI requests.
- **Amazon API Gateway:** Connects the frontend with backend services.

A local rule-based fallback can be used when AWS credentials are not configured.

## 📂 Project Structure

```text
PathFinder-AI/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── requirements.txt
│
├── docs/
├── .env.example
├── .gitignore
└── README.md
```

*The structure may vary depending on the final implementation.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/AI-Personalized-Learning-Path-Generator.git
cd AI-Personalized-Learning-Path-Generator
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend:

```bash
python app.py
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed in your terminal to access the application.

## 🎯 How It Works

1. Register or log in to the application.
2. Complete your student profile.
3. Select your desired career path.
4. Take the skill assessment.
5. Review your skill gap analysis.
6. Generate your personalized learning roadmap.
7. Follow recommended resources and complete milestones.
8. Track your learning progress through the dashboard.

## 🔮 Future Enhancements

- AI-powered adaptive assessments.
- Integration with more learning platforms.
- Personalized project recommendations.
- Resume-based skill extraction.
- Achievement badges and certificates.
- Advanced learning analytics.

## 🎓 Project Information

- **Project Name:** PathFinder AI
- **Domain:** Education / EdTech
- **Project Type:** AI-Powered Web Application
- **Target Users:** Students and Fresh Graduates

## 📄 License

This project is developed for educational and academic purposes.

---

**PathFinder AI – Discover Your Skills. Bridge Your Gaps. Build Your Future.**
