# Athlete Performance Tracker & Injury Risk Analyzer

A full-stack web application built with Python and Flask that helps coaches monitor athlete training loads and predict injury risk using the Acute:Chronic Workload Ratio (ACWR) model.

---

## Features

- **Role-based authentication** — separate dashboards for coaches and athletes
- **Workout logging** — athletes log daily sessions with type, duration, and intensity
- **Wellness check-ins** — daily tracking of sleep, soreness, mood, and resting heart rate
- **ACWR injury risk model** — calculates acute and chronic training loads to predict injury risk
- **Interactive charts** — Chart.js visualizations of training load trends over 28 days
- **Coach dashboard** — real-time risk badges (Low / Optimal / Moderate / High) for all assigned athletes

---

## Technologies Used

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Web Framework | Flask |
| Database ORM | SQLAlchemy |
| Database | SQLite |
| Authentication | Flask-Login + Werkzeug |
| Data Processing | Pandas + NumPy |
| Visualization | Chart.js |
| Frontend | Jinja2 + Bootstrap 5 |

---

## Project Structure

```
perform_tracker/
├── app/
│   └── ml/
│       ├── acwr.py                 # Acute:Chronic Workload Ratio calculations
│       ├── __init__.py
│       ├── models.py
│       └── routes.py
├── instance/
│   └── perform_tracker.db          # Local SQLite database
├── templates/                      # HTML templates
│   ├── athlete/
│   ├── athlete_dashboard.html
│   ├── base.html
│   ├── coach_dashboard.html
│   ├── login.html
│   └── register.html
├── tests/                          # Unit tests
│   ├── __init__.py
│   └── test_app.py
├── .gitignore
├── config.py                       # App configuration settings
├── requirements.txt                # Python dependencies
├── run.py                          # Application entry point
└── seed_data.py                    # Database seeding script
```

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Melnik31/apt.git
cd apt
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Mac/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize the database
```bash
python -c "
from app import create_app, db
from app import models
app = create_app()
with app.app_context():
    db.create_all()
    print('Database created!')
"
```

### 5. Seed demo data
```bash
python seed_data.py
```

This creates:
- 1 coach account
- 5 athletes with 28 days of workout and wellness data
- Each athlete has a different risk profile (Low, Optimal, Moderate, High)

### 6. Run the application
```bash
python run.py
```

Visit `http://127.0.0.1:5000/register` in your browser.

---

## Demo Login Credentials

| Role | Username | Password |
|---|---|---|
| Coach | coach1 | password |
| Athlete (Optimal) | Abby T | password |
| Athlete (High Risk) | John T | password |
| Athlete (Moderate) | Taylor K | password |
| Athlete (Low) | Alex M | password |
| Athlete (High Risk) | Sam R | password |

---

## How the ACWR Model Works

The **Acute:Chronic Workload Ratio (ACWR)** is a sports science model used by professional teams worldwide to manage athlete training load and reduce injury risk.

**Training Load** is calculated per session:
```
Training Load = Duration (minutes) × Intensity (1–10)
```

**ACWR Formula:**
```
Acute Load  = average daily training load over last 7 days
Chronic Load = average daily training load over last 28 days
ACWR = Acute Load ÷ Chronic Load
```

**Risk Thresholds:**

| ACWR Value | Risk Level | Meaning |
|---|---|---|
| < 0.8 | Low | Athlete is undertraining |
| 0.8 – 1.3 | Optimal | Safe training zone |
| 1.3 – 1.5 | Moderate | Workload spiking — monitor closely |
| > 1.5 | High | Danger zone — elevated injury risk |

**Reference:**
White, R. (2019, May 7). Acute:Chronic Workload Ratio | Science for Sport. Science for Sport. 

[https://www.scienceforsport.com/acutechronic-workload-ratio/](url)
---

## Known Limitations

- **New user problem** — athletes with less than 7 days of data will show inaccurate ACWR values since the chronic load baseline is too low
- **Self-reported data** — intensity and wellness scores are subjective and depend on honest user input
- **SQLite** — not suitable for production use with multiple concurrent users; PostgreSQL recommended for deployment
- **No real-time alerts** — coaches must manually check the dashboard; push notifications are not implemented

---

## Future Improvements

- Email or SMS alerts when an athlete enters the High risk zone
- Scikit-learn classifier combining ACWR + wellness features for a composite risk score
- Athlete detail page with full chart history accessible from the coach dashboard
- PostgreSQL support for production deployment
- Mobile-responsive design improvements

---

## Running Tests

```bash
pytest tests/
```
