# HR Workforce Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Dash](https://img.shields.io/badge/Plotly%20Dash-2.14+-informational?logo=plotly&logoColor=white)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

An interactive HR Workforce Dashboard built with **Python**, **Plotly Dash**, and **Pandas**. Designed as a portfolio project to demonstrate data visualisation and analytics skills comparable to Power BI / Tableau — but fully open-source and deployable via a single Python file.

> 🔴 **[View Live Demo](https://hr-workforce-dashboard.onrender.com)** — fully interactive, hosted on Render (free tier; may take ~30s to wake up)

---

## Screenshot

> *(Add a screenshot of your dashboard here — drag and drop an image into this README)*

---

## Features

### KPI Cards
| KPI Card | Description |
|---|---|
| Team Size | Filtered headcount |
| Currently Active / Separated | Current status split |
| Attrition | Share of separations |
| Average Service | Mean years of service |
| Strategic People Metrics | Women representation, internal fills, vacancy pressure, succession coverage |

### Charts
- Headcount by Department (bar)
- Gender Distribution (donut)
- Headcount by Location (bubble map)
- Terminations by Reason (bar)
- Tenure Distribution by band (bar)
- Women Representation Snapshot (bar)
- Performance Ratings (bar)

### Filters
Department, Location, Status, and Report Year dropdowns — all charts update reactively.

### Synthetic Data Preview & Verification
- In-app **Synthetic Data Preview** section shows top rows for:
  - Employees table
  - Internal Moves table
  - Terminations table
  - Positions table
  - Department Finance table
- One-click CSV export buttons are available for each table to audit KPI calculations externally.

### KPI Formula Definitions
Scope legend: **filtered** = current dashboard filters (`Department`, `Location`, `Status`, `Report Year` where applicable); **company-wide** = entire dataset regardless of filters.

- **Team Size** = count of filtered employees. *(Scope: filtered)*
- **Currently Active** = count where `status == "Active"` in filtered employees. *(Scope: filtered)*
- **Separated** = count where `status == "Terminated"` in filtered employees. *(Scope: filtered)*
- **Terminations (Year)** = count of termination events in selected `report_year`. *(Scope: employees filtered by department/location)*
- **Attrition (%)** = `separations_in_period / average_headcount * 100`, where `average_headcount = (headcount_at_period_start + headcount_at_period_end) / 2`. *(Scope: employees filtered by department/location; selected report year for separations)*
- **Average Service** = mean of `tenure_years` in filtered employees. *(Scope: filtered)*
- **Internal role fills (YTD) (%)** = `internal_moves_in_selected_year_for_filtered_employees / filtered_employee_count * 100`. *(Scope: filtered denominator; selected-year events matched to filtered employees)*
- **Women in leadership roles (%)** = `women_in_senior_roles / total_senior_roles * 100`. *(Scope: filtered)*
- **Women promoted this year (%)** = `women_promoted / total_promoted * 100`. *(Scope: filtered)*
- **Women among new hires (%)** = `women_hired_in_report_year / total_hired_in_report_year * 100`. *(Scope: filtered + selected report year)*
- **Women among departures (%)** = `women_exits / total_exits * 100`. *(Scope: filtered; departures sourced from terminations table in selected report year)*
- **Open-role pressure (%)** = `open_positions / total_positions` (filtered by department/location) `* 100`. *(Scope: positions table filtered by department/location only)*
- **Profit per FTE** = `department_net_income / department_fte`. *(Scope: department finance table, selected report year, optionally department-filtered)*

---

## Tech Stack

| Library | Purpose |
|---|---|
| Dash | Web framework & reactive callbacks |
| Plotly Express | Interactive charts |
| Pandas | Data wrangling |
| NumPy | Random sample generation |
| Gunicorn | Production WSGI server (Render deployment) |

---

## Quick Start (Local)

```bash
# 1. Clone the repo
git clone https://github.com/HYHYHYHYHYHYHYHYHY/hr-workforce-dashboard.git
cd hr-workforce-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
python app.py
```

Then open your browser at **http://127.0.0.1:8050**

---

## Deployment (Render)

This app is production-ready for deployment on [Render](https://render.com) (free tier).

1. Connect your GitHub repo to Render as a **Web Service**
2. Set **Build command:** `pip install -r requirements.txt`
3. Set **Start command:** `gunicorn app:server`
4. Deploy — Render provides a public URL automatically

The `server = app.server` line in `app.py` exposes the underlying Flask server object that Gunicorn needs.

---

## Portfolio Embed (GitHub Pages / Portfolio Site)

To embed this dashboard as a live, interactive component on your portfolio page:

```html
<iframe
  src="https://hr-workforce-dashboard.onrender.com"
  width="100%"
  height="800px"
  frameborder="0"
  style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
</iframe>
```

> **Why iframe?** Visitors get a fully interactive dashboard without leaving your portfolio page — no installs, no downloads. Recruiters see your skills in action immediately.

---

## Sample Data

The dashboard uses synthetic, reproducible sample data (seed `42`) — privacy-safe and suitable for demos.

**Employees table (`df`) fields:** `employee_id`, `name`, `department`, `location`, `gender`, `status`, `hire_date`, `salary`, `age`, `performance`, `tenure_years`, `tenure_band`, `is_senior_role`, `promoted_ytd`, `high_potential`, `successor_ready`

**Internal moves table (`internal_moves_df`) fields:** `employee_id`, `move_date`, `move_type`

**Terminations table (`terminations_df`) fields:** `employee_id`, `termination_date`, `termination_reason`

**Positions table (`positions_df`) fields:** `position_id`, `department`, `location`, `is_open`

**Department finance table (`department_finance_df`) fields:** `report_year`, `department`, `department_fte`, `department_net_income`

---

## Project Structure

```
hr-workforce-dashboard/
├── app.py            # Main dashboard application
├── requirements.txt  # Python dependencies
└── README.md
```

---

## Skills Demonstrated

- Interactive dashboard design (filter-driven reactive updates)
- Data wrangling with Pandas (`groupby`, `cut`, `value_counts`)
- Multi-chart layouts with Plotly Express (bar, pie/donut, horizontal bar)
- KPI card components with conditional colour coding
- Clean, Power BI-inspired colour palette and layout
- Production deployment with Gunicorn on Render
- Portfolio integration via iframe embed

---

*Built as a portfolio project — sample data only.*
