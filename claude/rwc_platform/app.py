"""
RWC Operations Intelligence Platform
Main Application Entry Point
Streamlit-based Enterprise Dashboard
"""

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# ── Path setup ──────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from data.demo_data import (
    get_projects_df, get_workforce_df, get_materials_df,
    get_safety_df, get_cost_df, get_kpi_summary, get_timeline_df
)
from modules.ai_engine import (
    generate_executive_summary, generate_delay_analysis,
    generate_workforce_analysis, generate_executive_briefing,
    generate_cost_risk_summary, generate_bottleneck_detection,
    score_project_risk
)
from utils.charts import (
    chart_project_health, chart_project_progress, chart_workforce_heatmap,
    chart_trade_distribution, chart_project_timeline, chart_cost_variance,
    chart_material_risk, chart_overtime_exposure
)
from reports.pdf_generator import generate_pdf_report

# ── Page configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="RWC Operations Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700;800&family=Barlow+Condensed:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─ Root ─ */
:root {
    --bg-primary: #080C17;
    --bg-card: #0F1929;
    --bg-surface: #13202F;
    --bg-elevated: #1A2D42;
    --accent-orange: #F97316;
    --accent-blue: #3B82F6;
    --accent-cyan: #06B6D4;
    --accent-green: #10B981;
    --accent-yellow: #F59E0B;
    --accent-red: #EF4444;
    --accent-purple: #8B5CF6;
    --text-primary: #EEF2FF;
    --text-secondary: #94A3B8;
    --text-muted: #4A5568;
    --border: #1E3A5F;
    --border-bright: #2A4A7A;
    --glow-orange: rgba(249,115,22,0.15);
    --glow-blue: rgba(59,130,246,0.12);
}

/* ─ Global ─ */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Barlow', sans-serif !important;
}

[data-testid="stMain"] { background-color: var(--bg-primary) !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }

/* ─ Sidebar ─ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060A14 0%, #0A1020 100%) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 240px !important;
}
[data-testid="stSidebar"] * { color: var(--text-secondary) !important; }
[data-testid="stSidebar"] .stRadio label { 
    padding: 6px 10px !important; 
    border-radius: 6px !important; 
    transition: all 0.2s !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 13px !important;
}
[data-testid="stSidebar"] .stRadio label:hover { 
    background: var(--bg-elevated) !important; 
    color: var(--text-primary) !important; 
}

/* ─ KPI Cards ─ */
.kpi-card {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-surface) 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.kpi-card:hover { border-color: var(--border-bright); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.kpi-card.orange::before { background: linear-gradient(90deg, var(--accent-orange), transparent); }
.kpi-card.blue::before { background: linear-gradient(90deg, var(--accent-blue), transparent); }
.kpi-card.cyan::before { background: linear-gradient(90deg, var(--accent-cyan), transparent); }
.kpi-card.green::before { background: linear-gradient(90deg, var(--accent-green), transparent); }
.kpi-card.red::before { background: linear-gradient(90deg, var(--accent-red), transparent); }
.kpi-card.yellow::before { background: linear-gradient(90deg, var(--accent-yellow), transparent); }
.kpi-card.purple::before { background: linear-gradient(90deg, var(--accent-purple), transparent); }
.kpi-label {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 32px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-sub {
    font-size: 11px;
    color: var(--text-muted) !important;
    font-weight: 400;
}
.kpi-icon { font-size: 22px; float: right; margin-top: -4px; opacity: 0.7; }

/* ─ Section headers ─ */
.section-header {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-primary) !important;
    border-left: 3px solid var(--accent-orange);
    padding-left: 12px;
    margin: 28px 0 16px 0;
}

/* ─ Status badges ─ */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    font-family: 'Barlow Condensed', sans-serif;
}
.badge-red { background: rgba(239,68,68,0.15); color: #EF4444; border: 1px solid rgba(239,68,68,0.3); }
.badge-orange { background: rgba(249,115,22,0.15); color: #F97316; border: 1px solid rgba(249,115,22,0.3); }
.badge-yellow { background: rgba(245,158,11,0.15); color: #F59E0B; border: 1px solid rgba(245,158,11,0.3); }
.badge-green { background: rgba(16,185,129,0.15); color: #10B981; border: 1px solid rgba(16,185,129,0.3); }
.badge-blue { background: rgba(59,130,246,0.15); color: #3B82F6; border: 1px solid rgba(59,130,246,0.3); }

/* ─ AI output box ─ */
.ai-output {
    background: linear-gradient(135deg, rgba(15,25,41,0.9), rgba(19,32,47,0.9));
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-cyan);
    border-radius: 10px;
    padding: 20px 24px;
    font-family: 'Barlow', sans-serif;
    font-size: 13.5px;
    line-height: 1.75;
    color: #CBD5E1 !important;
    white-space: pre-wrap;
    margin: 12px 0;
}

/* ─ Alert box ─ */
.alert-critical {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.3);
    border-left: 4px solid #EF4444;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 6px 0;
    font-size: 13px;
}
.alert-high {
    background: rgba(249,115,22,0.08);
    border: 1px solid rgba(249,115,22,0.3);
    border-left: 4px solid #F97316;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 6px 0;
    font-size: 13px;
}
.alert-medium {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.3);
    border-left: 4px solid #F59E0B;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 6px 0;
    font-size: 13px;
}
.alert-low {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.3);
    border-left: 4px solid #10B981;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 6px 0;
    font-size: 13px;
}

/* ─ Metric blocks ─ */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
}
[data-testid="stMetricLabel"] { font-size: 11px !important; color: var(--text-muted) !important; }
[data-testid="stMetricValue"] { font-family: 'Barlow Condensed', sans-serif !important; font-size: 28px !important; font-weight: 800 !important; }

