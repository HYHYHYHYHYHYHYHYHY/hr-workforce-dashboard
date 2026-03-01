import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import date, timedelta
import random

SHOW_SALARY = False
MIDDLE_CHART_ID = "salary-box" if SHOW_SALARY else "women-metrics-bar"

# ── Reproducible sample data ────────────────────────────────────────────────
random.seed(42)
np.random.seed(42)

DEPARTMENTS = ["Engineering", "Sales", "HR", "Finance", "Marketing"]
LOCATIONS   = ["New York", "London", "Singapore", "Toronto", "Sydney"]
GENDERS     = ["Male", "Female", "Other/Prefer not to disclose"]

def random_date(start_year=2015, end_year=date.today().year):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))


def random_date_between(start_date, end_date):
    if start_date > end_date:
        return start_date
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

n = 300
data = {
    "employee_id": [f"E{1000+i}" for i in range(n)],
    "name":        [f"Employee {i}" for i in range(n)],
    "department":  [random.choice(DEPARTMENTS) for _ in range(n)],
    "location":    [random.choice(LOCATIONS)   for _ in range(n)],
    "gender":      random.choices(GENDERS, weights=[48, 48, 4], k=n),
    "hire_date":   [random_date() for _ in range(n)],
    "salary":      np.random.randint(45_000, 180_000, n),
    "age":         np.random.randint(22, 62, n),
    "performance": np.random.choice(["Exceeds", "Meets", "Below"], n, p=[0.25, 0.60, 0.15]),
    "is_senior_role": np.random.choice([True, False], n, p=[0.17, 0.83]),
    "promoted_ytd": np.random.choice([True, False], n, p=[0.14, 0.86]),
    "high_potential": np.random.choice([True, False], n, p=[0.22, 0.78]),
    "successor_ready": np.random.choice([True, False], n, p=[0.74, 0.26]),
}

df = pd.DataFrame(data)
df["hire_date"]    = pd.to_datetime(df["hire_date"])
df["tenure_years"] = ((pd.Timestamp("today") - df["hire_date"]).dt.days / 365).round(1)
df["tenure_band"]  = pd.cut(
    df["tenure_years"],
    bins=[0, 1, 3, 5, 10, 99],
    labels=["<1 yr", "1-3 yrs", "3-5 yrs", "5-10 yrs", "10+ yrs"],
)

# Terminations table (separate from employee master table)
today_date = date.today()
termination_share = random.uniform(0.18, 0.28)
eligible_termination_ids = df.loc[df["hire_date"].dt.date <= today_date, "employee_id"].tolist()
termination_count = min(len(eligible_termination_ids), max(1, int(round(len(eligible_termination_ids) * termination_share))))
terminated_employee_ids = np.random.choice(eligible_termination_ids, size=termination_count, replace=False)
termination_records = []

for employee_id in terminated_employee_ids:
    hire_date = df.loc[df["employee_id"] == employee_id, "hire_date"].iloc[0].date()
    earliest_term_date = hire_date + timedelta(days=30)
    term_date = random_date_between(earliest_term_date, today_date)
    termination_records.append(
        {
            "employee_id": employee_id,
            "termination_date": pd.Timestamp(term_date),
            "termination_reason": random.choices(["Voluntary", "Involuntary"], weights=[70, 30], k=1)[0],
        }
    )

terminations_df = pd.DataFrame(termination_records)

df["status"] = "Active"
df.loc[df["employee_id"].isin(terminations_df["employee_id"]), "status"] = "Terminated"

AVAILABLE_REPORT_YEARS = sorted(df["hire_date"].dt.year.unique().tolist(), reverse=True)
DEFAULT_REPORT_YEAR = AVAILABLE_REPORT_YEARS[0]

# Internal mobility events table (separate from employee master table)
internal_move_records = []
for year in AVAILABLE_REPORT_YEARS:
    year_end = pd.Timestamp(year=year, month=12, day=31)
    eligible_ids = df.loc[df["hire_date"] <= year_end, "employee_id"].tolist()
    if not eligible_ids:
        continue

    annual_move_share = random.uniform(0.20, 0.25)
    annual_move_count = min(len(eligible_ids), max(1, int(round(len(eligible_ids) * annual_move_share))))
    moved_ids = np.random.choice(eligible_ids, size=annual_move_count, replace=False)

    for employee_id in moved_ids:
        internal_move_records.append(
            {
                "employee_id": employee_id,
                "move_date": pd.Timestamp(random_date(start_year=year, end_year=year)),
                "move_type": random.choices(
                    ["Role Change", "Lateral Move", "Step-up Move"],
                    weights=[45, 35, 20],
                    k=1,
                )[0],
            }
        )

