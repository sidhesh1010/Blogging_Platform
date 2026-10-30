# BlogSphere – Blogging Platform Using Flask

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.1-red.svg)](https://www.sqlalchemy.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![Tests](https://img.shields.io/badge/Tests-Passing%20(41)-brightgreen.svg)]()
[![Internship](https://img.shields.io/badge/Internship-Week%206%20Completed-orange.svg)]()

> A modern, responsive, and secure full-stack blogging platform developed as part of an **8-Week Technical Internship Program**.

---

## 📌 Project Overview

**BlogSphere** is engineered to empower writers, developers, and thinkers to craft and share ideas effortlessly. Inspired by modern publishing platforms like Medium, BlogSphere combines clean editorial aesthetics with a robust, enterprise-grade Python Flask backend.

### Project Objectives
- **Authentication & Security:** Multi-user registration, secure password hashing (Werkzeug), and CSRF token protection.
- **Content Management:** Create, Read, Update, and Delete (CRUD) rich blog posts with formatting and categorization.
- **Reading Experience:** Medium-inspired clean typography, reading progress bar, reader mode controls, and dark theme.
- **Community Engagement:** Interactive comment threads, author moderation, clap counters, and article bookmarks.
- **Discovery:** Real-time search filtering, category tabs, and server-side pagination.
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
| **Testing** | Pytest 8.2 (41 automated tests passing) |
| **Version Control** | Git, GitHub (`https://github.com/sidhesh1010/Blogging_Platform`) |

---

## 📂 Project Architecture

```
Blogging_Platform/
│
├── app/
│   ├── __init__.py          # Application Factory (create_app), extension initialization
│   ├── auth.py              # Authentication Blueprint (login, register, logout, profile)
│   ├── posts.py             # Blog Post & Comment CRUD Blueprint (create, detail, edit, delete, comment)
│   ├── models.py            # SQLAlchemy models (User, BlogPost, Comment, ContactMessage)
│   ├── forms.py             # WTForms (RegistrationForm, LoginForm, PostForm, CommentForm, UpdateProfileForm)
│   ├── routes.py            # Core routes, search/filtering/pagination & error handlers (404, 403, 500)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Design system, dark theme tokens, reading progress & animations
│   │   └── js/
│   │       └── main.js      # Dark mode toggle, progress bar, reader controls & live search
│   └── templates/
│       ├── base.html        # Jinja2 master layout with theme toggle, progress bar & back-to-top
│       ├── index.html       # Hero section, server & live search, category pills & dynamic cards
│       ├── about.html       # Project mission, technology matrix & 8-week roadmap
│       ├── contact.html     # Interactive contact form backed by SQLite database
│       ├── login.html       # Secure login portal with remember-me
│       ├── register.html    # Author registration with validation
│       ├── profile.html     # Author profile management, published stories & comment stats
│       ├── create_post.html # Rich story creation interface with live word count, tags & preview
│       ├── edit_post.html   # Author story editor with tags & delete modal confirmation
│       ├── post_detail.html # Medium-style reading layout with discussion thread, tags & reader tools
│       └── errors/
│           ├── 404.html     # Custom responsive Page Not Found view
│           ├── 403.html     # Custom responsive Forbidden Access view
│           └── 500.html     # Custom responsive Server Error view
│
├── instance/
│   └── blogsphere.db        # SQLite database (auto-generated, git-ignored)
├── tests/
│   ├── test_week1.py        # Automated tests: Factory, routes & SQLite
│   ├── test_week2.py        # Automated tests: User auth, passwords, profile
│   ├── test_week3.py        # Automated tests: Blog post CRUD & author guards
│   ├── test_week4.py        # Automated tests: Reading interface, themes & error views
│   ├── test_week5.py        # Automated tests: Comment threads, validation & author moderation
│   └── test_week6.py        # Automated tests: Search, tag filtering, sorting & server pagination
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
8. **Automated Testing:** 8 passing tests in `tests/test_week3.py`.

### ✅ Week 4: Responsive Frontend Polish & Medium-like Reading Interface
1. **Dark Mode Theme Engine:** Dual-palette CSS variables with `localStorage` persistence and 1-click animated theme switcher in navbar.
2. **Medium-Style Reading Experience:** Dynamic reading progress bar showing exact scroll percentage across article pages.
3. **Reader Customization Toolbar:** Font size toggling (small/default/large), typography switching (modern sans vs editorial serif), and column width expansion.
4. **Interactive Engagement & Bookmarks:** Heart/clap counter with animated heartbeat pulse and local-storage powered article bookmarking.
5. **1-Click Code Block Copy:** Automatically attaches clipboard copy buttons to code snippets with live tooltip feedback.
6. **Real-Time Live Search:** Instant keyword filter on the homepage matching titles, categories, and authors with empty results fallback.
7. **Custom Responsive Error Pages:** Polished error views for 404 (Not Found), 403 (Forbidden), and 500 (Internal Server Error).
8. **Automated Testing:** 6 passing tests in `tests/test_week4.py`.

### ✅ Week 5: Interactive Commenting System & Moderation
1. **Comment Model:** Relational schema linking reader comments to `User` and `BlogPost` with cascade deletion on user or post deletion.
2. **Comment Form & Validation:** `CommentForm` with content length constraints (3 to 1000 characters) and CSRF protection.
3. **Discussion Thread UI:** Embedded responsive comment thread in `post_detail.html` with jump link in engagement bar.
4. **Author Moderation Privileges:** Dual authorization allowing either the comment author OR the blog post author (moderator) to delete comments (`403 Forbidden` for non-authorized users).
5. **Profile & Feed Indicators:** Dynamic reader response counters on user profiles (`user.comments.count()`) and feed article cards.
6. **Automated Testing:** 8 passing tests in `tests/test_week5.py`.

### ✅ Week 6: Full-Text Search, Tag Filtering & Server-Side Pagination
1. **Multi-Field Full-Text Search:** Case-insensitive search querying title, content, tags, category, and author username (`.ilike()`).
2. **Category & Tag Filtering:** Dynamic category filter pills and `#tag` keyword filtering across stories.
3. **Multi-Criteria Sorting:** Sort by `Newest First`, `Oldest First`, and `Most Discussed` (popular comment count descending).
4. **Server-Side Pagination:** Integrated SQLAlchemy `.paginate(page=p, per_page=6)` with numbered page links, Next/Prev navigation, and current page stats.
5. **State Preservation:** Search query `q`, active category, tag filter, and sort order are preserved across page navigations.
6. **Active Filter Tags Bar & Empty State:** Interactive badge tags showing active filters with 1-click removal, reset button, and empty state suggestions.
7. **Story Tags System:** Added `tags` to `BlogPost` model, `PostForm`, story editor views, and clickable tag pills on `post_detail.html`.
8. **Automated Testing:** 9 passing tests in `tests/test_week6.py` (41 total cumulative passing tests).

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
- [x] **Week 4:** Responsive Frontend Polish & Medium-like Reading Interface
- [x] **Week 5:** Interactive Commenting System & Moderation
- [x] **Week 6:** Full-Text Search, Tag Filtering & Server-Side Pagination
- [ ] **Week 7:** Automated Testing Suite & Production Deployment Preparation
- [ ] **Week 8:** Final Demonstration Video, Documentation & Internship Submission

---

## 👨‍💻 Author & Repository
- **Developer:** Sidhesh
- **Repository:** [https://github.com/sidhesh1010/Blogging_Platform](https://github.com/sidhesh1010/Blogging_Platform)
- **License:** MIT License
