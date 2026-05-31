"""
RWC Operations Intelligence Platform
AI Analysis Engine — OpenAI-compatible with intelligent mock fallback
"""

import os
import random
from datetime import datetime


# ─────────────────────────────────────────────
# MOCK AI OUTPUTS — Highly Realistic
# ─────────────────────────────────────────────

def _mock_executive_summary(kpis: dict, projects: list) -> str:
    date_str = datetime.today().strftime("%B %d, %Y")
    critical = [p for p in projects if p.get("status") == "CRITICAL"]
    at_risk = [p for p in projects if p.get("status") == "AT RISK"]
    on_track = [p for p in projects if p.get("status") == "ON TRACK"]

    critical_str = ", ".join([p["name"] for p in critical]) if critical else "none at this time"
    risk_str = ", ".join([p["name"] for p in at_risk]) if at_risk else "none"

    return f"""**RWC OPERATIONAL SUMMARY — {date_str}**

RWC's active portfolio is currently operating under **elevated risk conditions** across {kpis['active_projects']} concurrent projects, with a combined contract value exceeding ${kpis['total_contract_value']:,.0f}. The overall Operational Efficiency Score stands at **{kpis['efficiency_score']}/100**, reflecting the compound pressure of material procurement disruptions, workforce overtime exposure, and critical-path schedule slippage on two flagship projects.

**Critical Attention Required:** {critical_str.title()} is flagged as CRITICAL status and requires immediate executive intervention. Schedule recovery plans have not yet been formalized, and cost exposure is escalating.

**At-Risk Projects:** {risk_str.title()} — each project has active mitigation measures in place but warrants continued senior oversight.

**Positive Indicators:** {len(on_track)} project(s) are tracking on schedule and within budget. The Queensway Transit Depot represents a model execution, currently 6 days ahead of schedule with a projected under-run of approximately $450,000.

**Immediate Priorities:** Resolve medical-grade HVAC supply chain obstruction at Northgate Medical Centre; convene supplier recovery meeting for structural steel at Meridian Heights; and deploy additional QA supervision to address RFI backlog (currently {sum(p.get('open_rfi', 0) for p in projects)} open items portfolio-wide).
"""


def _mock_delay_analysis(projects: list) -> str:
    delayed = [p for p in projects if p.get("active_delays", 0) > 0]
    total_delays = sum(p.get("active_delays", 0) for p in delayed)

    return f"""**DELAY ANALYSIS REPORT**

A total of **{total_delays} active delay events** have been identified across {len(delayed)} project(s). The primary delay drivers, in order of schedule impact, are as follows:

**1. Material Procurement Disruptions (Primary Driver — 52% of delay exposure)**
Medical-grade HVAC equipment at Northgate Medical Centre remains the most consequential single delay event in the portfolio. The 5.5-month supply gap has shifted the critical path and is generating cascading impacts across MEP rough-in sequencing. Structural steel delays at Meridian Heights Tower represent the second-largest procurement failure, with downstream effects on curtain wall installation and elevator shaft completion.

**2. Design/RFI Backlog (Secondary Driver — 28% of delay exposure)**
The Northgate Medical Centre RFI log stands at 31 open items — an unusually high volume for this stage of construction. Unresolved design coordination questions are preventing trade contractors from proceeding on three critical work zones. Recommend immediate design-build team workshop to clear backlog within 10 business days.

**3. Quality & Rework Events (Tertiary Driver — 20% of delay exposure)**
Elevator shaft rework at Meridian Heights Tower, triggered by a failed QA inspection, has introduced approximately 18 working days of re-sequencing. Implement pre-pour and pre-close inspection checklists to prevent recurrence.

**Projected Portfolio Schedule Impact:** Current delay profile is estimated to extend overall portfolio delivery by an average of **11.3 weeks** across affected projects, with an associated cost exposure of **$5.8M–$7.2M** if uncorrected.
"""


def _mock_workforce_analysis(workforce_df) -> str:
    expiring = len(workforce_df[workforce_df["cert_status"].isin(["EXPIRED", "EXPIRING SOON"])])
    overtime = workforce_df[workforce_df["overtime_hours"] > 10]
    avg_efficiency = workforce_df["efficiency_score"].mean()

    return f"""**WORKFORCE RISK INTELLIGENCE REPORT**

The current field workforce totals **{len(workforce_df)} tracked personnel** across {workforce_df['project_name'].nunique()} active project sites. Analysis of workforce data reveals several operational risk indicators that require management attention.

**Certification Compliance Risk — HIGH**
{expiring} workers have certifications that are expired or expiring within 60 days. This represents a **{round(expiring/len(workforce_df)*100, 1)}% compliance exposure**. Workers operating under expired certifications create legal liability and insurability risk. Recommend immediate outreach to affected workers and scheduling of renewal training blocks. Non-compliant workers should be reassigned to non-certification-required tasks pending renewal.

**Overtime Exposure — ELEVATED**
{len(overtime)} workers are logging more than 10 hours of overtime per week. Extended overtime cycles correlate strongly with fatigue-related safety incidents and reduced productivity efficiency (typically 15–25% output degradation after the 55-hour threshold). Current overtime patterns suggest possible labour undersupply on the Northgate Medical Centre and Meridian Heights Tower sites.

**Efficiency Index — {round(avg_efficiency * 100, 1)}%**
Portfolio-wide crew efficiency is rated at {round(avg_efficiency * 100, 1)}% — slightly below the RWC target threshold of 82%. The lowest-performing trade segments are concentrated in specialty MEP crews, likely reflecting coordination issues caused by the RFI backlog and incomplete design documentation.

**Recommendation:** Deploy a workforce rebalancing exercise — specifically reallocating 15–20 labour units from Queensway Transit Depot (nearing completion) to Northgate Medical Centre to address critical-path labour shortfalls.
"""


