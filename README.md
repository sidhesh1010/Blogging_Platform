# BlogSphere – Blogging Platform Using Flask

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.1-red.svg)](https://www.sqlalchemy.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()
[![Internship](https://img.shields.io/badge/Internship-Week%201%20Completed-orange.svg)]()

> A modern, responsive, and secure full-stack blogging platform developed as part of an **8-Week Technical Internship Program**.

---

## 📌 Project Overview

**BlogSphere** is engineered to empower writers, developers, and thinkers to craft and share ideas effortlessly. Inspired by modern publishing platforms like Medium, BlogSphere combines clean editorial aesthetics with a robust, enterprise-grade Python Flask backend.

### Project Objectives
- **Authentication & Security:** Multi-user registration, secure password hashing (Werkzeug), and CSRF token protection.
- **Content Management:** Create, Read, Update, and Delete (CRUD) rich blog posts with formatting and categorization.
- **Community Engagement:** Interactive comment threads and author-reader interactions.
- **Discovery:** Category filtering, tag searching, and server-side pagination.
- **Production Readiness:** Configurable for local SQLite development and zero-downtime PostgreSQL deployment.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.12, Flask 3.0.3, Werkzeug 3.0.3 |
| **Database & ORM** | Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.1, SQLite / PostgreSQL |
| **Database Migrations** | Flask-Migrate 4.0.7, Alembic |
| **Authentication & Forms**| Flask-Login, Flask-WTF, WTForms, email-validator |
| **Frontend** | HTML5, Jinja2 Templates, Bootstrap 5.3, Bootstrap Icons, Custom CSS3 |
| **Testing** | Pytest 8.2 |
| **Version Control** | Git, GitHub (`https://github.com/sidhesh1010/Blogging_Platform`) |

---

## 📂 Project Architecture

```
Blogging_Platform/
│
├── app/
│   ├── __init__.py          # Application Factory (create_app), extension initialization
│   ├── models.py            # SQLAlchemy database models (ContactMessage, User, BlogPost)
│   ├── routes.py            # Application routes & Blueprint handlers
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Custom design system, typography & card animations
│   │   └── js/
│   │       └── main.js      # Auto-dismiss alerts, category filter, client UI
│   └── templates/
│       ├── base.html        # Jinja2 master layout with sticky navbar, alerts & footer
│       ├── index.html       # Hero section, category pills, featured spotlight & cards
│       ├── about.html       # Project mission, technology matrix & 8-week roadmap
│       └── contact.html     # Interactive contact form backed by SQLite database
│
├── instance/
│   └── blogsphere.db        # SQLite database (auto-generated, git-ignored)
├── tests/
│   └── test_week1.py        # Automated test suite verifying routes and database
├── venv/                    # Isolated Python virtual environment (git-ignored)
├── .env.example             # Template for configuration environment variables
├── .gitignore               # Comprehensive exclusion rules for Python & Flask
├── config.py                # Environment-driven configuration class
├── pytest.ini               # Pytest root configuration
├── requirements.txt         # Pinned production and development dependencies
├── run.py                   # Application entry point & local development server
└── README.md                # Project documentation and internship report
```

---

## 🚀 Week 1 Milestone: Setup & Architecture

### Tasks Completed in Week 1:
1. ✅ **Python Virtual Environment:** Created isolated environment (`venv`) using Python 3.12.
2. ✅ **Dependencies Installed:** Configured and installed Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF, Werkzeug, and Pytest.
3. ✅ **Application Factory Pattern:** Structured `app/__init__.py` using the `create_app()` factory pattern for scalable modular growth.
4. ✅ **SQLite & SQLAlchemy:** Configured `config.py` with dynamic `DATABASE_URL` fallback to `sqlite:///blogsphere.db`.
5. ✅ **Database Model:** Implemented `ContactMessage` model in `app/models.py` to verify database table creation and persistence.
6. ✅ **Modular Routing:** Configured `main` Flask Blueprint in `app/routes.py`.
7. ✅ **Jinja2 Master Layout:** Built `base.html` with Bootstrap 5.3, Bootstrap Icons, custom Google Fonts (`Outfit` & `Plus Jakarta Sans`), and toast alerts.
8. ✅ **Responsive Homepage:** Designed `index.html` with hero banner, live stats, category filtering, and responsive article cards.
9. ✅ **About & Contact Pages:** Created `about.html` (featuring the 8-week roadmap) and `contact.html` (connected to SQLite database).
10. ✅ **Static Assets:** Created `style.css` (custom design tokens and hover effects) and `main.js` (client interactions and alert dismissal).
11. ✅ **Automated Testing:** Implemented and passed all 4 test cases in `tests/test_week1.py` with 100% pass rate.
12. ✅ **Git Architecture:** Prepared `.gitignore`, `requirements.txt`, and `.env.example`.

---

## 💻 Local Setup & Execution Guide

Follow these steps to run the application locally on Windows (PowerShell):

### 1. Clone the Repository
```powershell
git clone https://github.com/sidhesh1010/Blogging_Platform.git
cd Blogging_Platform
```

### 2. Activate Virtual Environment
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1
```
*(If you are setting up fresh on another machine: run `python -m venv venv` first, then activate).*

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run the Application
```powershell
python run.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

### 5. Run Automated Tests
```powershell
pytest -v
```

---

## 📅 8-Week Internship Development Roadmap

- [x] **Week 1:** Flask Setup, Application Factory, SQLite & Base Architecture
- [ ] **Week 2:** User Authentication (Flask-Login, Password Hashing, CSRF Protection)
- [ ] **Week 3:** Blog Post CRUD Functionality (Rich Text Editor, Author Restrictions)
- [ ] **Week 4:** Responsive Frontend Polish & Medium-like Reading Interface
- [ ] **Week 5:** Interactive Commenting System & Moderation
- [ ] **Week 6:** Full-Text Search, Tag Filtering & Server-Side Pagination
- [ ] **Week 7:** Automated Testing Suite & Production Deployment Preparation
- [ ] **Week 8:** Final Demonstration Video, Documentation & Internship Submission

---

## 👨‍💻 Author & Repository
- **Developer:** Sidhesh
- **Repository:** [https://github.com/sidhesh1010/Blogging_Platform](https://github.com/sidhesh1010/Blogging_Platform)
- **License:** MIT License
