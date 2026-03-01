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
| Total Employees | Filtered headcount |
| Active / Terminated | Status split |
| Turnover Rate | % terminated of total |
| Avg Salary | Mean salary (USD) |
| Avg Tenure | Mean years of service |

### Charts
- Headcount by Department (bar)
- Gender Distribution (donut)
- Headcount by Location (horizontal bar)
- Tenure Distribution by band (bar)
- Salary Distribution by Department (box plot)
- Performance Ratings (bar)

### Filters
Department, Location, and Status dropdowns — all charts update reactively.

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

The dashboard uses **300 synthetic employee records** generated with a fixed random seed (`42`) — fully reproducible and privacy-safe. No real employee data is used.

**Fields:** `employee_id`, `name`, `department`, `location`, `gender`, `status`, `hire_date`, `salary`, `age`, `performance`, `tenure_years`, `tenure_band`

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
- Multi-chart layouts with Plotly Express (bar, pie/donut, box, horizontal bar)
- KPI card components with conditional colour coding
- Clean, Power BI-inspired colour palette and layout
- Production deployment with Gunicorn on Render
- Portfolio integration via iframe embed

---

*Built as a portfolio project — sample data only.*