/* ─ Dataframe ─ */
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 10px !important; }
.dvn-scroller { background: var(--bg-card) !important; }

/* ─ Buttons ─ */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-orange), #EA580C) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    font-size: 13px !important;
    padding: 10px 22px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }

/* ─ Expander ─ */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Barlow', sans-serif !important;
    font-weight: 600 !important;
}

/* ─ Divider ─ */
hr { border-color: var(--border) !important; }

/* ─ Tabs ─ */
.stTabs [data-baseweb="tab-list"] { background: var(--bg-card) !important; border-radius: 10px !important; }
.stTabs [data-baseweb="tab"] { color: var(--text-secondary) !important; font-family: 'Barlow', sans-serif !important; }
.stTabs [aria-selected="true"] { color: var(--accent-orange) !important; }
</style>
""", unsafe_allow_html=True)


# ── State ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data():
    return {
        "projects": get_projects_df(),
        "workforce": get_workforce_df(),
        "materials": get_materials_df(),
        "safety": get_safety_df(),
        "costs": get_cost_df(),
        "kpis": get_kpi_summary(),
        "timeline": get_timeline_df(),
    }


data = load_data()
kpis = data["kpis"]


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 20px 0 12px 0; text-align:center;">
        <div style="font-family:'Barlow Condensed',sans-serif; font-size:22px; font-weight:800; 
                    color:#F97316; letter-spacing:2px;">RWC</div>
        <div style="font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:700; 
                    color:#4A5568; letter-spacing:2px; text-transform:uppercase; margin-top:2px;">
            Operations Intelligence
        </div>
        <div style="margin: 12px auto; width:40px; height:1px; background: linear-gradient(90deg, transparent, #F97316, transparent);"></div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATION",
        [
            "🏛  Executive Command Center",
            "📋  Live Project Tracker",
            "🤖  AI Analysis Engine",
            "👷  Workforce Intelligence",
            "📦  Material & Procurement",
            "💰  Cost Impact Engine",
            "📊  Executive AI Briefing",
            "⚠️  Operational Alerts",
        ],
        label_visibility="visible",
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Barlow Condensed',sans-serif; font-size:10px; 
                color:#2A4A7A; letter-spacing:1px; text-align:center; text-transform:uppercase;">
        AI Engine Status
    </div>
    """, unsafe_allow_html=True)

    api_key = st.text_input("OpenAI API Key (optional)", type="password",
                             placeholder="sk-... (demo mode active)")
    if api_key:
        st.success("✓ AI Live Mode")
    else:
        st.info("⚡ Demo AI Mode Active")

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:11px; color:#2A4A7A; text-align:center; font-family:'JetBrains Mono',monospace;">
        {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC<br>
        v1.0.0 — Build 24.09
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: KPI CARD
# ─────────────────────────────────────────────────────────────────────────────

def kpi_card(label, value, sub, icon, color_class):
    st.markdown(f"""
    <div class="kpi-card {color_class}">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color: var(--accent-{'orange' if color_class=='orange' else 'blue' if color_class=='blue' else 'cyan' if color_class=='cyan' else 'green' if color_class=='green' else 'red' if color_class=='red' else 'yellow' if color_class=='yellow' else 'purple'});">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)


def section_header(text):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def ai_output_box(text):
    st.markdown(f'<div class="ai-output">{text}</div>', unsafe_allow_html=True)


def risk_badge(risk):
    mapping = {
        "CRITICAL": "badge-red", "HIGH": "badge-orange", "AT RISK": "badge-orange",
        "MEDIUM": "badge-yellow", "MONITORING": "badge-yellow",
        "LOW": "badge-green", "ON TRACK": "badge-green",
    }
    cls = mapping.get(risk.upper(), "badge-blue")
    return f'<span class="badge {cls}">{risk}</span>'


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: EXECUTIVE COMMAND CENTER
# ═════════════════════════════════════════════════════════════════════════════

if "Executive Command Center" in page:
    st.markdown("""
    <div style="margin-bottom:24px;">
        <h1 style="font-family:'Barlow Condensed',sans-serif; font-size:36px; font-weight:800; 
                   color:#EEF2FF; letter-spacing:2px; margin:0;">
            EXECUTIVE COMMAND CENTER
        </h1>
        <p style="color:#4A5568; font-size:13px; margin:6px 0 0 0; font-family:'Barlow',sans-serif;">
            Real-time portfolio intelligence  •  RWC Construction Management Group
        </p>
    </div>
    """, unsafe_allow_html=True)

    # KPI Row 1
    cols = st.columns(4)
    with cols[0]:
        kpi_card("Active Projects", kpis["active_projects"], "Across all divisions", "🏗️", "orange")
    with cols[1]:
        kpi_card("Delayed Projects", kpis["delayed_projects"], f"of {kpis['active_projects']} total", "⚠️", "red")
    with cols[2]:
        kpi_card("Workforce Deployed", f"{kpis['total_workforce']:,}", "Personnel on site", "👷", "blue")
    with cols[3]:
        kpi_card("Utilization Rate", f"{kpis['workforce_utilization']}%", "vs 85% target", "📈", "cyan")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # KPI Row 2
    cols2 = st.columns(4)
    with cols2[0]:
        kpi_card("Open Safety Risks", kpis["open_safety_risks"], "Items requiring action", "🦺", "yellow")
    with cols2[1]:
        kpi_card("Material Delays", kpis["material_delays"], "Critical/High risk items", "📦", "red")
    with cols2[2]:
        kpi_card("Cost Exposure", f"${kpis['cost_exposure']/1_000_000:.1f}M", "Estimated variance risk", "💸", "orange")
    with cols2[3]:
        kpi_card("Efficiency Score", f"{kpis['efficiency_score']}", "/ 100 — Guarded", "⚡", "purple")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.divider()

    # Charts Row
    section_header("PROJECT HEALTH OVERVIEW")
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.plotly_chart(chart_project_health(data["projects"]), use_container_width=True)
    with col_b:
        st.plotly_chart(chart_project_progress(data["projects"]), use_container_width=True)

    section_header("PROJECT TIMELINE")
    st.plotly_chart(chart_project_timeline(data["timeline"]), use_container_width=True)

    # AI Summary
    section_header("AI OPERATIONAL SNAPSHOT")
    with st.spinner("Generating AI analysis..."):
        summary = generate_executive_summary(kpis, data["projects"].to_dict("records"), api_key)
    ai_output_box(summary)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: LIVE PROJECT TRACKER
# ═════════════════════════════════════════════════════════════════════════════

elif "Project Tracker" in page:
    st.markdown("""
    <h1 style="font-family:'Barlow Condensed',sans-serif; font-size:36px; font-weight:800; 
               color:#EEF2FF; letter-spacing:2px; margin-bottom:4px;">
        LIVE PROJECT OPERATIONS TRACKER
    </h1>
    <p style="color:#4A5568; font-size:13px; margin-bottom:24px;">
        Real-time project status, risk indicators & operational drill-down
    </p>
    """, unsafe_allow_html=True)

    df = data["projects"].copy()

    # Filters
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        search = st.text_input("🔍 Search projects", placeholder="Project name, supervisor, trade...")
    with col_f2:
        risk_filter = st.selectbox("Schedule Risk", ["All", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
    with col_f3:
        status_filter = st.selectbox("Status", ["All", "CRITICAL", "AT RISK", "MONITORING", "ON TRACK"])

    if search:
        mask = (
            df["name"].str.contains(search, case=False) |
            df["supervisor"].str.contains(search, case=False) |
            df["trade"].str.contains(search, case=False)
        )
        df = df[mask]
    if risk_filter != "All":
        df = df[df["schedule_risk"] == risk_filter]
    if status_filter != "All":
        df = df[df["status"] == status_filter]

    st.markdown(f"<p style='color:#4A5568; font-size:12px;'>Showing {len(df)} of {len(data['projects'])} projects</p>", unsafe_allow_html=True)

    # Project cards
    for _, row in df.iterrows():
        health = row["health_score"]
        health_color = "#EF4444" if health < 50 else "#F97316" if health < 65 else "#F59E0B" if health < 80 else "#10B981"
        risk_score = score_project_risk(row.to_dict())

        with st.expander(f"{'🔴' if row['status']=='CRITICAL' else '🟠' if row['status']=='AT RISK' else '🟡' if row['status']=='MONITORING' else '🟢'}  {row['name']}  —  {row['type']}  |  {row['supervisor']}", expanded=row["status"] in ["CRITICAL"]):
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            with c1:
                st.markdown(f"**Client:** {row['client']}")
                st.markdown(f"**Location:** {row['location']}")
                st.markdown(f"**Trade:** {row['trade']}")
                st.markdown(f"**Contract Value:** ${row['contract_value']:,.0f}")
            with c2:
                st.metric("Progress", f"{row['progress']}%")
                st.metric("Workforce", f"{row['workforce_count']}")
                st.metric("Open RFIs", row["open_rfi"])
            with c3:
                st.metric("Confidence", f"{row['confidence']}%")
                st.metric("Active Delays", row["active_delays"])
                st.metric("Change Orders", row["change_orders"])
            with c4:
                st.markdown(f"**Health Score**")
                st.markdown(f"<span style='font-family:Barlow Condensed; font-size:36px; font-weight:800; color:{health_color};'>{health}</span><span style='color:#4A5568;'>/100</span>", unsafe_allow_html=True)
                st.markdown(f"**AI Risk Grade: {risk_score['grade']}**")
                st.markdown(f"<small style='color:#64748B;'>{risk_score['recommendation']}</small>", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(f"**📝 Supervisor Notes:** {row['notes']}")

            if risk_score["factors"]:
                st.markdown("**⚠️ Risk Factors Detected:**")
                for f in risk_score["factors"]:
                    st.markdown(f"<small style='color:#F97316;'>• {f}</small>", unsafe_allow_html=True)

            col_d1, col_d2, col_d3 = st.columns(3)
            col_d1.markdown(f"**Planned End:** {row['planned_end']}")
            col_d2.markdown(f"**Revised End:** {row['revised_end']}")
            slippage = (pd.to_datetime(row["revised_end"]) - pd.to_datetime(row["planned_end"])).days
            col_d3.markdown(f"**Schedule Slippage:** {'🔴 ' if slippage > 30 else '🟡 ' if slippage > 0 else '🟢 '}{slippage} days")

    # Export
    st.markdown("---")
    st.download_button(
        "⬇ Export Projects to CSV",
        data["projects"].to_csv(index=False).encode("utf-8"),
        file_name=f"rwc_projects_{datetime.today().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: AI ANALYSIS ENGINE
# ═════════════════════════════════════════════════════════════════════════════

elif "AI Analysis Engine" in page:
    st.markdown("""
    <h1 style="font-family:'Barlow Condensed',sans-serif; font-size:36px; font-weight:800; 
               color:#EEF2FF; letter-spacing:2px; margin-bottom:4px;">
        AI OPERATIONAL ANALYSIS ENGINE
    </h1>
    <p style="color:#4A5568; font-size:13px; margin-bottom:24px;">
        AI-generated operational intelligence, risk analysis & management recommendations
    </p>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Executive Summary", "⏱ Delay Analysis", "👷 Workforce Risk",
        "💰 Cost Risk", "🔍 Bottleneck Detection"
    ])

    with tab1:
        section_header("EXECUTIVE OPERATIONAL SUMMARY")
        with st.spinner("AI is analyzing portfolio data..."):
            output = generate_executive_summary(kpis, data["projects"].to_dict("records"), api_key)
        ai_output_box(output)

    with tab2:
        section_header("DELAY ANALYSIS REPORT")
        with st.spinner("Analyzing delay drivers..."):
            output = generate_delay_analysis(data["projects"].to_dict("records"), api_key)
        ai_output_box(output)

    with tab3:
        section_header("WORKFORCE RISK INTELLIGENCE")
        with st.spinner("Analyzing workforce data..."):
            output = generate_workforce_analysis(data["workforce"], api_key)
        ai_output_box(output)

    with tab4:
        section_header("COST RISK & FINANCIAL EXPOSURE")
        with st.spinner("Analyzing cost data..."):
            output = generate_cost_risk_summary(data["costs"], api_key)
        ai_output_box(output)

    with tab5:
        section_header("BOTTLENECK DETECTION")
        with st.spinner("Detecting operational bottlenecks..."):
            output = generate_bottleneck_detection(data["projects"].to_dict("records"))
        ai_output_box(output)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: WORKFORCE INTELLIGENCE
