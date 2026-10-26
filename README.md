# Nisha Rani Singha - Professional Django Portfolio & Data Science Showcase

A modern, responsive, and dynamic personal portfolio website built with **Django 6**, showcasing academic achievements, data science projects, technical competencies, and an interactive **Machine Learning Customer Segmentation (RFM & K-Means)** live demo.

---

## 🌟 Overview & Information from CV

- **Name:** Nisha Rani Singha
- **Location:** Dhaka, Bangladesh
- **Contact:** nishasingha277@gmail.com | 01609439468
- **Education:** Bachelor of Computer Science and Engineering, Northern University Bangladesh (DEC 2024 – DEC 2027) | **CGPA: 3.75**
- **Specialization:** Python, Data Analysis (NumPy, Pandas), Statistics & Probability, Machine Learning (Scikit-learn), Exploratory Data Analysis (EDA)
- **Certification:** Ostad Data Science Course
- **Extracurricular Activities:** Participation in Programming Contests, Research Interest in Collective Behaviour

---

## 🚀 Key Features

1. **Modern Responsive Design**: Dark-mode aesthetic with glassmorphism navigation, animated skill progress bars, and mobile-ready layout using Bootstrap 5.3 & FontAwesome 6.
2. **Interactive Live Machine Learning Demo**:
   - Live **RFM & K-Means Customer Segmentation** simulator.
   - Real-time prediction powered by backend clustering algorithms.
   - Dynamic 2D scatter plot visualizer built with **Chart.js**.
   - Preset customer personas (*VIP Champions, Loyal Customers, Potential Loyalists, At-Risk*).
3. **Comprehensive CV Sections**:
   - **Hero & Profile**: Name, bio, photo, location, contact, and quick status.
   - **Academic Credentials**: Northern University Bangladesh degree details (CGPA 3.75).
   - **Professional Certifications**: Ostad Data Science training.
   - **Categorized Skills**: Programming (Python, Django), Data Analysis (Pandas, NumPy, EDA, Preprocessing), Machine Learning (Scikit-learn, Model Training, K-Means), Statistics & Probability, and Core Tools (Jupyter, Git).
   - **Projects Portfolio**: Detailed case studies for *Customer Segmentation Using RFM & K-Means*, *Exploratory Data Analysis (EDA)*, and *Data Analysis Using Pandas*.
   - **Extracurricular & Research**: Competitive Programming & Collective Behaviour research.
   - **Interactive Contact Form**: Stores inquiries directly in SQLite database with feedback notifications.
4. **Django Admin Panel**:
   - Manage Profile details, Education, Skills, Projects, Certifications, and view Contact Messages at `/admin/`.

---

## 📁 Project Structure

```text
nisha_portfolio/
│
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
│
├── portfolio_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── portfolio/
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── management/
│   │   └── commands/
│   │       └── seed_portfolio.py
│   ├── static/
│   │   └── portfolio/
│   │       ├── css/style.css
│   │       ├── js/main.js
│   │       └── images/profile.jpg
│   └── templates/
│       └── portfolio/
│           ├── base.html
│           ├── index.html
│           └── project_detail.html
│
└── media/
    └── profile/
        └── profile.jpg
```

---

## ⚡ Quick Start Guide

### 1. Navigate to the Project Directory
```powershell
cd "C:\Users\HP\.gemini\antigravity\scratch\nisha_portfolio"
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run Migrations & Seed Initial CV Data
```powershell
python manage.py migrate
python manage.py seed_portfolio
```

### 4. Start the Django Development Server
```powershell
python manage.py runserver
```
Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

---

## 🔐 Admin Dashboard

To access the Django Admin management panel:
- **URL:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Username:** `admin`
- **Password:** `admin1234`