internal_moves_df = pd.DataFrame(internal_move_records)

# Positions table (separate from employee master table)
position_count = int(n * 1.2)
positions_df = pd.DataFrame(
    {
        "position_id": [f"P{10000+i}" for i in range(position_count)],
        "department": [random.choice(DEPARTMENTS) for _ in range(position_count)],
        "location": [random.choice(LOCATIONS) for _ in range(position_count)],
        "is_open": np.random.choice([True, False], position_count, p=[0.14, 0.86]),
    }
)

# Department finance table (separate from employee and position tables)
finance_records = []
for year in AVAILABLE_REPORT_YEARS:
    year_end = pd.Timestamp(year=year, month=12, day=31)
    for department_name in DEPARTMENTS:
        dept_fte = int(((df["department"] == department_name) & (df["hire_date"] <= year_end)).sum())
        dept_fte = max(dept_fte, 10)
        net_income = int(dept_fte * random.randint(42_000, 88_000))
        finance_records.append(
            {
                "report_year": year,
                "department": department_name,
                "department_fte": dept_fte,
                "department_net_income": net_income,
            }
        )

department_finance_df = pd.DataFrame(finance_records)

COLORS = {
    "primary":   "#00B7A8",
    "secondary": "#7FD8CF",
    "accent":    "#F5B448",
    "danger":    "#EF4444",
    "success":   "#10B981",
    "bg":        "#F8FAFC",
    "surface":   "#FFFFFF",
    "text":      "#0F172A",
    "muted":     "#64748B",
    "border":    "#E2E8F0",
}

WORKDAY_CHART_SEQUENCE = [
    "#9EDFD3",
    "#59C7BC",
    "#BFEAE3",
    "#7BCFC5",
    "#D9F2EE",
    "#84A4DD",
    "#C4D2EE",
]

DEPARTMENT_NEUTRAL_SEQUENCE = [
    "#D9F2EE",
    "#BFEAE3",
    "#9EDFD3",
    "#7BCFC5",
    "#84A4DD",
]

GENDER_COLOR_MAP = {
    "Female": "#F5B448",
    "Male": "#59C7BC",
    "Other/Prefer not to disclose": "#D9F2EE",
}

PERFORMANCE_COLOR_MAP = {
    "Exceeds": "#59C7BC",
    "Meets": "#9EDFD3",
    "Below": "#F5B448",
}

WOMEN_SNAPSHOT_COLOR_MAP = {
    "Workforce": "#F5B448",
    "Leadership": "#59C7BC",
    "Promotions": "#9EDFD3",
    "New Hires": "#BFEAE3",
    "Departures": "#7BCFC5",
}

employees_preview = df.head(20).copy()
internal_moves_preview = internal_moves_df.head(20).copy()
internal_moves_preview["move_date"] = internal_moves_preview["move_date"].dt.strftime("%Y-%m-%d")
terminations_preview = terminations_df.head(20).copy()
terminations_preview["termination_date"] = terminations_preview["termination_date"].dt.strftime("%Y-%m-%d")
positions_preview = positions_df.head(20).copy()
finance_preview = department_finance_df.head(20).copy()

app = dash.Dash(__name__, title="HR Workforce Dashboard")
server = app.server

