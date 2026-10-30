# BlogSphere – Blogging Platform Using Flask

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.1-red.svg)](https://www.sqlalchemy.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()
[![Internship](https://img.shields.io/badge/Internship-Week%203%20Completed-orange.svg)]()

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
| **Testing** | Pytest 8.2 (18 automated tests passing) |
| **Version Control** | Git, GitHub (`https://github.com/sidhesh1010/Blogging_Platform`) |

---

## 📂 Project Architecture

```
Blogging_Platform/
│
├── app/
│   ├── __init__.py          # Application Factory (create_app), extension initialization
│   ├── auth.py              # Authentication Blueprint (login, register, logout, profile)
│   ├── posts.py             # Blog Post CRUD Blueprint (create, detail, edit, delete)
│   ├── models.py            # SQLAlchemy models (User, BlogPost, ContactMessage)
│   ├── forms.py             # WTForms (RegistrationForm, LoginForm, PostForm, UpdateProfileForm)
│   ├── routes.py            # Core routes (index, about, contact)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Custom design system, typography & card animations
│   │   └── js/
│   │       └── main.js      # Auto-dismiss alerts, category filter, client UI
│   └── templates/
│       ├── base.html        # Jinja2 master layout with sticky navbar, alerts & footer
│       ├── index.html       # Hero section, category pills, live post cards & spotlight
│       ├── about.html       # Project mission, technology matrix & 8-week roadmap
│       ├── contact.html     # Interactive contact form backed by SQLite database
│       ├── login.html       # Secure login portal with remember-me
│       ├── register.html    # Author registration with validation
│       ├── profile.html     # Author profile management & published stories list
│       ├── create_post.html # Rich story creation interface with live word count & preview
│       ├── edit_post.html   # Author story editor with delete modal confirmation
│       └── post_detail.html # Medium-style reading layout with related stories
│
├── instance/
│   └── blogsphere.db        # SQLite database (auto-generated, git-ignored)
├── tests/
│   ├── test_week1.py        # Automated tests: Factory, routes & SQLite
│   ├── test_week2.py        # Automated tests: User auth, passwords, profile
│   └── test_week3.py        # Automated tests: Blog post CRUD & author guards
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

## 🚀 Milestones Progress

### ✅ Week 1: Setup & Architecture
1. **Python Virtual Environment:** Created isolated environment (`venv`) using Python 3.12.
2. **Dependencies Installed:** Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF, Werkzeug, Pytest.
3. **Application Factory Pattern:** Structured `app/__init__.py` with `create_app()`.
4. **SQLite & SQLAlchemy:** Dynamic `DATABASE_URL` with fallback to `sqlite:///blogsphere.db`.
5. **Database Model:** Implemented `ContactMessage` model in `app/models.py`.
6. **Master Layout & Pages:** `base.html`, `index.html`, `about.html`, `contact.html`.
7. **Automated Testing:** 4 passing tests in `tests/test_week1.py`.

### ✅ Week 2: User Authentication & Profiles
1. **User Model:** Implemented `User` model with Werkzeug secure password hashing (`scrypt`).
2. **Session Management:** Flask-Login integration (`@login_required`, `current_user`, session cookies).
3. **Registration & Login:** Forms with email/username uniqueness checks and validation.
4. **Author Profiles:** Edit username and bio, dynamic Gravatar generation, security overview.
5. **CSRF Protection:** Integrated Flask-WTF CSRF tokens on all form submissions.
6. **Automated Testing:** 6 passing tests in `tests/test_week2.py`.

### ✅ Week 3: Blog Post CRUD & Author Safeguards
1. **BlogPost Model:** Relational schema linked to `User` via foreign key and cascade deletion.
2. **Helper Properties:** Clean text snippet generator (`snippet()`), reading time estimator (`read_time()`), category fallback images (`default_image()`).
3. **Story Creation (`/post/create`):** Rich editorial template with live character/word count, dynamic reading time, category selection, and live image preview.
4. **Story Reading (`/post/<id>`):** Medium-like reading layout with breadcrumbs, author profile card, like/clap counter, social share triggers, and related articles.
5. **Story Editing (`/post/<id>/edit`):** Author-restricted editing route (`post.author == current_user` safeguard returning 403 Forbidden for unauthorized users).
6. **Story Deletion (`/post/<id>/delete`):** Secure POST deletion with confirmation modal and author authorization check.
7. **Homepage & Profile Integration:** Real database stories dynamically populated on the homepage with graceful fallback; profile lists author's stories with quick edit/delete controls.
8. **Automated Testing:** 8 passing tests in `tests/test_week3.py` (18 total across test suite).

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
- [x] **Week 2:** User Authentication (Flask-Login, Password Hashing, CSRF Protection, Profile Management)
- [x] **Week 3:** Blog Post CRUD Functionality (Rich Text Editor, Author Restrictions)
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
