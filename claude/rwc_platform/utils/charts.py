"""
RWC Operations Intelligence Platform
Chart & Visualization Utilities — Plotly-based premium charts
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# DESIGN TOKENS
# ─────────────────────────────────────────────

COLORS = {
    "bg_primary": "#0A0E1A",
    "bg_card": "#111827",
    "bg_surface": "#1A2235",
    "accent_orange": "#F97316",
    "accent_blue": "#3B82F6",
    "accent_cyan": "#06B6D4",
    "accent_green": "#10B981",
    "accent_yellow": "#F59E0B",
    "accent_red": "#EF4444",
    "accent_purple": "#8B5CF6",
    "text_primary": "#F1F5F9",
    "text_muted": "#64748B",
    "border": "#1E2D45",
}

RISK_COLORS = {
    "CRITICAL": "#EF4444",
    "HIGH": "#F97316",
    "MEDIUM": "#F59E0B",
    "LOW": "#10B981",
    "ON TRACK": "#10B981",
    "AT RISK": "#F97316",
    "MONITORING": "#F59E0B",
    "DELAYED": "#EF4444",
    "ON TRACK": "#10B981",
    "PARTIAL DELAY": "#F59E0B",
    "CRITICAL SHORTAGE": "#EF4444",
}

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="'Barlow', 'DM Sans', sans-serif", color=COLORS["text_primary"], size=12),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(
        bgcolor="rgba(17,24,39,0.8)",
        bordercolor=COLORS["border"],
        borderwidth=1,
    ),
    xaxis=dict(
        gridcolor="rgba(30,45,69,0.6)",
        zerolinecolor=COLORS["border"],
        tickfont=dict(color=COLORS["text_muted"]),
    ),
    yaxis=dict(
        gridcolor="rgba(30,45,69,0.6)",
        zerolinecolor=COLORS["border"],
        tickfont=dict(color=COLORS["text_muted"]),
    ),
)


# ─────────────────────────────────────────────
# PROJECT HEALTH CHART
# ─────────────────────────────────────────────

def chart_project_health(df: pd.DataFrame) -> go.Figure:
    colors = [RISK_COLORS.get(s, COLORS["accent_blue"]) for s in df["status"]]
    short_names = [n[:22] + "…" if len(n) > 22 else n for n in df["name"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["health_score"],
        y=short_names,
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(color="rgba(0,0,0,0)", width=0),
            opacity=0.85,
        ),
        text=[f"{s}%" for s in df["health_score"]],
        textposition="inside",
        textfont=dict(color="white", size=11, family="Barlow"),
        hovertemplate="<b>%{y}</b><br>Health Score: %{x}/100<extra></extra>",
    ))

    layout = CHART_LAYOUT.copy()
    layout.update(dict(
        title=dict(text="Project Health Scores", font=dict(size=14, color=COLORS["text_primary"])),
        xaxis=dict(**CHART_LAYOUT["xaxis"], range=[0, 105], ticksuffix=""),
        height=280,
        margin=dict(l=180, r=20, t=40, b=20),
    ))
    fig.update_layout(**layout)
    return fig


# ─────────────────────────────────────────────
# PROGRESS CHART
# ─────────────────────────────────────────────

def chart_project_progress(df: pd.DataFrame) -> go.Figure:
    short_names = [n[:22] + "…" if len(n) > 22 else n for n in df["name"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=short_names,
        y=df["progress"],
        marker=dict(
            color=df["progress"],
            colorscale=[[0, COLORS["accent_red"]], [0.5, COLORS["accent_yellow"]], [1, COLORS["accent_cyan"]]],
            showscale=False,
            line=dict(color="rgba(0,0,0,0)"),
        ),
        text=[f"{p}%" for p in df["progress"]],
        textposition="outside",
        textfont=dict(color=COLORS["text_primary"], size=11),
        hovertemplate="<b>%{x}</b><br>Progress: %{y}%<extra></extra>",
    ))

    layout = CHART_LAYOUT.copy()
    layout.update(dict(
        title=dict(text="Project Completion Progress", font=dict(size=14, color=COLORS["text_primary"])),
        yaxis=dict(**CHART_LAYOUT["yaxis"], range=[0, 115], ticksuffix="%"),
        height=300,
    ))
    fig.update_layout(**layout)
    return fig


# ─────────────────────────────────────────────
# WORKFORCE HEATMAP
# ─────────────────────────────────────────────

def chart_workforce_heatmap(workforce_df: pd.DataFrame) -> go.Figure:
    pivot = workforce_df.groupby(["trade", "project_name"])["efficiency_score"].mean().unstack(fill_value=0)
    short_cols = [c[:18] + "…" if len(c) > 18 else c for c in pivot.columns]

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=short_cols,
        y=pivot.index.tolist(),
        colorscale=[
            [0.0, COLORS["accent_red"]],
            [0.4, COLORS["accent_yellow"]],
            [0.7, COLORS["accent_cyan"]],
            [1.0, COLORS["accent_green"]],
        ],
        zmin=0, zmax=1,
        text=[[f"{v:.0%}" for v in row] for row in pivot.values],
        texttemplate="%{text}",
        textfont=dict(size=10, color="white"),
        hovertemplate="Trade: %{y}<br>Project: %{x}<br>Efficiency: %{z:.1%}<extra></extra>",
        colorbar=dict(
            tickformat=".0%",
            tickfont=dict(color=COLORS["text_muted"]),
            title=dict(text="Efficiency", font=dict(color=COLORS["text_muted"])),
            bgcolor="rgba(0,0,0,0)",
        ),
    ))

    layout = CHART_LAYOUT.copy()
    layout.update(dict(
        title=dict(text="Workforce Efficiency by Trade & Project", font=dict(size=14, color=COLORS["text_primary"])),
        height=350,
        margin=dict(l=160, r=40, t=50, b=100),
        xaxis=dict(**CHART_LAYOUT["xaxis"], tickangle=-35),
    ))
    fig.update_layout(**layout)
    return fig


# ─────────────────────────────────────────────
# TRADE DISTRIBUTION DONUT
# ─────────────────────────────────────────────

def chart_trade_distribution(workforce_df: pd.DataFrame) -> go.Figure:
    trade_counts = workforce_df["trade"].value_counts()

    palette = [COLORS["accent_orange"], COLORS["accent_blue"], COLORS["accent_cyan"],
               COLORS["accent_green"], COLORS["accent_yellow"], COLORS["accent_red"],
               COLORS["accent_purple"], "#EC4899", "#14B8A6", "#6366F1"]

    fig = go.Figure(data=go.Pie(
        labels=trade_counts.index.tolist(),
        values=trade_counts.values.tolist(),
        hole=0.55,
        marker=dict(colors=palette[:len(trade_counts)], line=dict(color=COLORS["bg_primary"], width=2)),
        textfont=dict(size=11, color="white"),
        hovertemplate="<b>%{label}</b><br>Workers: %{value}<br>%{percent}<extra></extra>",
    ))

    fig.add_annotation(
        text=f"<b>{len(workforce_df)}</b><br>Workers",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color=COLORS["text_primary"]),
    )

    layout = CHART_LAYOUT.copy()
    layout.update(dict(
        title=dict(text="Trade Distribution", font=dict(size=14, color=COLORS["text_primary"])),
        height=320,
        showlegend=True,
        legend=dict(**CHART_LAYOUT["legend"], orientation="v", x=1.0, y=0.5),
    ))
    fig.update_layout(**layout)
    return fig


# ─────────────────────────────────────────────
# GANTT / TIMELINE CHART
# ─────────────────────────────────────────────

def chart_project_timeline(timeline_df: pd.DataFrame) -> go.Figure:
    status_colors = {
        "ON TRACK": COLORS["accent_green"],
        "MONITORING": COLORS["accent_yellow"],
        "AT RISK": COLORS["accent_orange"],
        "CRITICAL": COLORS["accent_red"],
    }

    fig = go.Figure()

    for _, row in timeline_df.iterrows():
        color = status_colors.get(row["Status"], COLORS["accent_blue"])
        start_offset = (pd.to_datetime(row["Start"]) - pd.to_datetime("2023-01-01")).days
        planned_days = (pd.to_datetime(row["Planned End"]) - pd.to_datetime(row["Start"])).days
        revised_days = (pd.to_datetime(row["Revised End"]) - pd.to_datetime(row["Start"])).days

        # Planned bar (solid)
        fig.add_trace(go.Bar(
            x=[planned_days],
            y=[row["Project"]],
            orientation="h",
            base=[start_offset],
            marker=dict(color=color, opacity=0.45, line=dict(color=color, width=2)),
            showlegend=False,
            hoverinfo="skip",
        ))
        # Revised bar (lighter, shows slippage)
        fig.add_trace(go.Bar(
            x=[revised_days],
            y=[row["Project"]],
            orientation="h",
            base=[start_offset],
            marker=dict(color=color, opacity=0.15, line=dict(color=color, width=1)),
            showlegend=False,
            hovertemplate=f"<b>{row['Project']}</b><br>Status: {row['Status']}<br>Progress: {row['Progress']}%<extra></extra>",
        ))

    layout = CHART_LAYOUT.copy()
    layout.update(dict(
        title=dict(text="Project Timeline Overview", font=dict(size=14, color=COLORS["text_primary"])),
        height=340,
        barmode="overlay",
        xaxis=dict(**CHART_LAYOUT["xaxis"], title="Days from Jan 2023"),
        margin=dict(l=200, r=20, t=50, b=30),
    ))
    fig.update_layout(**layout)
    return fig


# ─────────────────────────────────────────────
# COST VARIANCE CHART
# ─────────────────────────────────────────────

def chart_cost_variance(cost_df: pd.DataFrame) -> go.Figure:
    short_names = [n[:20] + "…" if len(n) > 20 else n for n in cost_df["project"]]
    colors = [COLORS["accent_green"] if v >= 0 else COLORS["accent_red"] for v in cost_df["cost_variance"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=short_names,
        y=cost_df["cost_variance"] / 1000,
        marker=dict(color=colors, opacity=0.85),
        text=[f"${v/1000:+,.0f}K" for v in cost_df["cost_variance"]],
        textposition="outside",
        textfont=dict(color=COLORS["text_primary"], size=10),
        hovertemplate="<b>%{x}</b><br>Cost Variance: $%{y:,.0f}K<extra></extra>",
    ))

    layout = CHART_LAYOUT.copy()
    layout.update(dict(
        title=dict(text="Cost Variance by Project ($000s)", font=dict(size=14, color=COLORS["text_primary"])),
        yaxis=dict(**CHART_LAYOUT["yaxis"], tickprefix="$", ticksuffix="K"),
        shapes=[dict(type="line", x0=-0.5, x1=len(cost_df)-0.5, y0=0, y1=0,
                     line=dict(color=COLORS["text_muted"], width=1, dash="dash"))],
        height=300,
    ))
    fig.update_layout(**layout)
    return fig


# ─────────────────────────────────────────────
# MATERIAL RISK BUBBLE CHART
# ─────────────────────────────────────────────

def chart_material_risk(mat_df: pd.DataFrame) -> go.Figure:
    risk_num = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
    mat_df = mat_df.copy()
    mat_df["risk_num"] = mat_df["risk"].map(risk_num).fillna(1)
    mat_df["short_material"] = mat_df["material"].apply(lambda x: x[:25] + "…" if len(x) > 25 else x)
    colors = [RISK_COLORS.get(r, COLORS["accent_blue"]) for r in mat_df["risk"]]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mat_df["cost_impact"] / 1000,
        y=mat_df["risk_num"],
        mode="markers+text",
        marker=dict(
            size=mat_df["cost_impact"] / 30000 + 12,
            color=colors,
            opacity=0.8,
            line=dict(color="white", width=1),
        ),
        text=mat_df["short_material"],
        textposition="top center",
        textfont=dict(size=9, color=COLORS["text_muted"]),
        hovertemplate="<b>%{text}</b><br>Cost Impact: $%{x:.0f}K<br>Risk Level: %{y}<extra></extra>",
    ))

    layout = CHART_LAYOUT.copy()
    layout.update(dict(
        title=dict(text="Material Procurement Risk Map", font=dict(size=14, color=COLORS["text_primary"])),
        xaxis=dict(**CHART_LAYOUT["xaxis"], title="Cost Impact ($000s)", tickprefix="$", ticksuffix="K"),
        yaxis=dict(**CHART_LAYOUT["yaxis"], tickvals=[1, 2, 3, 4], ticktext=["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
        height=350,
    ))
    fig.update_layout(**layout)
    return fig


# ─────────────────────────────────────────────
# OVERTIME EXPOSURE CHART
# ─────────────────────────────────────────────

def chart_overtime_exposure(workforce_df: pd.DataFrame) -> go.Figure:
    ot_by_project = workforce_df.groupby("project_name")["overtime_hours"].sum().reset_index()
    ot_by_project["short_name"] = ot_by_project["project_name"].apply(lambda x: x[:20] + "…" if len(x) > 20 else x)
    ot_by_project = ot_by_project.sort_values("overtime_hours", ascending=False)

    colors = [COLORS["accent_red"] if v > 100 else COLORS["accent_orange"] if v > 50 else COLORS["accent_yellow"]
              for v in ot_by_project["overtime_hours"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=ot_by_project["short_name"],
        y=ot_by_project["overtime_hours"],
        marker=dict(color=colors, opacity=0.85),
        text=[f"{v}h" for v in ot_by_project["overtime_hours"]],
        textposition="outside",
        textfont=dict(color=COLORS["text_primary"], size=11),
        hovertemplate="<b>%{x}</b><br>Total OT Hours: %{y}<extra></extra>",
    ))

    layout = CHART_LAYOUT.copy()
    layout.update(dict(
        title=dict(text="Overtime Hours by Project", font=dict(size=14, color=COLORS["text_primary"])),
        yaxis=dict(**CHART_LAYOUT["yaxis"], title="Total OT Hours"),
        height=300,
    ))
    fig.update_layout(**layout)
    return fig