app.layout = html.Div(
    style={"backgroundColor": COLORS["bg"],
           "fontFamily": "Inter, Segoe UI, Roboto, Arial, sans-serif",
           "minHeight": "100vh", "padding": "0"},
    children=[
        # Header
        html.Div(
            style={"background": f"linear-gradient(120deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%)", "padding": "16px 32px",
                   "display": "flex", "alignItems": "center", "gap": "16px"},
            children=[
                html.H1("HR Workforce Dashboard",
                        style={"color": "white", "margin": 0, "fontSize": "24px"}),
                html.Span("Sample Data - 300 Employees",
                         style={"color": "#E2E8F0", "fontSize": "13px"}),
            ],
        ),
        # Filters
        html.Div(
                 style={"backgroundColor": COLORS["surface"], "padding": "12px 32px",
                   "display": "flex", "gap": "24px", "flexWrap": "wrap",
                     "borderBottom": f"1px solid {COLORS['border']}"},
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
                html.Div([
                    html.Label("Report Year", style={"fontWeight": "600", "fontSize": "12px"}),
                    dcc.Dropdown(
                        id="report-year-filter",
                        options=[{"label": str(year), "value": int(year)} for year in AVAILABLE_REPORT_YEARS],
                        value=DEFAULT_REPORT_YEAR,
                        clearable=False,
                        style={"width": "140px"},
                    ),
                ]),
            ],
        ),
        # KPI row
        html.Div(id="kpi-row",
                 style={"display": "flex", "gap": "16px",
                        "padding": "24px 32px 8px", "flexWrap": "wrap"}),
         # Strategic metric tiles
         html.Div(id="strategic-metrics-grid",
               style={"display": "grid",
                   "gridTemplateColumns": "repeat(auto-fill, minmax(210px, 210px))",
                   "justifyContent": "space-between",
                   "gap": "10px",
                   "padding": "8px 32px 12px"}),
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
                html.Div(dcc.Graph(id=MIDDLE_CHART_ID),
                         style={"flex": "1 1 420px", "backgroundColor": "white",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,.08)"}),
                html.Div(dcc.Graph(id="perf-bar"),
                         style={"flex": "0 1 340px", "backgroundColor": "white",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,.08)"}),
            ],
        ),
        # Termination chart
        html.Div(
            style={"padding": "0 32px 16px"},
            children=[
                html.Div(dcc.Graph(id="termination-reason-bar"),
                         style={"backgroundColor": "white",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,.08)"}),
            ],
        ),
        # Synthetic data preview
        html.Div(
            style={"padding": "0 32px 32px"},
            children=[
                html.H3("Synthetic Data Preview", style={"margin": "8px 0 12px", "color": COLORS["text"]}),
                html.Div(
                    style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(320px, 1fr))", "gap": "12px"},
                    children=[
                        html.Div(
                            style={"backgroundColor": "white", "borderRadius": "8px", "boxShadow": "0 2px 6px rgba(0,0,0,.08)", "padding": "12px"},
                            children=[
                                html.Div(
                                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "8px"},
                                    children=[
                                        html.H4("Employees (Top 20)", style={"margin": 0, "fontSize": "14px", "color": COLORS["text"]}),
                                        html.Button("Download CSV", id="download-employees-btn",
                                                    style={"border": "1px solid #D2D0CE", "borderRadius": "4px", "padding": "4px 10px", "cursor": "pointer"}),
                                    ],
                                ),
                                dcc.Download(id="download-employees"),
                                dash_table.DataTable(
                                    data=employees_preview.to_dict("records"),
                                    columns=[{"name": column_name, "id": column_name} for column_name in employees_preview.columns],
                                    page_size=6,
                                    style_table={"overflowX": "auto"},
                                    style_cell={"textAlign": "left", "fontSize": "11px", "padding": "6px", "whiteSpace": "normal", "height": "auto"},
                                    style_header={"fontWeight": "700", "backgroundColor": "#F8F8F8"},
                                ),
                            ],
                        ),
                        html.Div(
                            style={"backgroundColor": "white", "borderRadius": "8px", "boxShadow": "0 2px 6px rgba(0,0,0,.08)", "padding": "12px"},
                            children=[
                                html.Div(
                                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "8px"},
                                    children=[
                                        html.H4("Terminations (Top 20)", style={"margin": 0, "fontSize": "14px", "color": COLORS["text"]}),
                                        html.Button("Download CSV", id="download-terminations-btn",
                                                    style={"border": "1px solid #D2D0CE", "borderRadius": "4px", "padding": "4px 10px", "cursor": "pointer"}),
                                    ],
                                ),
                                dcc.Download(id="download-terminations"),
                                dash_table.DataTable(
                                    data=terminations_preview.to_dict("records"),
                                    columns=[{"name": column_name, "id": column_name} for column_name in terminations_preview.columns],
                                    page_size=6,
                                    style_table={"overflowX": "auto"},
                                    style_cell={"textAlign": "left", "fontSize": "11px", "padding": "6px", "whiteSpace": "normal", "height": "auto"},
                                    style_header={"fontWeight": "700", "backgroundColor": "#F8F8F8"},
                                ),
                            ],
                        ),
                        html.Div(
                            style={"backgroundColor": "white", "borderRadius": "8px", "boxShadow": "0 2px 6px rgba(0,0,0,.08)", "padding": "12px"},
                            children=[
                                html.Div(
                                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "8px"},
                                    children=[
                                        html.H4("Internal Moves (Top 20)", style={"margin": 0, "fontSize": "14px", "color": COLORS["text"]}),
                                        html.Button("Download CSV", id="download-internal-moves-btn",
                                                    style={"border": "1px solid #D2D0CE", "borderRadius": "4px", "padding": "4px 10px", "cursor": "pointer"}),
                                    ],
                                ),
                                dcc.Download(id="download-internal-moves"),
                                dash_table.DataTable(
                                    data=internal_moves_preview.to_dict("records"),
                                    columns=[{"name": column_name, "id": column_name} for column_name in internal_moves_preview.columns],
                                    page_size=6,
                                    style_table={"overflowX": "auto"},
                                    style_cell={"textAlign": "left", "fontSize": "11px", "padding": "6px", "whiteSpace": "normal", "height": "auto"},
                                    style_header={"fontWeight": "700", "backgroundColor": "#F8F8F8"},
                                ),
                            ],
                        ),
                        html.Div(
                            style={"backgroundColor": "white", "borderRadius": "8px", "boxShadow": "0 2px 6px rgba(0,0,0,.08)", "padding": "12px"},
                            children=[
                                html.Div(
                                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "8px"},
                                    children=[
                                        html.H4("Positions (Top 20)", style={"margin": 0, "fontSize": "14px", "color": COLORS["text"]}),
                                        html.Button("Download CSV", id="download-positions-btn",
                                                    style={"border": "1px solid #D2D0CE", "borderRadius": "4px", "padding": "4px 10px", "cursor": "pointer"}),
                                    ],
                                ),
                                dcc.Download(id="download-positions"),
                                dash_table.DataTable(
                                    data=positions_preview.to_dict("records"),
                                    columns=[{"name": column_name, "id": column_name} for column_name in positions_preview.columns],
                                    page_size=6,
                                    style_table={"overflowX": "auto"},
                                    style_cell={"textAlign": "left", "fontSize": "11px", "padding": "6px", "whiteSpace": "normal", "height": "auto"},
                                    style_header={"fontWeight": "700", "backgroundColor": "#F8F8F8"},
                                ),
                            ],
                        ),
                        html.Div(
                            style={"backgroundColor": "white", "borderRadius": "8px", "boxShadow": "0 2px 6px rgba(0,0,0,.08)", "padding": "12px"},
                            children=[
                                html.Div(
                                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "8px"},
                                    children=[
                                        html.H4("Department Finance (Top 20)", style={"margin": 0, "fontSize": "14px", "color": COLORS["text"]}),
                                        html.Button("Download CSV", id="download-finance-btn",
                                                    style={"border": "1px solid #D2D0CE", "borderRadius": "4px", "padding": "4px 10px", "cursor": "pointer"}),
                                    ],
                                ),
                                dcc.Download(id="download-finance"),
                                dash_table.DataTable(
                                    data=finance_preview.to_dict("records"),
                                    columns=[{"name": column_name, "id": column_name} for column_name in finance_preview.columns],
                                    page_size=6,
                                    style_table={"overflowX": "auto"},
                                    style_cell={"textAlign": "left", "fontSize": "11px", "padding": "6px", "whiteSpace": "normal", "height": "auto"},
                                    style_header={"fontWeight": "700", "backgroundColor": "#F8F8F8"},
                                ),
                            ],
                        ),
                    ],
                ),
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
        style={"backgroundColor": COLORS["surface"], "borderRadius": "10px",
               "padding": "16px 20px", "minWidth": "160px", "flex": "1 1 160px",
               "boxShadow": "0 8px 24px rgba(15,23,42,.06)",
               "border": f"1px solid {COLORS['border']}",
               "borderTop": f"4px solid {color}"},
        children=[
            html.P(title, style={"margin": 0, "fontSize": "12px",
                                  "color": COLORS["muted"], "fontWeight": "600",
                                  "textTransform": "uppercase"}),
            html.P(str(value), style={"margin": "6px 0 2px", "fontSize": "28px",
                                       "fontWeight": "700", "color": COLORS["text"]}),
        ],
    )