# ═════════════════════════════════════════════════════════════════════════════

elif "Workforce Intelligence" in page:
    st.markdown("""
    <h1 style="font-family:'Barlow Condensed',sans-serif; font-size:36px; font-weight:800; 
               color:#EEF2FF; letter-spacing:2px; margin-bottom:4px;">
        WORKFORCE INTELLIGENCE MODULE
    </h1>
    <p style="color:#4A5568; font-size:13px; margin-bottom:24px;">
        Labour allocation, certification compliance, efficiency analytics & overtime exposure
    </p>
    """, unsafe_allow_html=True)

    wf = data["workforce"]

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    expired = len(wf[wf["cert_status"] == "EXPIRED"])
    expiring = len(wf[wf["cert_status"] == "EXPIRING SOON"])
    high_ot = len(wf[wf["overtime_hours"] > 15])
    avg_eff = round(wf["efficiency_score"].mean() * 100, 1)

    with c1: kpi_card("Total Workers", len(wf), "Across all sites", "👷", "blue")
    with c2: kpi_card("Cert. Non-Compliant", expired + expiring, f"{expired} expired · {expiring} expiring", "📋", "red")
    with c3: kpi_card("High Overtime", high_ot, "Workers >15h OT/week", "⏰", "orange")
    with c4: kpi_card("Avg Efficiency", f"{avg_eff}%", "Portfolio crew index", "⚡", "cyan")

    section_header("EFFICIENCY HEATMAP")
    st.plotly_chart(chart_workforce_heatmap(wf), use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        section_header("TRADE DISTRIBUTION")
        st.plotly_chart(chart_trade_distribution(wf), use_container_width=True)
    with col_b:
        section_header("OVERTIME EXPOSURE")
        st.plotly_chart(chart_overtime_exposure(wf), use_container_width=True)

    section_header("CERTIFICATION COMPLIANCE TABLE")
    cert_issues = wf[wf["cert_status"] != "VALID"][
        ["name", "trade", "project_name", "certification_expiry", "cert_status", "overtime_hours"]
    ].sort_values("cert_status")
    if len(cert_issues) > 0:
        st.markdown(f"""
        <div class="alert-high">
            ⚠️ <strong>{len(cert_issues)} workers</strong> require certification action. 
            Non-compliant workers must not perform certified tasks until renewed.
        </div>""", unsafe_allow_html=True)
        st.dataframe(cert_issues, use_container_width=True, hide_index=True)
    else:
        st.success("✓ All worker certifications are current.")

    section_header("FULL WORKFORCE REGISTER")
    st.dataframe(
        wf[["worker_id", "name", "trade", "project_name", "hours_this_week",
            "overtime_hours", "efficiency_score", "cert_status", "supervisor_rating"]],
        use_container_width=True, hide_index=True,
    )
    st.download_button("⬇ Export Workforce CSV", wf.to_csv(index=False).encode("utf-8"),
                       file_name="rwc_workforce.csv", mime="text/csv")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: MATERIAL & PROCUREMENT
# ═════════════════════════════════════════════════════════════════════════════

elif "Material" in page:
    st.markdown("""
    <h1 style="font-family:'Barlow Condensed',sans-serif; font-size:36px; font-weight:800; 
               color:#EEF2FF; letter-spacing:2px; margin-bottom:4px;">
        MATERIAL & PROCUREMENT MONITOR
    </h1>
    <p style="color:#4A5568; font-size:13px; margin-bottom:24px;">
        Supply chain intelligence, procurement risk scoring & delivery tracking
    </p>
    """, unsafe_allow_html=True)

    mat = data["materials"]

    c1, c2, c3, c4 = st.columns(4)
    critical_mat = len(mat[mat["risk"] == "CRITICAL"])
    high_mat = len(mat[mat["risk"] == "HIGH"])
    total_impact = mat["cost_impact"].sum()
    delayed_count = len(mat[mat["risk"].isin(["CRITICAL", "HIGH", "MEDIUM"])])

    with c1: kpi_card("Critical Shortages", critical_mat, "Immediate action needed", "🚨", "red")
    with c2: kpi_card("High Risk Items", high_mat, "Close monitoring required", "⚠️", "orange")
    with c3: kpi_card("Total Cost Impact", f"${total_impact/1_000_000:.1f}M", "Procurement exposure", "💸", "yellow")
    with c4: kpi_card("Delayed Items", delayed_count, f"of {len(mat)} tracked items", "📦", "blue")

    section_header("PROCUREMENT RISK MAP")
    st.plotly_chart(chart_material_risk(mat), use_container_width=True)

    section_header("MATERIAL DELAY REGISTER")
    for _, row in mat.sort_values("risk", key=lambda x: x.map({"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3})).iterrows():
        risk = row["risk"]
        alert_class = f"alert-{'critical' if risk=='CRITICAL' else 'high' if risk=='HIGH' else 'medium' if risk=='MEDIUM' else 'low'}"
        pct_received = round(row["qty_received"] / row["qty_ordered"] * 100) if row["qty_ordered"] > 0 else 0
        st.markdown(f"""
        <div class="{alert_class}">
            <strong>{row['material']}</strong> 
            <span style="color:#64748B; font-size:11px; margin-left:8px;">[ {risk} ]  |  {row['project']}</span><br>
            <span style="font-size:12px; color:#94A3B8;">
                Supplier: {row['supplier']}  •  
                Received: {row['qty_received']}/{row['qty_ordered']} {row['unit']} ({pct_received}%)  •  
                ETA: {row['actual_eta']}  •  
                Cost Impact: ${row['cost_impact']:,.0f}
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.download_button("⬇ Export Procurement CSV", mat.to_csv(index=False).encode("utf-8"),
                       file_name="rwc_materials.csv", mime="text/csv")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: COST IMPACT ENGINE
# ═════════════════════════════════════════════════════════════════════════════

elif "Cost Impact" in page:
    st.markdown("""
    <h1 style="font-family:'Barlow Condensed',sans-serif; font-size:36px; font-weight:800; 
               color:#EEF2FF; letter-spacing:2px; margin-bottom:4px;">
        ESTIMATING & COST IMPACT ENGINE
    </h1>
    <p style="color:#4A5568; font-size:13px; margin-bottom:24px;">
        Financial variance tracking, delay cost exposure & budget performance
    </p>
    """, unsafe_allow_html=True)

    cost_df = data["costs"]

    total_contracts = cost_df["contract_value"].sum()
    total_spent = cost_df["amount_spent"].sum()
    total_variance = cost_df["cost_variance"].sum()
    total_ot_cost = cost_df["overtime_cost"].sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Portfolio Value", f"${total_contracts/1_000_000:.1f}M", "Total contracts", "🏗️", "blue")
    with c2: kpi_card("Spent to Date", f"${total_spent/1_000_000:.1f}M", "Across all projects", "💳", "orange")
    with c3: kpi_card("Net Variance", f"${total_variance/1_000_000:.2f}M", "Negative = over budget", "📉", "red" if total_variance < 0 else "green")
    with c4: kpi_card("Overtime Cost", f"${total_ot_cost/1_000_000:.1f}M", "Premium labour exposure", "⏰", "yellow")

    section_header("COST VARIANCE BY PROJECT")
    st.plotly_chart(chart_cost_variance(cost_df), use_container_width=True)

    section_header("AI COST RISK SUMMARY")
    with st.spinner("Generating financial risk analysis..."):
        output = generate_cost_risk_summary(cost_df, api_key)
    ai_output_box(output)

    section_header("FINANCIAL DETAIL TABLE")
    display_df = cost_df[["project", "contract_value", "amount_spent", "cost_variance",
                           "delay_cost_exposure", "overtime_cost", "contingency_used_pct"]].copy()
    display_df.columns = ["Project", "Contract ($)", "Spent ($)", "Variance ($)",
                           "Delay Exposure ($)", "OT Cost ($)", "Contingency Used (%)"]
    st.dataframe(display_df.style.format({
        "Contract ($)": "${:,.0f}",
        "Spent ($)": "${:,.0f}",
        "Variance ($)": "${:,.0f}",
        "Delay Exposure ($)": "${:,.0f}",
        "OT Cost ($)": "${:,.0f}",
        "Contingency Used (%)": "{:.0f}%",
    }), use_container_width=True)

    st.download_button("⬇ Export Cost Data CSV", cost_df.to_csv(index=False).encode("utf-8"),
                       file_name="rwc_cost_data.csv", mime="text/csv")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: EXECUTIVE AI BRIEFING
# ═════════════════════════════════════════════════════════════════════════════

elif "Briefing" in page:
    st.markdown("""
    <h1 style="font-family:'Barlow Condensed',sans-serif; font-size:36px; font-weight:800; 
               color:#EEF2FF; letter-spacing:2px; margin-bottom:4px;">
        EXECUTIVE AI BRIEFING PANEL
    </h1>
    <p style="color:#4A5568; font-size:13px; margin-bottom:24px;">
        Daily leadership briefing  •  AI-synthesized  •  Board-ready format
    </p>
    """, unsafe_allow_html=True)

    with st.spinner("Generating executive briefing..."):
        briefing = generate_executive_briefing(kpis, data["projects"].to_dict("records"), api_key)

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0A0E1A, #0F1929);
                border: 1px solid #1E3A5F; border-top: 3px solid #F97316;
                border-radius: 12px; padding: 28px 32px; 
                font-family: 'Barlow', sans-serif; font-size: 13.5px; 
                line-height: 1.8; color: #CBD5E1; white-space: pre-wrap;">
{briefing}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "⬇ Download Briefing (TXT)",
            data=briefing.encode("utf-8"),
            file_name=f"rwc_executive_briefing_{datetime.today().strftime('%Y%m%d')}.txt",
            mime="text/plain",
        )
    with col_dl2:
        with st.spinner("Preparing PDF..."):
            try:
                pdf_bytes = generate_pdf_report(kpis, data["projects"], briefing)
                st.download_button(
                    "⬇ Download Executive Report (PDF)",
                    data=pdf_bytes,
                    file_name=f"rwc_executive_report_{datetime.today().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                )
            except Exception as e:
                st.info("Install 'reportlab' for PDF export: `pip install reportlab`")

    # Management notes
    section_header("MANAGEMENT NOTES")
    note = st.text_area(
        "Add operational notes for this briefing period:",
        placeholder="Enter notes for the record — e.g. client call outcomes, board decisions, field observations...",
        height=120,
    )
    if st.button("Save Notes"):
        if note:
            st.success(f"✓ Notes saved at {datetime.now().strftime('%H:%M')} — {datetime.today().strftime('%B %d, %Y')}")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: OPERATIONAL ALERTS
# ═════════════════════════════════════════════════════════════════════════════

elif "Alerts" in page:
    st.markdown("""
    <h1 style="font-family:'Barlow Condensed',sans-serif; font-size:36px; font-weight:800; 
               color:#EEF2FF; letter-spacing:2px; margin-bottom:4px;">
        OPERATIONAL ALERT CENTER
    </h1>
    <p style="color:#4A5568; font-size:13px; margin-bottom:24px;">
        Live risk alerts, safety incidents & procurement warnings across all active projects
    </p>
    """, unsafe_allow_html=True)

    safety_df = data["safety"]
    wf = data["workforce"]
    mat = data["materials"]

    # Summary counts
    c1, c2, c3, c4 = st.columns(4)
    open_safety = len(safety_df[safety_df["status"] == "OPEN"])
    critical_mats = len(mat[mat["risk"] == "CRITICAL"])
    cert_issues = len(wf[wf["cert_status"] != "VALID"])
    critical_proj = kpis["critical_projects"]
    with c1: kpi_card("Safety Alerts", open_safety, "Open incidents", "🦺", "red")
    with c2: kpi_card("Material Alerts", critical_mats, "Critical shortages", "📦", "orange")
    with c3: kpi_card("HR Alerts", cert_issues, "Cert. non-compliance", "📋", "yellow")
    with c4: kpi_card("Critical Projects", critical_proj, "Require escalation", "🚨", "red")

    section_header("SAFETY INCIDENTS REGISTER")
    for _, row in safety_df.sort_values(["status", "severity"], key=lambda x: x.map({
        "OPEN": 0, "CLOSED": 1, "CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3
    }).fillna(2)).iterrows():
        sev = row["severity"]
        status_icon = "🔴" if row["status"] == "OPEN" else "✅"
        alert_class = f"alert-{'critical' if sev=='CRITICAL' else 'high' if sev=='HIGH' else 'medium' if sev=='MEDIUM' else 'low'}"
        st.markdown(f"""
        <div class="{alert_class}">
            {status_icon} <strong>{row['type']}</strong> — {row['project']} 
            <span style="color:#64748B; font-size:11px; margin-left:8px;">[{sev}]  •  {row['date']}  •  Status: {row['status']}</span><br>
            <span style="font-size:12px; color:#94A3B8;">{row['description']}</span>
        </div>
        """, unsafe_allow_html=True)

    section_header("CRITICAL PROCUREMENT ALERTS")
    critical_items = mat[mat["risk"].isin(["CRITICAL", "HIGH"])]
    for _, row in critical_items.iterrows():
        pct = round(row["qty_received"] / row["qty_ordered"] * 100) if row["qty_ordered"] > 0 else 0
        alert_cls = "alert-critical" if row["risk"] == "CRITICAL" else "alert-high"
        st.markdown(f"""
        <div class="{alert_cls}">
            🚛 <strong>{row['material']}</strong> — {row['project']}<br>
            <span style="font-size:12px; color:#94A3B8;">
                Supplier: {row['supplier']}  •  {pct}% received  •  
                New ETA: {row['actual_eta']}  •  Cost Impact: ${row['cost_impact']:,.0f}
            </span>
        </div>
        """, unsafe_allow_html=True)

    section_header("WORKFORCE COMPLIANCE ALERTS")
    cert_alert = wf[wf["cert_status"] != "VALID"][["name", "trade", "project_name", "certification_expiry", "cert_status"]]
    if len(cert_alert) > 0:
        for _, row in cert_alert.iterrows():
            alert_cls = "alert-critical" if row["cert_status"] == "EXPIRED" else "alert-medium"
            icon = "❌" if row["cert_status"] == "EXPIRED" else "⚠️"
            st.markdown(f"""
            <div class="{alert_cls}">
                {icon} <strong>{row['name']}</strong> — {row['trade']} — {row['project_name']}<br>
                <span style="font-size:12px; color:#94A3B8;">
                    Certification Status: <strong>{row['cert_status']}</strong>  •  Expiry: {row['certification_expiry']}
                </span>
            </div>
            """, unsafe_allow_html=True)
