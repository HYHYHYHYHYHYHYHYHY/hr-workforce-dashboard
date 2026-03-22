# HR Workforce Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Dash](https://img.shields.io/badge/Plotly%20Dash-2.14+-informational?logo=plotly&logoColor=white)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

An interactive HR analytics dashboard built with Python, Dash, Plotly, and Pandas.
The app is intentionally written in a single `app.py` so it is easy to read end-to-end while learning.

> 🔴 **[View Live Demo](https://hr-workforce-dashboard.onrender.com)** (Render free tier may take ~30s to wake up)

---

## What This Project Teaches

If you are learning coding/data apps, this project is useful because it combines:

- **Data modeling** (separate tables for employees, terminations, internal moves, positions, finance)
- **Business KPI design** (attrition, voluntary ratio, internal fill rate, vacancy pressure)
- **Reactive UI programming** (one callback updates all cards and charts from filters)
- **Storytelling with visuals** (department, geography, gender, tenure, performance, termination reasons)

---

## Dashboard Features

### KPI Cards (top row)

- **Currently Active (as of year-end)**
- **Terminations (Report Year)**
- **Attrition (Report Year)**
- **Voluntary termination ratio (Report Year)**
- **Average Service (as of year-end)**
- **Average Pay** *(only shown when `SHOW_SALARY = True`)*

### Strategic Metric Tiles

- Internal role fills (YTD)
- Women across workforce
- Women in leadership roles
- Women promoted YTD
- Women among new hires
- Women among departures
- Profit per FTE
- Department net income
- Open position ratio (Snapshot)
- High-potential share in senior roles (Snapshot)
- Succession cover in leadership (Snapshot)

### Charts

- Headcount by Department (bar)
- Gender Distribution (donut)
- Headcount by Location (bubble map)
- Terminations by Reason (bar)
- Tenure Distribution (bar)
- Women Representation Snapshot **or** Salary Distribution by Department (feature-flag switch)
- Performance Ratings (bar)

### Filters

- Department
- Location
- Status
- Report Year

All filters trigger one callback (`update_dashboard`) and refresh all KPI cards + charts together.

---

## Code Architecture (How `app.py` Works)

This is the high-level flow:

1. **Generate synthetic data** using NumPy/random (fixed seed for reproducibility).
2. **Create derived fields** (`tenure_years`, `tenure_band`, employee status from terminations).
3. **Build Dash layout** (header, filters, cards, charts, preview tables).
4. **Register callback** that:
   - reads filter values,
   - computes KPI numbers,
   - builds Plotly figures,
   - returns all outputs in one function.
5. **Run app** locally with `app.run(debug=True)`.

### Why separate tables?

Instead of putting everything in one employee table, the app uses event/fact tables:

- `df` (employee master)
- `terminations_df` (termination events)
- `internal_moves_df` (mobility events)
- `positions_df` (open/filled positions)
- `department_finance_df` (department finance by year)

This mirrors real analytics systems and makes KPI logic clearer (for example, attrition is based on termination events, not just employee status).

---

## Callback Walkthrough (`update_dashboard`)

This is the most important function in the app. It takes filter values as inputs and returns all KPI cards + chart figures.

### Step 1: Read filters and define period

- Inputs: `dept`, `loc`, `status`, `report_year`
- Convert `report_year` to integer
- Build `period_start` (`Jan 1`) and `period_end` (`Dec 31`) for the selected year

Why this matters: many HR metrics are period-based, so we need exact start/end dates.

### Step 2: Build analysis scopes

- `dff = apply_filters(...)` gives the main filtered employee dataset
- `employee_scope` is built from department/location filters to align event matching
- `terminations_year_scope` filters termination events to selected year + employee scope
- `positions_scope` and `finance_scope` are filtered separately because they come from different tables

Why this matters: each KPI should use the right table and the right scope, not just one global dataframe.

### Step 3: Compute headcount states for attrition denominator

- Find employee IDs hired before period start/end
- Remove IDs terminated before start/end
- Compute:
  - `start_headcount`
  - `end_headcount`
  - `average_headcount = (start + end) / 2`

Why this matters: average headcount is more stable and fair than using only start or end headcount.

### Step 4: Compute KPI numerators and rates

- `separations_in_period` from `terminations_year_scope`
- `voluntary_separations` from termination reason
- `turnover` and `voluntary_termination_ratio` both use `average_headcount`
- Women metrics use helper functions:
  - `pct(mask)` for simple percentages
  - `pct_with_denominator(num_mask, den_mask)` for ratio metrics with explicit denominator

Why this matters: the helper functions prevent duplicated logic and keep formulas readable.

### Step 5: Compute event-based and finance/position metrics

- Internal fills: count move events in selected year for employees in current scope
- Vacancy ratio: open positions / total positions from `positions_df`
- Profit metrics: finance totals from `department_finance_df` for selected year

Why this matters: this shows a practical mini data warehouse pattern (different fact tables feeding one dashboard).

### Step 6: Build UI component outputs

- Build `kpis` list (cards)
- Build `strategic_tiles` list
- Build each Plotly figure (`dept_bar`, `gender_pie`, `location_bar`, etc.)
- Return all outputs in the exact order declared in `@app.callback`

Why this matters: in Dash, output order must match return order exactly.

### Step 7: Feature-flagged middle chart

- If `SHOW_SALARY = True`: show salary distribution by department
- Else: show women representation snapshot

Why this matters: this is a clean way to swap features without rewriting layout logic.

---

## KPI Calculations (Explained)

### Scope legend

- **Filtered scope**: applies current Department / Location / Status filters
- **Year scope**: applies selected Report Year period
- **Year-end scope**: applies selected Report Year as-of `Dec 31`
- **Snapshot metrics**: current-state only where no historical table exists

### Core formulas used in code

- **Currently Active (as of year-end)**
  - Count employees active on `Dec 31` of `report_year`
  - Uses `hire_date` and termination events to rebuild status as-of year-end

- **Terminations (Report Year)**
  - Count rows in `terminations_df` where `termination_date.year == report_year`
  - Then match to filtered employee scope

- **Attrition (%)**
  - `attrition = separations_in_period / average_headcount * 100`
  - `average_headcount = (start_headcount + end_headcount) / 2`
  - This is a standard HR approach because it avoids bias from growth/shrink during the year

- **Voluntary termination ratio (Report Year) (%)**
  - `voluntary_separations / average_headcount * 100`
  - Same denominator as attrition for consistency

- **Average Service (as of year-end)**
  - For each employee in year-end scope: `(period_end - hire_date)` in years
  - KPI is the mean of that year-end tenure

- **Internal role fills (YTD)**
  - Count internal move events in selected year for employees in filtered scope
  - Divide by filtered employee count

- **Women across workforce**
  - Female share in year-end scope (`as of Dec 31` for selected year)

- **Women in leadership / promotions / hires / departures**
  - Each metric uses `numerator / denominator` with context-specific denominator
  - Example: women in leadership = women in senior roles / all senior roles

- **Open position ratio (%)**
  - `open_positions / total_positions * 100`
  - Uses `positions_df` filtered by department/location
  - Labeled **(Snapshot)** because there is no position-status history by year

- **High-potential share in senior roles / Succession cover in leadership**
  - Computed from current employee attributes in filtered scope
  - Labeled **(Snapshot)** because there is no historical effective-dated table

- **Profit per FTE**
  - `department_net_income / department_fte`
  - Uses selected report year, optional department filter

---

## Chart Logic (How to Explain It)

- **Department colors**: neutral palette by default; accent yellow highlights the largest department.
- **Women Representation Snapshot**: `Workforce` bar intentionally uses accent yellow for emphasis.
- **Gender donut**: explicit color map for stable category colors across filter changes.
- **Location map**: bubble size = headcount, custom geo styling for cleaner borders.
- **Performance bars**: explicit map (`Exceeds`, `Meets`, `Below`) so colors are consistent every run.

Tip for presentations: explain each chart as *question → calculation → visual encoding*.

Example:
- Question: “Where is our workforce concentrated?”
- Calculation: count employees by location
- Encoding: map marker size and color by count

---

## Synthetic Data Preview & Verification

The app includes a **Synthetic Data Preview** section with top rows and CSV download for each table:

- Employees
- Terminations
- Internal Moves
- Positions
- Department Finance

Use this to verify KPI calculations manually in Excel/Pandas when learning.

---

## Tech Stack (Why these tools)

| Tool | Why it is used |
|---|---|
| Dash | Python-first web UI framework with reactive callbacks |
| Plotly Express | Quick interactive chart creation with clean APIs |
| Pandas | Filtering, grouping, and KPI math |
| NumPy + random | Fast synthetic data generation with controlled distributions |
| Gunicorn | Production web server for Render deployment |

---

## Quick Start (Local)

```bash
# 1) Clone
git clone https://github.com/HYHYHYHYHYHYHYHYHY/hr-workforce-dashboard.git
cd hr-workforce-dashboard

# 2) Install deps
pip install -r requirements.txt

# 3) Run app
python app.py
```

Open: **http://127.0.0.1:8050**

---

## Deployment (Render)

1. Connect the repo as a **Web Service**
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn app:server`
4. Deploy

`server = app.server` exposes the Flask server object required by Gunicorn.

---

## Project Structure

```text
hr-workforce-dashboard/
├── app.py            # Data generation + layout + callbacks
├── requirements.txt  # Dependencies
└── README.md         # Project and learning documentation
```

---

## Suggested Talking Track (for interviews / demos)

1. Start with **business objective**: monitor workforce health and talent pipeline.
2. Explain **data model**: event tables separated from employee master.
3. Walk through **one KPI deeply** (attrition with average headcount denominator).
4. Show **interactive filtering** and how one callback drives the whole dashboard.
5. Highlight **engineering choices**: reproducible synthetic data, explicit color maps, downloadable source tables.

---

Built as a portfolio and learning project with synthetic data only.