def metric_tile(title, value, note, color):
    return html.Div(
        style={"backgroundColor": COLORS["surface"], "borderRadius": "10px",
               "padding": "12px 14px", "boxShadow": "0 8px 24px rgba(15,23,42,.06)",
               "border": f"1px solid {COLORS['border']}",
               "borderLeft": f"4px solid {color}"},
        children=[
            html.P(title, style={"margin": "0 0 4px", "fontSize": "11px",
                                 "fontWeight": "600", "color": COLORS["muted"],
                                 "textTransform": "uppercase"}),
            html.P(value, style={"margin": "0", "fontSize": "22px",
                                 "fontWeight": "700", "color": COLORS["text"]}),
            html.P(note, style={"margin": "3px 0 0", "fontSize": "11px",
                                "color": COLORS["muted"]}),
        ],
    )


@app.callback(
    Output("kpi-row",      "children"),
    Output("strategic-metrics-grid", "children"),
    Output("dept-bar",     "figure"),
    Output("gender-pie",   "figure"),
    Output("location-bar", "figure"),
    Output("termination-reason-bar", "figure"),
    Output("tenure-bar",   "figure"),
    Output(MIDDLE_CHART_ID, "figure"),
    Output("perf-bar",     "figure"),
    Input("dept-filter",   "value"),
    Input("loc-filter",    "value"),
    Input("status-filter", "value"),
    Input("report-year-filter", "value"),
)
def update_dashboard(dept, loc, status, report_year):
    dff = apply_filters(dept, loc, status)
    report_year = int(report_year) if report_year is not None else DEFAULT_REPORT_YEAR
    period_start = pd.Timestamp(year=report_year, month=1, day=1)
    period_end = pd.Timestamp(year=report_year, month=12, day=31)

    employee_scope = df.copy()
    if dept != "All":
        employee_scope = employee_scope[employee_scope["department"] == dept]
    if loc != "All":
        employee_scope = employee_scope[employee_scope["location"] == loc]
    employee_scope_ids = set(employee_scope["employee_id"])

    terminations_year_scope = terminations_df[terminations_df["termination_date"].dt.year.eq(report_year)]
    terminations_year_scope = terminations_year_scope[terminations_year_scope["employee_id"].isin(employee_scope_ids)]
    terminations_all_scope = terminations_df[terminations_df["employee_id"].isin(employee_scope_ids)]

    positions_scope = positions_df.copy()
    if dept != "All":
        positions_scope = positions_scope[positions_scope["department"] == dept]
    if loc != "All":
        positions_scope = positions_scope[positions_scope["location"] == loc]

    finance_scope = department_finance_df[department_finance_df["report_year"] == report_year]
    if dept != "All":
        finance_scope = finance_scope[finance_scope["department"] == dept]

    location_coords = {
        "New York": {"lat": 40.7128, "lon": -74.0060},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Singapore": {"lat": 1.3521, "lon": 103.8198},
        "Toronto": {"lat": 43.6532, "lon": -79.3832},
        "Sydney": {"lat": -33.8688, "lon": 151.2093},
    }

    total      = len(dff)
    active     = int((dff["status"] == "Active").sum())
    terminated = int((dff["status"] == "Terminated").sum())
    separations_in_period = int(len(terminations_year_scope))
    voluntary_separations = int((terminations_year_scope["termination_reason"] == "Voluntary").sum())

    hired_before_start_ids = set(employee_scope.loc[employee_scope["hire_date"] < period_start, "employee_id"])
    hired_before_end_ids = set(employee_scope.loc[employee_scope["hire_date"] <= period_end, "employee_id"])
    terminated_before_start_ids = set(terminations_all_scope.loc[terminations_all_scope["termination_date"] < period_start, "employee_id"])
    terminated_before_end_ids = set(terminations_all_scope.loc[terminations_all_scope["termination_date"] <= period_end, "employee_id"])

    start_headcount = len(hired_before_start_ids - terminated_before_start_ids)
    end_headcount = len(hired_before_end_ids - terminated_before_end_ids)
    average_headcount = (start_headcount + end_headcount) / 2
    turnover = f"{separations_in_period / average_headcount * 100:.1f}%" if average_headcount else "n/a"
    voluntary_termination_ratio = (
        f"{voluntary_separations / average_headcount * 100:.1f}%"
        if average_headcount else "n/a"
    )
    avg_salary = f"${dff['salary'].mean():,.0f}" if total else "n/a"
    avg_tenure = f"{dff['tenure_years'].mean():.1f} yrs" if total else "n/a"

    women = dff["gender"].eq("Female")
    senior = dff["is_senior_role"]
    promoted = dff["promoted_ytd"]
    ytd_hires = dff["hire_date"].dt.year.eq(report_year)
    terminated_ids_in_scope = set(terminations_year_scope["employee_id"])
    ytd_exits = dff["employee_id"].isin(terminated_ids_in_scope)

    def pct(mask):
        return f"{mask.mean() * 100:.1f}%" if len(mask) else "n/a"

    def pct_with_denominator(num_mask, den_mask):
        denominator = int(den_mask.sum())
        if denominator == 0:
            return "n/a", "No matching records"
        numerator = int((num_mask & den_mask).sum())
        return f"{numerator / denominator * 100:.1f}%", f"{numerator} of {denominator}"

    women_senior_pct, women_senior_note = pct_with_denominator(women, senior)
    women_promoted_pct, women_promoted_note = pct_with_denominator(women, promoted)
    women_hires_pct, women_hires_note = pct_with_denominator(women, ytd_hires)
    women_exits_pct, women_exits_note = pct_with_denominator(women, ytd_exits)

    moves_in_selected_year = internal_moves_df[internal_moves_df["move_date"].dt.year.eq(report_year)]
    employees_in_scope = set(dff["employee_id"])
    internal_fills_count = int(
        moves_in_selected_year["employee_id"].isin(employees_in_scope).sum()
    )
    internal_fill_pct = f"{internal_fills_count / total * 100:.1f}%" if total else "n/a"
    women_workforce_pct = pct(women) if total else "n/a"
    total_positions_in_scope = len(positions_scope)
    open_positions_in_scope = int(positions_scope["is_open"].sum())
    vacancy_pct = f"{open_positions_in_scope / total_positions_in_scope * 100:.1f}%" if total_positions_in_scope else "n/a"
    hipos_in_senior_pct, hipos_note = pct_with_denominator(dff["high_potential"], senior)
    succession_pct, succession_note = pct_with_denominator(dff["successor_ready"], senior)

    finance_net_income = int(finance_scope["department_net_income"].sum()) if len(finance_scope) else 0
    finance_fte = int(finance_scope["department_fte"].sum()) if len(finance_scope) else 0
    profit_per_fte = f"${finance_net_income / finance_fte:,.0f}" if finance_fte else "n/a"
    net_income_display = f"${finance_net_income:,.0f}" if finance_net_income else "n/a"

    kpis = [
        # kpi_card("Team Size", total,          color=COLORS["primary"]),
        kpi_card("Currently Active", active,   color=COLORS["success"]),
        # kpi_card("Separated", terminated,      color=COLORS["danger"]),
        kpi_card("Terminations YTD", separations_in_period, color=COLORS["danger"]),
        kpi_card("Attrition YTD", turnover,        color=COLORS["danger"]),
        kpi_card("Voluntary termination ratio YTD", voluntary_termination_ratio, color=COLORS["danger"]),
        kpi_card("Average Service", avg_tenure, color="#8764B8"),
    ]
    if SHOW_SALARY:
        kpis.insert(4, kpi_card("Average Pay", avg_salary, color=COLORS["secondary"]))

    strategic_tiles = [
        metric_tile("Internal role fills YTD", internal_fill_pct,
                    f"{internal_fills_count} event(s) in {report_year}", COLORS["primary"]),
        metric_tile("Women across workforce", women_workforce_pct,
                    "Current filtered population", COLORS["success"]),
        metric_tile("Women in leadership roles", women_senior_pct,
                    women_senior_note, COLORS["success"]),
        metric_tile("Women promoted YTD", women_promoted_pct,
                    women_promoted_note, COLORS["success"]),
        metric_tile("Women among new hires", women_hires_pct,
                    women_hires_note, COLORS["success"]),
        metric_tile("Women among departures", women_exits_pct,
                    women_exits_note, COLORS["success"]),
        metric_tile("Profit per FTE", profit_per_fte,
                f"{report_year} finance scope", COLORS["primary"]),
        metric_tile("Department net income", net_income_display,
                f"{report_year} finance scope", COLORS["primary"]),
        metric_tile("Open position ratio", vacancy_pct,
                    f"{open_positions_in_scope} of {total_positions_in_scope} positions open", COLORS["primary"]),
        metric_tile("High-potential share in senior roles", hipos_in_senior_pct,
                    hipos_note, "#C239B3"),
        metric_tile("Succession cover in leadership", succession_pct,
                    succession_note, "#C239B3"),
   ]
    base = dict(
        paper_bgcolor=COLORS["surface"],
        plot_bgcolor=COLORS["surface"],
        font=dict(family="Inter, Segoe UI, Roboto, Arial", size=12, color=COLORS["text"]),
        margin=dict(l=16, r=16, t=40, b=16),
    )

    # Headcount by department
    d = dff.groupby("department", observed=True).size().reset_index(name="count")
    largest_department = d.loc[d["count"].idxmax(), "department"] if not d.empty else None
    dept_color_map = {}
    neutral_index = 0
    for department_name in sorted(d["department"].tolist()):
        if department_name == largest_department:
            dept_color_map[department_name] = COLORS["accent"]
        else:
            dept_color_map[department_name] = DEPARTMENT_NEUTRAL_SEQUENCE[neutral_index % len(DEPARTMENT_NEUTRAL_SEQUENCE)]
            neutral_index += 1

    dept_bar = px.bar(d, x="department", y="count",
                      title="Headcount by Department",
                      color="department",
                      color_discrete_map=dept_color_map)
    dept_bar.update_layout(**base, showlegend=False)
    dept_bar.update_xaxes(title="", showgrid=False)
    dept_bar.update_yaxes(title="Employees", gridcolor="#D9E2E1", zerolinecolor="#D9E2E1")

    # Gender donut
    g = dff["gender"].value_counts().reset_index()
    g.columns = ["gender", "count"]
    gender_pie = px.pie(g, names="gender", values="count",
                        title="Gender Distribution", hole=0.45,
                        color="gender",
                        color_discrete_map=GENDER_COLOR_MAP)
    gender_layout = base.copy()
    gender_layout["legend"] = dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5)
    gender_layout["margin"] = dict(l=16, r=16, t=50, b=64)
    gender_pie.update_layout(**gender_layout)
    gender_pie.update_traces(domain=dict(x=[0.15, 0.85], y=[0.18, 0.95]))
    gender_pie.update_traces(textposition="outside", textinfo="percent+label", marker=dict(line=dict(color="#D9E2E1", width=1)))

    # Headcount by location (bubble map)
    lo = dff.groupby("location", observed=True).size().reset_index(name="count")
    lo["lat"] = lo["location"].map(lambda location: location_coords.get(location, {}).get("lat"))
    lo["lon"] = lo["location"].map(lambda location: location_coords.get(location, {}).get("lon"))
    lo = lo.dropna(subset=["lat", "lon"])
    location_bar = px.scatter_geo(
        lo,
        lat="lat",
        lon="lon",
        size="count",
        color="count",
        hover_name="location",
        hover_data={"count": True, "lat": False, "lon": False},
        color_continuous_scale=[
            [0.0, "#D9F2EE"],
            [0.4, "#9EDFD3"],
            [0.7, "#59C7BC"],
            [1.0, "#00B7A8"],
        ],
        projection="natural earth",
        title="Headcount by Location (Bubble Map)",
    )
    location_layout = base.copy()
    location_layout["margin"] = dict(l=6, r=6, t=48, b=6)
    location_layout["height"] = 470
    location_layout["coloraxis_showscale"] = False
    location_layout["geo"] = dict(
        showland=True,
        landcolor="#F3F2F1",
        bgcolor="white",
        showcountries=True,
        countrycolor="#BFC8C7",
        countrywidth=0.8,
        showcoastlines=True,
        coastlinecolor="#BFC8C7",
        coastlinewidth=0.8,
        showframe=False,
        domain={"x": [0.0, 1.0], "y": [0.0, 1.0]},
    )
    location_bar.update_layout(**location_layout)
    location_bar.update_traces(marker=dict(line=dict(color="#BFC8C7", width=0.8)))

    termination_reason_counts = (terminations_year_scope["termination_reason"]
                                 .value_counts()
                                 .reindex(["Voluntary", "Involuntary"], fill_value=0)
                                 .reset_index())
    termination_reason_counts.columns = ["reason", "count"]
    termination_reason_bar = px.bar(
        termination_reason_counts,
        x="reason",
        y="count",
        title=f"Terminations by Reason ({report_year})",
        color="reason",
        color_discrete_map={"Voluntary": "#59C7BC", "Involuntary": "#F5B448"},
        text="count",
    )
    termination_reason_bar.update_layout(**base, showlegend=False)
    termination_reason_bar.update_traces(textposition="outside")
    termination_reason_bar.update_xaxes(title="", showgrid=False)
    termination_reason_bar.update_yaxes(title="Employees", gridcolor="#D9E2E1", zerolinecolor="#D9E2E1")

    # Tenure distribution
    tc = dff["tenure_band"].value_counts().sort_index().reset_index()
    tc.columns = ["band", "count"]
    tenure_bar = px.bar(tc, x="band", y="count", title="Tenure Distribution",
                        color="band",
                        color_discrete_sequence=["#D9F2EE", "#BFEAE3", "#9EDFD3", "#7BCFC5", "#59C7BC"])
    tenure_bar.update_layout(**base, showlegend=False)
    tenure_bar.update_xaxes(title="", showgrid=False)
    tenure_bar.update_yaxes(title="Employees", gridcolor="#D9E2E1", zerolinecolor="#D9E2E1")

    if SHOW_SALARY:
        middle_chart = px.box(dff, x="department", y="salary",
                              title="Salary Distribution by Department",
                              color="department",
                              color_discrete_map=dept_color_map)
        middle_chart.update_layout(**base, showlegend=False)
        middle_chart.update_xaxes(title="", showgrid=False)
        middle_chart.update_yaxes(title="Salary (USD)", tickformat=",", gridcolor="#D9E2E1", zerolinecolor="#D9E2E1")
    else:
        women_metric_df = pd.DataFrame(
            {
                "metric": [
                    "Workforce",
                    "Leadership",
                    "Promotions",
                    "New Hires",
                    "Departures",
                ],
                "share": [
                    (women.mean() * 100) if total else 0,
                    ((women & senior).sum() / senior.sum() * 100) if senior.sum() else 0,
                    ((women & promoted).sum() / promoted.sum() * 100) if promoted.sum() else 0,
                    ((women & ytd_hires).sum() / ytd_hires.sum() * 100) if ytd_hires.sum() else 0,
                    ((women & ytd_exits).sum() / ytd_exits.sum() * 100) if ytd_exits.sum() else 0,
                ],
            }
        )

        middle_chart = px.bar(
            women_metric_df,
            x="metric",
            y="share",
            title="Women Representation Snapshot",
            color="metric",
            color_discrete_map=WOMEN_SNAPSHOT_COLOR_MAP,
            text="share",
        )
        middle_chart.update_layout(**base, showlegend=False)
        middle_chart.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        middle_chart.update_xaxes(title="", showgrid=False)
        middle_chart.update_yaxes(title="Share (%)", range=[0, 100], gridcolor="#D9E2E1", zerolinecolor="#D9E2E1")

    # Performance ratings
    perf_order = ["Below", "Meets","Exceeds"]
    pc = (dff["performance"].value_counts()
          .reindex(perf_order, fill_value=0).reset_index())
    pc.columns = ["rating", "count"]
    perf_bar = px.bar(pc, x="rating", y="count", title="Performance Ratings",
                      color="rating",
                      color_discrete_map=PERFORMANCE_COLOR_MAP)
    perf_bar.update_layout(**base, showlegend=False)
    perf_bar.update_xaxes(title="", showgrid=False)
    perf_bar.update_yaxes(title="Employees", gridcolor="#D9E2E1", zerolinecolor="#D9E2E1")

    return kpis, strategic_tiles, dept_bar, gender_pie, location_bar, termination_reason_bar, tenure_bar, middle_chart, perf_bar


