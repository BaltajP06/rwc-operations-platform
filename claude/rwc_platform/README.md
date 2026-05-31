# RWC Operations Intelligence Platform

**Enterprise-Grade Construction Management Dashboard**  
Built with Python · Streamlit · Plotly · Pandas · AI-Assisted Analysis

---

## What This Is

A fully functional internal operations platform for a commercial construction company. Built to demonstrate systems thinking, operational UX design, and AI integration for a portfolio / job interview context.

Features 8 modules:
- Executive Command Center (live KPIs)
- Live Project Tracker (drill-down cards, filtering, risk scoring)
- AI Analysis Engine (delay analysis, workforce risk, cost risk, bottleneck detection)
- Workforce Intelligence (heatmaps, certification compliance, overtime)
- Material & Procurement Monitor (supply chain risk scoring)
- Cost Impact Engine (financial variance, budget tracking)
- Executive AI Briefing Panel (board-ready PDF report)
- Operational Alert Center (safety, procurement, HR alerts)

---

## Folder Structure

```
rwc_platform/
├── app.py                    ← Main Streamlit app (entry point)
├── requirements.txt          ← Python dependencies
├── README.md                 ← This file
│
├── data/
│   ├── __init__.py
│   └── demo_data.py          ← All demo data generators (projects, workforce, materials, safety, costs)
│
├── modules/
│   ├── __init__.py
│   └── ai_engine.py          ← AI analysis engine (OpenAI + mock fallback)
│
├── utils/
│   ├── __init__.py
│   └── charts.py             ← All Plotly chart functions
│
├── reports/
│   ├── __init__.py
│   └── pdf_generator.py      ← ReportLab PDF export
│
└── assets/                   ← (reserved for logos, fonts if needed)
```

---

## Installation

### Prerequisites
- Python 3.9 or higher
- pip

### Step 1 — Clone or create the project folder

```bash
# If downloading as a zip, extract it. Then:
cd rwc_platform
```

### Step 2 — Create a virtual environment (recommended)

```bash
python -m venv venv

# Activate it:
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

This installs: `streamlit`, `pandas`, `numpy`, `plotly`, `openai`, `reportlab`

### Step 4 — Run the app

```bash
streamlit run app.py
```

The app will open automatically at: **http://localhost:8501**

---

## Using the App

### Demo Mode (no API key needed)
The app runs fully in demo mode by default. All AI outputs are generated using advanced mock logic that produces realistic, professional-sounding analysis. No API key required.

### Live AI Mode (optional)
To use real GPT-4 analysis:
1. Enter your OpenAI API key in the sidebar text field
2. The app will use `gpt-4` for executive summaries and operational analysis

---

## Key Commands Reference

```bash
# Run the app
streamlit run app.py

# Run with a specific port
streamlit run app.py --server.port 8080

# Run without opening browser
streamlit run app.py --server.headless true

# Test all modules without starting the UI
python -c "from data.demo_data import get_kpi_summary; print(get_kpi_summary())"
```

---

## How to Keep This Project (Before GitHub)

### What to do right now:

1. **Keep all files in the `rwc_platform/` folder** — don't move individual files around. The relative imports depend on the folder structure.

2. **Create a `.gitignore` file** in the root folder with:
   ```
   venv/
   __pycache__/
   *.pyc
   .env
   .DS_Store
   *.egg-info/
   dist/
   ```

3. **Never commit your API key.** If you use one, store it in a `.env` file and load it with `python-dotenv`:
   ```bash
   pip install python-dotenv
   ```
   Then in `app.py`:
   ```python
   from dotenv import load_dotenv
   import os
   load_dotenv()
   api_key = os.getenv("OPENAI_API_KEY", "")
   ```
   And in `.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

4. **Make a backup** — copy the entire `rwc_platform/` folder to a cloud drive before touching anything.

---

## How to Put This on GitHub (When Ready)

### Step 1 — Create a GitHub account (if needed)
Go to https://github.com and create a free account.

### Step 2 — Create a new repository
- Click "New repository"
- Name it: `rwc-operations-platform`
- Set to **Private** (recommended for a portfolio project)
- Do NOT initialize with README (you already have one)
- Click "Create repository"

### Step 3 — Initialize git locally

```bash
cd rwc_platform

# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: RWC Operations Intelligence Platform v1.0"

# Connect to GitHub (replace YOUR_USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/rwc-operations-platform.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4 — Subsequent updates
```bash
git add .
git commit -m "Describe what you changed"
git push
```

---

## Future Scalability Ideas

### Near-term Additions
- **Real database backend**: Replace `demo_data.py` with a PostgreSQL or SQLite database. Use SQLAlchemy for ORM.
- **User authentication**: Add Streamlit Authenticator or Auth0 integration for login/roles.
- **Real-time data refresh**: Add auto-refresh intervals for live job site data feeds.
- **Project creation/editing UI**: Add forms to create and update project records in the database.
- **Email notifications**: Send automated alerts via SendGrid when safety or schedule thresholds are breached.

### AI Enhancements
- **Procore API integration**: Pull real project data from Procore using their REST API. Replace `demo_data.py` with live Procore calls.
- **Microsoft 365 integration**: Use Microsoft Graph API to push briefings to Teams channels or Outlook calendars.
- **Predictive delay modeling**: Train a simple ML model (scikit-learn) on historical project data to predict delay probability.
- **Voice briefings**: Use OpenAI TTS to generate spoken executive briefings as MP3 files.
- **GPT-4 Vision**: Upload site photos and have AI identify safety issues automatically.

### Enterprise Deployment
- **Deploy to Streamlit Cloud**: Free hosting at https://streamlit.io/cloud — connect your GitHub repo and deploy in minutes.
- **Deploy to Azure/AWS**: Use Docker + Azure App Service or AWS Elastic Beanstalk for enterprise hosting.
- **Docker containerization**:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY . .
  EXPOSE 8501
  CMD ["streamlit", "run", "app.py", "--server.headless", "true"]
  ```

### Procore / Microsoft Integration Notes
- **Procore**: REST API at `https://api.procore.com/rest/v1.0/` — requires OAuth 2.0. Key endpoints: `/projects`, `/submittals`, `/rfis`, `/schedule/tasks`. Replace `get_projects_df()` with live API calls.
- **Microsoft Teams**: Use Power Automate or direct Graph API webhooks to post the daily briefing card to a Teams channel automatically.
- **Microsoft Project**: Use the Project Online REST API to sync schedule data with Gantt charts.

---

## Interview Talking Points

When presenting this project, highlight:

1. **Systems thinking**: The platform models the actual operational complexity of construction management — not just a CRUD app.
2. **AI integration pattern**: The OpenAI-compatible architecture with graceful mock fallback shows production-readiness thinking.
3. **Modular architecture**: Each module (data, AI, charts, reports) is independently testable and replaceable.
4. **Enterprise UX**: Dark industrial aesthetic chosen deliberately to match construction industry culture.
5. **Scalability path**: You can explain exactly how this would connect to Procore, SAP, or Microsoft systems.

---

*RWC Operations Intelligence Platform — v1.0.0*  
*Built with Python + Streamlit + AI-Assisted Analysis*
