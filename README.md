# RWC Operations Intelligence Platform

Enterprise-grade construction operations dashboard built with Python and Streamlit.

Replaces the Monday morning status call. Leadership opens one screen and sees everything — live project health, schedule risk, workforce compliance, material delays, cost variance — in 30 seconds.

## Modules
- Executive Command Center — 7 live KPIs with trend indicators
- Live Project Tracker — drill-down cards with AI risk grading A to F
- AI Analysis Engine — delay analysis, workforce risk, cost exposure
- Workforce Intelligence — certification compliance and overtime heatmap
- Material and Procurement Monitor — supply chain risk scoring
- Cost Impact Engine — variance tracking and contingency burn rate
- Executive AI Briefing — one-click board-ready PDF export
- Operational Alerts — safety, procurement and HR flags

## Stack
Python · Streamlit · Plotly · Pandas · OpenAI API · ReportLab

## Run Locally
pip install -r requirements.txt
streamlit run app.py

## Architecture
Modular design with 4 independent layers: data module, AI engine, charts module, PDF generator. Data layer is designed to be replaced with live Procore API calls for production deployment.

## Roadmap
- PostgreSQL backend
- Procore API integration
- Role-based authentication
- Mobile-responsive field view