def _mock_executive_briefing(kpis: dict, projects: list) -> str:
    date_str = datetime.today().strftime("%A, %B %d, %Y")
    return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**RWC CONSTRUCTION MANAGEMENT GROUP**
**DAILY EXECUTIVE OPERATIONS BRIEFING**
**Prepared for: Senior Leadership & Board of Directors**
**Date: {date_str} | Classification: Internal — Confidential**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**OPERATIONAL HEALTH SUMMARY**
Overall portfolio health is rated **{kpis['avg_health_score']}/100** — classified as GUARDED. Two of six active projects are operating under elevated risk conditions. The company's aggregate cost exposure from current delay and variance events is estimated at **${kpis['cost_exposure']:,.0f}**, with the largest single driver being the Northgate Medical Centre procurement failure.

**TOP OPERATIONAL RISKS (Ranked by Impact)**
1. 🔴 **Northgate Medical Centre** — Critical supply chain failure (medical HVAC). Schedule slippage of 5.5+ months. Estimated cost impact: $1.2M–$2.8M. Client relations at risk.
2. 🟠 **Meridian Heights Tower** — Structural steel delay + elevator shaft rework. 3 active delays. Confidence rating: 61%. Overtime crews deployed.
3. 🟡 **Harborfront Logistics Hub** — Roofing membrane and dock leveler procurement 3 weeks behind. Minor but monitored.

**PROJECT HIGHLIGHTS**
✅ Queensway Transit Depot: 92% complete — ahead of schedule, under budget. Prepare client acceptance package.
✅ Cascade Business Park Ph.2: 84% complete — no active delays. Final MEP inspections pending.
🟡 Summit Ridge Condominiums: 22% complete — early-stage, one minor safety incident closed.

**WORKFORCE OBSERVATIONS**
Total deployed workforce: **{kpis['total_workforce']} personnel**. Utilization at {kpis['workforce_utilization']}%. Certification compliance review required. Overtime exposure elevated at Northgate and Meridian sites.

**SAFETY OBSERVATIONS**
{kpis['open_safety_risks']} open safety items across the portfolio. One equipment incident at Northgate Medical Centre (scissor lift proximity event) remains under investigation. Zero lost-time injuries this reporting period.

**STRATEGIC RECOMMENDATIONS FOR LEADERSHIP**
1. Authorize emergency procurement escalation for Northgate HVAC — explore alternative North American suppliers immediately.
2. Schedule client communication meeting with Regional Health Authority regarding revised schedule and recovery plan.
3. Review contingency drawdown authority for Meridian Heights — current trajectory suggests contingency will be exhausted by Q1 2025.
4. Initiate workforce rebalancing study to redeploy Queensway resources to Northgate upon depot project closeout.
5. Commission independent QA audit of Northgate design documentation to clear RFI backlog.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
*Briefing prepared by RWC Operations Intelligence Platform | AI-Assisted Analysis*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def _mock_cost_risk_summary(cost_df) -> str:
    total_exposure = abs(cost_df["cost_variance"].sum())
    return f"""**COST RISK & FINANCIAL EXPOSURE ANALYSIS**

The current portfolio presents a **negative cost variance of ${total_exposure:,.0f}** against contract baselines. This figure is expected to grow if material procurement and schedule delay events are not resolved within the next 30–45 days.

**Key Financial Risk Drivers:**

**Labour Cost Overrun (Overtime Premium):** Extended overtime deployment at Meridian Heights and Northgate Medical Centre is generating an estimated **$485,000–$720,000** in unbudgeted premium labour costs. If overtime continues at current rates through Q1 2025, this figure may reach $1.1M portfolio-wide.

**Material Delay Cost Exposure:** Supply chain disruptions are generating both direct cost impacts (expediting fees, alternative sourcing premiums) and indirect costs (idle labour, extended equipment rentals, acceleration of follow-on trades). Combined material-related cost exposure is estimated at **$2.1M–$3.4M**.

**Rework and Quality Events:** Elevator shaft rework at Meridian Heights is estimated at $215,000 in direct rework costs plus an additional $180,000 in trade contractor re-sequencing. Enhanced QA checkpoints have been implemented to prevent recurrence.

**Contingency Status:** Three projects have consumed more than 50% of their allocated contingency reserves. The Northgate Medical Centre contingency is projected to be exhausted within 60 days at the current burn rate. A supplemental contingency request should be prepared for board review.

**Positive Offset:** Queensway Transit Depot projects an under-run of approximately $450,000, and Cascade Business Park Phase 2 is $180,000 favourable — partially offsetting portfolio-wide exposure.
"""


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def generate_executive_summary(kpis: dict, projects: list, api_key: str = None) -> str:
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            prompt = f"""You are the Chief Operations Analyst for RWC Construction Management Group.
Generate a professional executive operational summary based on this data:
KPIs: {kpis}
Projects: {[{k: v for k, v in p.items() if k in ['name','status','progress','schedule_risk','active_delays','health_score']} for p in projects]}
Write in a professional, senior executive tone. Be specific and data-driven. 3-4 paragraphs."""
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
            )
            return response.choices[0].message.content
        except Exception:
            pass
    return _mock_executive_summary(kpis, projects)


