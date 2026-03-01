# HR Workforce Dashboard

An interactive HR Workforce Dashboard built with **Python**, **Plotly Dash**, and **Pandas**.
Designed as a portfolio project to demonstrate data visualisation and analytics skills
comparable to Power BI / Tableau — but fully open-source and shareable via a single Python file.

---

## Features

| KPI Card | Description |
|---|---|
| Total Employees | Filtered headcount |
| Active / Terminated | Status split |
| Turnover Rate | % terminated of total |
| Avg Salary | Mean salary (USD) |
| Avg Tenure | Mean years of service |

**Charts**
- Headcount by Department (bar)
- Gender Distribution (donut)
- Headcount by Location (horizontal bar)
- Tenure Distribution by band (bar)
- Salary Distribution by Department (box plot)
- Performance Ratings (bar)

**Filters** — Department, Location, Status (all charts update reactively)

---

## Tech Stack

| Library | Purpose |
|---|---|
| [Dash](https://dash.plotly.com/) | Web framework & reactive callbacks |
| [Plotly Express](https://plotly.com/python/plotly-express/) | Interactive charts |
| [Pandas](https://pandas.pydata.org/) | Data wrangling |
| [NumPy](https://numpy.org/) | Random sample generation |

---

## Quick Start

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

## Sample Data

The dashboard uses **300 synthetic employee records** generated with a fixed random seed (42)
so results are fully reproducible. No real employee data is used.

Fields: `employee_id`, `name`, `department`, `location`, `gender`, `status`,
`hire_date`, `salary`, `age`, `performance`, `tenure_years`, `tenure_band`

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
- Data wrangling with Pandas (groupby, cut, value_counts)
- Multi-chart layouts with Plotly Express (bar, pie/donut, box, horizontal bar)
- KPI card components with conditional colour coding
- Clean, Power BI-inspired colour palette and layout

---

*Built as a portfolio project — sample data only.*
