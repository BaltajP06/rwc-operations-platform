# RWC Operations Intelligence Platform
Built as a proof-of-concept platform demonstrating how AI can support construction operations teams by identifying project risks, workforce compliance issues, procurement delays, and cost overruns through a single dashboard.

A construction operations dashboard designed to help project teams identify risks before they become costly problems.

The platform combines project tracking, workforce compliance monitoring, material procurement visibility, and AI-powered risk analysis into a single operational view. Instead of manually reviewing spreadsheets and reports, managers can quickly see which projects require attention and why.

## Why I Built This

Construction projects generate large amounts of operational data, but important risks are often buried across multiple systems and reports.

This project explores how AI and data visualization can help operations teams identify:

- Schedule delays
- Workforce compliance issues
- Material procurement risks
- Cost overruns
- Safety concerns

The goal is to provide actionable insights in seconds rather than hours of manual review.

## Key Features

### Executive Command Center
Centralized dashboard displaying operational KPIs and project health metrics.

### Project Risk Tracker
Monitors active projects and assigns risk ratings based on schedule, workforce, material, and cost factors.

### AI Risk Analysis Engine
Uses AI-powered analysis to explain project risks and suggest actions.

### Workforce Compliance Dashboard
Tracks certifications, workforce readiness, and overtime exposure.

### Procurement & Materials Monitoring
Highlights supply chain concerns, shortages, and procurement delays.

### Cost Impact Analysis
Provides visibility into budget variance and contingency usage.

### Executive Reporting
Generates professional PDF reports for management reviews.

### Operational Alerts
Surfaces critical issues requiring immediate attention.

## Technology Stack

- Python
- Streamlit
- Pandas
- Plotly
- OpenAI API
- ReportLab

## Architecture

The application follows a modular architecture with separate layers for:

- Data processing
- Risk analysis
- Visualization
- Reporting

Future versions are designed to support live integrations with systems such as Procore.

## Running Locally

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

## Future Improvements

- PostgreSQL integration
- Procore API connectivity
- Role-based authentication
- Real-time project updates
- Mobile-responsive dashboards
- Predictive analytics

## What This Demonstrates

- Python development
- Data visualization
- AI-powered insights
- Report generation
- Business process automation