def generate_delay_analysis(projects: list, api_key: str = None) -> str:
    return _mock_delay_analysis(projects)


def generate_workforce_analysis(workforce_df, api_key: str = None) -> str:
    return _mock_workforce_analysis(workforce_df)


def generate_executive_briefing(kpis: dict, projects: list, api_key: str = None) -> str:
    return _mock_executive_briefing(kpis, projects)


def generate_cost_risk_summary(cost_df, api_key: str = None) -> str:
    return _mock_cost_risk_summary(cost_df)


def generate_bottleneck_detection(projects: list) -> str:
    return """**OPERATIONAL BOTTLENECK DETECTION — AI ANALYSIS**

The following systemic bottlenecks have been identified through pattern analysis of current project data:

**Bottleneck #1: Specialty Equipment Procurement Lead Times**
Three separate projects are experiencing delays attributable to long-lead specialty equipment (medical HVAC, elevators, switchgear). RWC's procurement workflows are not currently structured to account for 12–18 month lead times on mission-critical items. Recommendation: Implement a "critical procurement calendar" tied to project scheduling software, with automatic procurement trigger dates set 20% earlier than current practice.

**Bottleneck #2: RFI Resolution Velocity**
The portfolio-wide RFI backlog has grown 340% in the past 90 days, concentrated at Northgate Medical Centre. Slow design team response is blocking multiple trade packages. Recommendation: Establish a 72-hour RFI response SLA with contractual remedies for non-compliance.

**Bottleneck #3: Workforce Certification Administration**
Certification tracking is reactive rather than predictive. The current compliance gap (12+ workers with expired or near-expiry certifications) has created a scheduling risk where affected workers may need to be pulled from site without notice. Recommendation: Implement a 90-day advance notification system and pre-book renewal training automatically.

**Bottleneck #4: Quality Assurance Gate Sequencing**
Two rework events this period indicate insufficient pre-close QA checkpoints. Installing milestone-based inspection gates (rather than phase-end inspections) would detect deficiencies earlier and reduce rework costs by an estimated 40–60%.
"""


def score_project_risk(project: dict) -> dict:
    """AI-style risk scoring for a single project."""
    score = 100
    factors = []

    if project.get("schedule_risk") == "CRITICAL":
        score -= 35
        factors.append("Critical schedule risk (-35)")
    elif project.get("schedule_risk") == "HIGH":
        score -= 20
        factors.append("High schedule risk (-20)")
    elif project.get("schedule_risk") == "MEDIUM":
        score -= 10
        factors.append("Medium schedule risk (-10)")

    if project.get("material_status") == "CRITICAL SHORTAGE":
        score -= 25
        factors.append("Critical material shortage (-25)")
    elif project.get("material_status") == "DELAYED":
        score -= 12
        factors.append("Material delays (-12)")

    delays = project.get("active_delays", 0)
    if delays > 4:
        score -= 15
    elif delays > 1:
        score -= 8
    elif delays > 0:
        score -= 3
    if delays > 0:
        factors.append(f"{delays} active delays (-{min(15, delays * 3)})")

    rfi = project.get("open_rfi", 0)
    if rfi > 20:
        score -= 10
        factors.append(f"High RFI backlog: {rfi} open (-10)")
    elif rfi > 10:
        score -= 5

    safety = project.get("safety_incidents", 0)
    if safety >= 3:
        score -= 10
        factors.append(f"{safety} safety incidents (-10)")
    elif safety > 0:
        score -= 4

    score = max(0, min(100, score))
    return {
        "score": score,
        "grade": "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "D" if score >= 40 else "F",
        "factors": factors,
        "recommendation": (
            "No action required — maintain current oversight cadence." if score >= 85 else
            "Monitor closely — schedule weekly status reviews." if score >= 70 else
            "Intervention recommended — assign senior PM oversight." if score >= 55 else
            "Urgent escalation required — executive attention needed." if score >= 40 else
            "CRITICAL — immediate executive intervention and recovery plan activation."
        )
    }
