import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import date, timedelta
import random

# ── Reproducible sample data ────────────────────────────────────────────────
random.seed(42)
np.random.seed(42)

DEPARTMENTS = ["Engineering", "Sales", "HR", "Finance", "Marketing", "Operations"]
LOCATIONS   = ["New York", "London", "Singapore", "Toronto", "Sydney"]
GENDERS     = ["Male", "Female", "Non-binary"]

def random_date(start_year=2015, end_year=2024):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

n = 300
data = {
    "employee_id": [f"E{1000+i}" for i in range(n)],
    "name":        [f"Employee {i}" for i in range(n)],
    "department":  [random.choice(DEPARTMENTS) for _ in range(n)],
    "location":    [random.choice(LOCATIONS)   for _ in range(n)],
    "gender":      random.choices(GENDERS, weights=[48, 48, 4], k=n),
    "status":      random.choices(["Active", "Active", "Active", "Active", "Terminated"], k=n),
    "hire_date":   [random_date() for _ in range(n)],
    "salary":      np.random.randint(45_000, 180_000, n),
    "age":         np.random.randint(22, 62, n),
    "performance": np.random.choice(["Exceeds", "Meets", "Below"], n, p=[0.25, 0.60, 0.15]),
}

df = pd.DataFrame(data)
df["hire_date"]    = pd.to_datetime(df["hire_date"])
df["tenure_years"] = ((pd.Timestamp("today") - df["hire_date"]).dt.days / 365).round(1)
df["tenure_band"]  = pd.cut(
    df["tenure_years"],
    bins=[0, 1, 3, 5, 10, 99],
    labels=["<1 yr", "1-3 yrs", "3-5 yrs", "5-10 yrs", "10+ yrs"],
)

COLORS = {
    "primary":   "#0078D4",
    "secondary": "#50E6FF",
    "accent":    "#FFB900",
    "danger":    "#D13438",
    "success":   "#107C10",
    "bg":        "#F3F2F1",
    "text":      "#323130",
}

app = dash.Dash(__name__, title="HR Workforce Dashboard")

