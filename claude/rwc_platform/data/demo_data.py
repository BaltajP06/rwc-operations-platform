"""
RWC Operations Intelligence Platform
Demo Data Generator — Realistic Commercial Construction Data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# ─────────────────────────────────────────────
# PROJECT DATA
# ─────────────────────────────────────────────

PROJECTS = [
    {
        "id": "RWC-2024-001",
        "name": "Meridian Heights Tower",
        "client": "Meridian Development Corp",
        "type": "High-Rise Residential",
        "supervisor": "Daniel Hartley",
        "trade": "Structural / MEP",
        "location": "Downtown Core — Block 14",
        "contract_value": 48_500_000,
        "progress": 67,
        "schedule_risk": "HIGH",
        "material_status": "DELAYED",
        "workforce_count": 142,
        "active_delays": 3,
        "confidence": 61,
        "start_date": "2023-09-01",
        "planned_end": "2025-03-15",
        "revised_end": "2025-06-20",
        "safety_incidents": 2,
        "open_rfi": 14,
        "change_orders": 7,
        "cost_variance": -1_250_000,
        "status": "AT RISK",
        "health_score": 54,
        "notes": "Structural steel delivery from supplier delayed 6 weeks. Elevator shaft rework required after QA inspection failure. Overtime crews deployed.",
    },
    {
        "id": "RWC-2024-002",
        "name": "Cascade Business Park — Phase 2",
        "client": "Briarwood Holdings Ltd",
        "type": "Commercial Office",
        "supervisor": "Sandra Voss",
        "trade": "Civil / Concrete",
        "location": "Eastside Business District",
        "contract_value": 22_750_000,
        "progress": 84,
        "schedule_risk": "LOW",
        "material_status": "ON TRACK",
        "workforce_count": 78,
        "active_delays": 0,
        "confidence": 91,
        "start_date": "2024-01-10",
        "planned_end": "2024-12-31",
        "revised_end": "2024-12-31",
        "safety_incidents": 0,
        "open_rfi": 3,
        "change_orders": 2,
        "cost_variance": 180_000,
        "status": "ON TRACK",
        "health_score": 89,
        "notes": "Project tracking ahead of schedule on concrete pours. Awaiting final MEP inspections. Client satisfaction high.",
    },
    {
        "id": "RWC-2024-003",
        "name": "Northgate Medical Centre",
        "client": "Regional Health Authority",
        "type": "Healthcare Facility",
        "supervisor": "Marcus Webb",
        "trade": "MEP / Specialty Systems",
        "location": "Northgate Medical Campus",
        "contract_value": 61_200_000,
        "progress": 38,
        "schedule_risk": "CRITICAL",
        "material_status": "CRITICAL SHORTAGE",
        "workforce_count": 201,
        "active_delays": 6,
        "confidence": 41,
        "start_date": "2024-03-01",
        "planned_end": "2026-01-30",
        "revised_end": "2026-07-15",
        "safety_incidents": 3,
        "open_rfi": 31,
        "change_orders": 19,
        "cost_variance": -3_800_000,
        "status": "CRITICAL",
        "health_score": 32,
        "notes": "Medical-grade HVAC system backordered. Infection control specialist flagged 3 corridor layout issues requiring redesign. Critical path shifted 6 months.",
    },
    {
        "id": "RWC-2024-004",
        "name": "Harborfront Logistics Hub",
        "client": "Pacific Freight Solutions Inc.",
        "type": "Industrial / Warehouse",
        "supervisor": "Tina Okafor",
        "trade": "Steel / Mechanical",
        "location": "Port Industrial Zone",
        "contract_value": 17_400_000,
        "progress": 55,
        "schedule_risk": "MEDIUM",
        "material_status": "PARTIAL DELAY",
        "workforce_count": 63,
        "active_delays": 1,
        "confidence": 74,
        "start_date": "2024-02-15",
        "planned_end": "2024-11-30",
        "revised_end": "2025-01-15",
        "safety_incidents": 1,
        "open_rfi": 8,
        "change_orders": 4,
        "cost_variance": -320_000,
        "status": "MONITORING",
        "health_score": 68,
        "notes": "Crane rental conflict with adjacent project resolved. Dock leveler procurement delayed 3 weeks. Roof panels installation 2 weeks behind.",
    },
    {
        "id": "RWC-2023-089",
        "name": "Queensway Transit Depot",
        "client": "Metro Transit Commission",
        "type": "Transit Infrastructure",
        "supervisor": "Raymond Cho",
        "trade": "Civil / Electrical",
        "location": "Queensway Corridor",
        "contract_value": 35_900_000,
        "progress": 92,
        "schedule_risk": "LOW",
        "material_status": "ON TRACK",
        "workforce_count": 34,
        "active_delays": 0,
        "confidence": 96,
        "start_date": "2023-06-01",
        "planned_end": "2024-10-31",
        "revised_end": "2024-10-15",
        "safety_incidents": 0,
        "open_rfi": 1,
        "change_orders": 1,
        "cost_variance": 450_000,
        "status": "ON TRACK",
        "health_score": 95,
        "notes": "Commissioning phase underway. Final utility connections scheduled for Oct 8. Under budget by ~$450K. Client preparing acceptance documentation.",
    },
    {
        "id": "RWC-2024-005",
        "name": "Summit Ridge Condominiums",
        "client": "Summit Residential Partners",
        "type": "Mid-Rise Residential",
        "supervisor": "Priya Nair",
        "trade": "Concrete / Finishing",
        "location": "West End — Summit Road",
        "contract_value": 29_300_000,
        "progress": 22,
        "schedule_risk": "MEDIUM",
        "material_status": "ON TRACK",
        "workforce_count": 89,
        "active_delays": 1,
        "confidence": 78,
        "start_date": "2024-07-01",
        "planned_end": "2026-04-30",
        "revised_end": "2026-06-15",
        "safety_incidents": 1,
        "open_rfi": 11,
        "change_orders": 3,
        "cost_variance": -85_000,
        "status": "MONITORING",
        "health_score": 72,
        "notes": "Foundation pours complete. First floor framing underway. Slight delay in window system procurement. Safety incident (minor) — near-miss investigation closed.",
    },
]


def get_projects_df():
    return pd.DataFrame(PROJECTS)


# ─────────────────────────────────────────────
# WORKFORCE DATA
# ─────────────────────────────────────────────

TRADES = ["Ironworkers", "Electricians", "Pipefitters", "Carpenters", "Concrete Finishers",
          "Operating Engineers", "Labourers", "HVAC Technicians", "Glaziers", "Roofers"]


def get_workforce_df():
    rows = []
    project_ids = [p["id"] for p in PROJECTS]
    project_names = [p["name"] for p in PROJECTS]

    worker_names = [
        "Aleksei Volkov", "Maria Santos", "James Oduya", "Lin Wei", "Fatima Hassan",
        "Carlos Rivera", "Anna Bergström", "Samuel Osei", "Yuki Tanaka", "Ravi Patel",
        "Tom MacGregor", "Diane Fontaine", "Kwame Boateng", "Ingrid Larsen", "Hassan Al-Rashid",
        "Elena Petrov", "Marcus Johnson", "Soo-Jin Park", "Deepak Sharma", "Nadia Kowalski",
        "Peter O'Brien", "Amara Diallo", "Chen Xiaoming", "Olga Marchetti", "Theo Baxter",
        "Lucia Moreno", "Brendan Walsh", "Aiko Suzuki", "Kofi Mensah", "Svetlana Ivanova",
    ]

    for i, name in enumerate(worker_names):
        proj_idx = i % len(project_ids)
        cert_days = random.randint(-30, 365)
        cert_expiry = (datetime.today() + timedelta(days=cert_days)).strftime("%Y-%m-%d")
        rows.append({
            "worker_id": f"WRK-{1000 + i}",
            "name": name,
            "trade": random.choice(TRADES),
            "project_id": project_ids[proj_idx],
            "project_name": project_names[proj_idx],
            "hours_this_week": random.randint(30, 68),
            "overtime_hours": max(0, random.randint(-10, 20)),
            "efficiency_score": round(random.uniform(0.6, 1.0), 2),
            "certification_expiry": cert_expiry,
            "cert_status": "EXPIRED" if cert_days < 0 else ("EXPIRING SOON" if cert_days < 60 else "VALID"),
            "days_on_project": random.randint(10, 300),
            "supervisor_rating": round(random.uniform(3.0, 5.0), 1),
        })

    return pd.DataFrame(rows)


# ─────────────────────────────────────────────
# MATERIAL / PROCUREMENT DATA
# ─────────────────────────────────────────────

def get_materials_df():
    items = [
        {"material": "Structural Steel Beams (W-section)", "supplier": "NorthStar Steel Corp", "project": "Meridian Heights Tower", "ordered": "2024-06-01", "expected": "2024-07-15", "actual_eta": "2024-09-01", "qty_ordered": 320, "qty_received": 80, "unit": "tonnes", "risk": "CRITICAL", "cost_impact": 485000},
        {"material": "Medical-Grade HVAC Units", "supplier": "CleanAir Systems Ltd", "project": "Northgate Medical Centre", "ordered": "2024-04-10", "expected": "2024-07-01", "actual_eta": "2024-12-15", "qty_ordered": 24, "qty_received": 0, "unit": "units", "risk": "CRITICAL", "cost_impact": 1_200_000},
        {"material": "Electrical Switchgear Panels", "supplier": "Volt-Pro Industries", "project": "Northgate Medical Centre", "ordered": "2024-05-20", "expected": "2024-08-01", "actual_eta": "2024-10-30", "qty_ordered": 18, "qty_received": 6, "unit": "panels", "risk": "HIGH", "cost_impact": 320_000},
        {"material": "Precast Concrete Panels", "supplier": "Consolidated Precast Inc.", "project": "Harborfront Logistics Hub", "ordered": "2024-06-15", "expected": "2024-08-20", "actual_eta": "2024-09-10", "qty_ordered": 640, "qty_received": 500, "unit": "panels", "risk": "MEDIUM", "cost_impact": 95_000},
        {"material": "Curtain Wall Glazing System", "supplier": "PanGlass Solutions", "project": "Summit Ridge Condominiums", "ordered": "2024-07-01", "expected": "2024-10-01", "actual_eta": "2024-11-20", "qty_ordered": 2800, "qty_received": 0, "unit": "sqm", "risk": "MEDIUM", "cost_impact": 175_000},
        {"material": "Elevator Core Components", "supplier": "VertexLift International", "project": "Meridian Heights Tower", "ordered": "2024-03-01", "expected": "2024-06-01", "actual_eta": "2024-09-15", "qty_ordered": 4, "qty_received": 1, "unit": "systems", "risk": "HIGH", "cost_impact": 680_000},
        {"material": "Reinforcement Bar (Grade 500)", "supplier": "CanSteel Fabricators", "project": "Summit Ridge Condominiums", "ordered": "2024-07-10", "expected": "2024-08-01", "actual_eta": "2024-08-05", "qty_ordered": 185, "qty_received": 185, "unit": "tonnes", "risk": "LOW", "cost_impact": 0},
        {"material": "Roofing Membrane & Insulation", "supplier": "WeatherShield Materials", "project": "Harborfront Logistics Hub", "ordered": "2024-07-01", "expected": "2024-09-01", "actual_eta": "2024-09-22", "qty_ordered": 4200, "qty_received": 0, "unit": "sqm", "risk": "MEDIUM", "cost_impact": 55_000},
    ]
    return pd.DataFrame(items)


# ─────────────────────────────────────────────
# SAFETY / ALERTS DATA
# ─────────────────────────────────────────────

def get_safety_df():
    incidents = [
        {"date": "2024-08-14", "project": "Northgate Medical Centre", "type": "Near-Miss", "severity": "HIGH", "description": "Worker came within 1m of unsecured floor opening — L4 corridor. Barrier replaced.", "status": "CLOSED", "days_open": 0},
        {"date": "2024-08-20", "project": "Meridian Heights Tower", "type": "First Aid Injury", "severity": "MEDIUM", "description": "Laceration to hand — improper glove use. First aid administered on site.", "status": "CLOSED", "days_open": 0},
        {"date": "2024-09-02", "project": "Northgate Medical Centre", "type": "Equipment Incident", "severity": "HIGH", "description": "Scissor lift proximity alarm triggered near overhead utility. Operator retrained.", "status": "OPEN", "days_open": 12},
        {"date": "2024-09-10", "project": "Harborfront Logistics Hub", "type": "Near-Miss", "severity": "MEDIUM", "description": "Forklift near-miss with pedestrian in unmarked crossing zone.", "status": "OPEN", "days_open": 4},
        {"date": "2024-09-15", "project": "Meridian Heights Tower", "type": "Environmental", "severity": "LOW", "description": "Minor concrete washout into storm drain — contained and reported.", "status": "OPEN", "days_open": 1},
        {"date": "2024-09-18", "project": "Summit Ridge Condominiums", "type": "Near-Miss", "severity": "MEDIUM", "description": "Unsecured scaffolding component on Level 3 — corrected before shift start.", "status": "CLOSED", "days_open": 0},
    ]
    return pd.DataFrame(incidents)


# ─────────────────────────────────────────────
# COST / FINANCIAL DATA
# ─────────────────────────────────────────────

def get_cost_df():
    rows = []
    for p in PROJECTS:
        contract = p["contract_value"]
        spent = contract * (p["progress"] / 100) * random.uniform(0.95, 1.12)
        rows.append({
            "project": p["name"],
            "contract_value": contract,
            "amount_spent": round(spent),
            "projected_final": round(contract + abs(p["cost_variance"]) * random.uniform(0.8, 1.5) * (-1 if p["cost_variance"] < 0 else 1)),
            "cost_variance": p["cost_variance"],
            "delay_cost_exposure": abs(p["cost_variance"]) * random.uniform(0.5, 2.0),
            "overtime_cost": p["workforce_count"] * random.randint(200, 1200),
            "material_variance": abs(p["cost_variance"]) * random.uniform(0.1, 0.6),
            "contingency_used_pct": random.randint(10, 85),
        })
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────
# KPI SUMMARY
# ─────────────────────────────────────────────

def get_kpi_summary():
    df = get_projects_df()
    workforce_df = get_workforce_df()
    safety_df = get_safety_df()
    mat_df = get_materials_df()
    cost_df = get_cost_df()

    active_projects = len(df)
    delayed_projects = len(df[df["schedule_risk"].isin(["HIGH", "CRITICAL"])])
    total_workforce = df["workforce_count"].sum()
    max_workforce = total_workforce * 1.15
    workforce_utilization = round((total_workforce / max_workforce) * 100, 1)
    open_safety = len(safety_df[safety_df["status"] == "OPEN"])
    material_delays = len(mat_df[mat_df["risk"].isin(["HIGH", "CRITICAL"])])
    cost_exposure = abs(cost_df["cost_variance"].sum()) + cost_df["delay_cost_exposure"].sum()
    avg_health = df["health_score"].mean()
    efficiency_score = round(avg_health * 0.85 + random.uniform(-2, 2), 1)

    return {
        "active_projects": active_projects,
        "delayed_projects": delayed_projects,
        "workforce_utilization": workforce_utilization,
        "total_workforce": total_workforce,
        "open_safety_risks": open_safety,
        "material_delays": material_delays,
        "cost_exposure": round(cost_exposure),
        "efficiency_score": round(efficiency_score, 1),
        "avg_health_score": round(avg_health, 1),
        "total_contract_value": df["contract_value"].sum(),
        "critical_projects": len(df[df["status"] == "CRITICAL"]),
        "on_track_projects": len(df[df["status"] == "ON TRACK"]),
    }


# ─────────────────────────────────────────────
# TIMELINE DATA (Gantt-style)
# ─────────────────────────────────────────────

def get_timeline_df():
    rows = []
    for p in PROJECTS:
        rows.append({
            "Project": p["name"][:28] + ("…" if len(p["name"]) > 28 else ""),
            "Start": p["start_date"],
            "Planned End": p["planned_end"],
            "Revised End": p["revised_end"],
            "Progress": p["progress"],
            "Status": p["status"],
        })
    return pd.DataFrame(rows)