@app.callback(
    Output("download-employees", "data"),
    Input("download-employees-btn", "n_clicks"),
    prevent_initial_call=True,
)
def download_employees_csv(_):
    return dcc.send_data_frame(df.to_csv, "synthetic_employees.csv", index=False)


@app.callback(
    Output("download-internal-moves", "data"),
    Input("download-internal-moves-btn", "n_clicks"),
    prevent_initial_call=True,
)
def download_internal_moves_csv(_):
    return dcc.send_data_frame(internal_moves_df.to_csv, "synthetic_internal_moves.csv", index=False)


@app.callback(
    Output("download-terminations", "data"),
    Input("download-terminations-btn", "n_clicks"),
    prevent_initial_call=True,
)
def download_terminations_csv(_):
    return dcc.send_data_frame(terminations_df.to_csv, "synthetic_terminations.csv", index=False)


@app.callback(
    Output("download-positions", "data"),
    Input("download-positions-btn", "n_clicks"),
    prevent_initial_call=True,
)
def download_positions_csv(_):
    return dcc.send_data_frame(positions_df.to_csv, "synthetic_positions.csv", index=False)


@app.callback(
    Output("download-finance", "data"),
    Input("download-finance-btn", "n_clicks"),
    prevent_initial_call=True,
)
def download_finance_csv(_):
    return dcc.send_data_frame(department_finance_df.to_csv, "synthetic_department_finance.csv", index=False)


if __name__ == "__main__":
    app.run(debug=True)