app.layout = html.Div(
    style={"backgroundColor": COLORS["bg"],
           "fontFamily": "Segoe UI, Arial, sans-serif",
           "minHeight": "100vh", "padding": "0"},
    children=[
        # Header
        html.Div(
            style={"backgroundColor": COLORS["primary"], "padding": "16px 32px",
                   "display": "flex", "alignItems": "center", "gap": "16px"},
            children=[
                html.H1("HR Workforce Dashboard",
                        style={"color": "white", "margin": 0, "fontSize": "24px"}),
                html.Span("Sample Data - 300 Employees",
                          style={"color": "#cce5ff", "fontSize": "13px"}),
            ],
        ),
        # Filters
        html.Div(
            style={"backgroundColor": "white", "padding": "12px 32px",
                   "display": "flex", "gap": "24px", "flexWrap": "wrap",
                   "borderBottom": "2px solid #F3F2F1"},
            children=[
                html.Div([
                    html.Label("Department", style={"fontWeight": "600", "fontSize": "12px"}),
                    dcc.Dropdown(
                        id="dept-filter",
                        options=[{"label": "All", "value": "All"}] +
                                [{"label": d, "value": d} for d in sorted(DEPARTMENTS)],
                        value="All", clearable=False, style={"width": "180px"},
                    ),
                ]),
                html.Div([
                    html.Label("Location", style={"fontWeight": "600", "fontSize": "12px"}),
                    dcc.Dropdown(
                        id="loc-filter",
                        options=[{"label": "All", "value": "All"}] +
                                [{"label": l, "value": l} for l in sorted(LOCATIONS)],
                        value="All", clearable=False, style={"width": "180px"},
                    ),
                ]),
                html.Div([
                    html.Label("Status", style={"fontWeight": "600", "fontSize": "12px"}),
                    dcc.Dropdown(
                        id="status-filter",
                        options=[{"label": "All", "value": "All"},
                                 {"label": "Active", "value": "Active"},
                                 {"label": "Terminated", "value": "Terminated"}],
                        value="All", clearable=False, style={"width": "160px"},
                    ),
                ]),
            ],
        ),
        # KPI row
        html.Div(id="kpi-row",
                 style={"display": "flex", "gap": "16px",
                        "padding": "24px 32px 8px", "flexWrap": "wrap"}),
        # Charts row 1
        html.Div(
            style={"display": "flex", "gap": "16px",
                   "padding": "8px 32px", "flexWrap": "wrap"},
            children=[
                html.Div(dcc.Graph(id="dept-bar"),
                         style={"flex": "1 1 420px", "backgroundColor": "white",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,.08)"}),
                html.Div(dcc.Graph(id="gender-pie"),
                         style={"flex": "0 1 340px", "backgroundColor": "white",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,.08)"}),
                html.Div(dcc.Graph(id="location-bar"),
                         style={"flex": "1 1 380px", "backgroundColor": "white",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,.08)"}),
            ],
        ),
        # Charts row 2
        html.Div(
            style={"display": "flex", "gap": "16px",
                   "padding": "8px 32px 32px", "flexWrap": "wrap"},
            children=[
                html.Div(dcc.Graph(id="tenure-bar"),
                         style={"flex": "1 1 380px", "backgroundColor": "white",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,.08)"}),
                html.Div(dcc.Graph(id="salary-box"),
                         style={"flex": "1 1 420px", "backgroundColor": "white",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,.08)"}),
                html.Div(dcc.Graph(id="perf-bar"),
                         style={"flex": "0 1 340px", "backgroundColor": "white",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,.08)"}),
            ],
        ),
    ],
)


def apply_filters(dept, loc, status):
    dff = df.copy()
    if dept   != "All": dff = dff[dff["department"] == dept]
    if loc    != "All": dff = dff[dff["location"]   == loc]
    if status != "All": dff = dff[dff["status"]      == status]
    return dff


def kpi_card(title, value, color=COLORS["primary"]):
    return html.Div(
        style={"backgroundColor": "white", "borderRadius": "8px",
               "padding": "16px 20px", "minWidth": "160px", "flex": "1 1 160px",
               "boxShadow": "0 2px 6px rgba(0,0,0,.08)",
               "borderTop": f"4px solid {color}"},
        children=[
            html.P(title, style={"margin": 0, "fontSize": "12px",
                                  "color": "#605E5C", "fontWeight": "600",
                                  "textTransform": "uppercase"}),
            html.P(str(value), style={"margin": "6px 0 2px", "fontSize": "28px",
                                       "fontWeight": "700", "color": COLORS["text"]}),
        ],
    )


@app.callback(
    Output("kpi-row",      "children"),
    Output("dept-bar",     "figure"),
    Output("gender-pie",   "figure"),
    Output("location-bar", "figure"),
    Output("tenure-bar",   "figure"),
    Output("salary-box",   "figure"),
    Output("perf-bar",     "figure"),
    Input("dept-filter",   "value"),
    Input("loc-filter",    "value"),
    Input("status-filter", "value"),
)
def update_dashboard(dept, loc, status):
    dff = apply_filters(dept, loc, status)
    total      = len(dff)
    active     = int((dff["status"] == "Active").sum())
    terminated = int((dff["status"] == "Terminated").sum())
    turnover   = f"{terminated / total * 100:.1f}%" if total else "n/a"
    avg_salary = f"${dff['salary'].mean():,.0f}" if total else "n/a"
    avg_tenure = f"{dff['tenure_years'].mean():.1f} yrs" if total else "n/a"

    kpis = [
        kpi_card("Total Employees", total,      color=COLORS["primary"]),
        kpi_card("Active",          active,     color=COLORS["success"]),
        kpi_card("Terminated",      terminated, color=COLORS["danger"]),
        kpi_card("Turnover Rate",   turnover,   color=COLORS["accent"]),
        kpi_card("Avg Salary",      avg_salary, color=COLORS["secondary"]),
        kpi_card("Avg Tenure",      avg_tenure, color="#8764B8"),
    ]

    base = dict(paper_bgcolor="white", plot_bgcolor="white",
                font=dict(family="Segoe UI, Arial", size=12, color=COLORS["text"]),
                margin=dict(l=16, r=16, t=40, b=16))

    # Headcount by department
    d = dff.groupby("department", observed=True).size().reset_index(name="count")
    dept_bar = px.bar(d, x="department", y="count",
                      title="Headcount by Department",
                      color="department",
                      color_discrete_sequence=px.colors.qualitative.Set2)
    dept_bar.update_layout(**base, showlegend=False)
    dept_bar.update_xaxes(title="")
    dept_bar.update_yaxes(title="Employees")

    # Gender donut
    g = dff["gender"].value_counts().reset_index()
    g.columns = ["gender", "count"]
    gender_pie = px.pie(g, names="gender", values="count",
                        title="Gender Distribution", hole=0.45,
                        color_discrete_sequence=[COLORS["primary"],
                                                 COLORS["accent"], "#8764B8"])
    gender_pie.update_layout(**base)
    gender_pie.update_traces(textposition="inside", textinfo="percent+label")

    # Headcount by location
    lo = dff.groupby("location", observed=True).size().reset_index(name="count")
    location_bar = px.bar(lo, x="count", y="location", orientation="h",
                          title="Headcount by Location",
                          color="count", color_continuous_scale="Blues")
    location_bar.update_layout(**base, coloraxis_showscale=False)
    location_bar.update_xaxes(title="Employees")
    location_bar.update_yaxes(title="")

    # Tenure distribution
    tc = dff["tenure_band"].value_counts().sort_index().reset_index()
    tc.columns = ["band", "count"]
    tenure_bar = px.bar(tc, x="band", y="count", title="Tenure Distribution",
                        color="band",
                        color_discrete_sequence=px.colors.sequential.Blues_r)
    tenure_bar.update_layout(**base, showlegend=False)
    tenure_bar.update_xaxes(title="")
    tenure_bar.update_yaxes(title="Employees")

    # Salary box by department
    salary_box = px.box(dff, x="department", y="salary",
                        title="Salary Distribution by Department",
                        color="department",
                        color_discrete_sequence=px.colors.qualitative.Set2)
    salary_box.update_layout(**base, showlegend=False)
    salary_box.update_xaxes(title="")
    salary_box.update_yaxes(title="Salary (USD)", tickformat=",")

    # Performance ratings
    perf_order = ["Exceeds", "Meets", "Below"]
    pc = (dff["performance"].value_counts()
          .reindex(perf_order, fill_value=0).reset_index())
    pc.columns = ["rating", "count"]
    perf_bar = px.bar(pc, x="rating", y="count", title="Performance Ratings",
                      color="rating",
                      color_discrete_map={"Exceeds": COLORS["success"],
                                          "Meets":   COLORS["primary"],
                                          "Below":   COLORS["danger"]})
    perf_bar.update_layout(**base, showlegend=False)
    perf_bar.update_xaxes(title="")
    perf_bar.update_yaxes(title="Employees")

    return kpis, dept_bar, gender_pie, location_bar, tenure_bar, salary_box, perf_bar


if __name__ == "__main__":
    app.run(debug=True)
