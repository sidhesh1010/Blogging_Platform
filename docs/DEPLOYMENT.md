# BlogSphere – Production Deployment & Operations Guide

This guide details the steps to deploy and operate **BlogSphere** in high-availability, containerized, and cloud-native environments.

---

## 🏗️ 1. Architecture Overview

BlogSphere follows the **Application Factory** architecture with clean environment decoupling:

```
[ Internet / Clients ]
          │ (HTTPS :443)
          ▼
[ Nginx / Cloud Load Balancer / CDN ]
          │ (HTTP :5000)
          ▼
[ Gunicorn / Waitress WSGI Application Server ]
          │
  ┌───────┴────────────────────────┐
  │  Flask 3.0.3 Application Core   │
  │  ├── Auth Blueprint            │
  │  ├── Posts & Comments Blueprint │
  │  └── Main Blueprint & /health   │
  └───────┬────────────────────────┘
          │ (SQLAlchemy ORM 2.1)
          ▼
[ PostgreSQL 16+ / SQLite Database ]
```

---

## 🔐 2. Environment Variables Reference

| Variable | Description | Default | Required in Production |
| :--- | :--- | :--- | :--- |
| `FLASK_ENV` | Environment identifier (`development`, `testing`, `production`) | `development` | Yes (`production`) |
| `SECRET_KEY` | High-entropy random string for session & CSRF protection | Dev Fallback | **Yes** (32+ chars) |
| `DATABASE_URL` | PostgreSQL or SQLite connection string | Local SQLite path | **Yes** (PostgreSQL) |
| `PORT` | HTTP port for WSGI server to bind | `5000` | Auto-provided by PaaS |

> [!IMPORTANT]
> In `production` mode, `ProductionConfig` automatically enforces:
> - `SESSION_COOKIE_SECURE = True` (cookies transmitted over HTTPS only)
> - `SESSION_COOKIE_HTTPONLY = True` (mitigates XSS cookie theft)
> - `SESSION_COOKIE_SAMESITE = 'Lax'` (mitigates CSRF vulnerabilities)
> - `REMEMBER_COOKIE_HTTPONLY = True`

---

## 🚀 3. Cloud Deployment Options

### Option A: Render (Recommended PaaS)

1. **Create PostgreSQL Database on Render:**
   - Go to [dashboard.render.com](https://dashboard.render.com) -> New **PostgreSQL**.
   - Note the **Internal Database URL**.

2. **Deploy Web Service:**
   - Click New **Web Service** -> Connect GitHub repo `sidhesh1010/Blogging_Platform`.
   - Environment: `Python 3`.
   - Build Command:
     ```bash
     pip install -r requirements.txt && flask db upgrade
     ```
   - Start Command:
     ```bash
     gunicorn run:app
     ```
   - Add Environment Variables:
     - `FLASK_ENV`: `production`
     - `SECRET_KEY`: `<Generate with: python -c "import secrets; print(secrets.token_hex(32))">`
     - `DATABASE_URL`: `<Your Render PostgreSQL Internal URL>`

3. **Verify Deployment:**
   - Navigate to `https://<your-subdomain>.onrender.com/health` to confirm `status: "healthy"` and `database: "connected"`.

---

### Option B: Docker & Docker Compose

Deploy locally or on any cloud VPS (AWS EC2, DigitalOcean Droplet, Linode):

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sidhesh1010/Blogging_Platform.git
   cd Blogging_Platform
   ```

2. **Configure Production Secrets:**
   Create `.env` file:
   ```env
   FLASK_ENV=production
   SECRET_KEY=generate_a_random_32_character_token_here
   ```

3. **Build and Launch Containers:**
   ```bash
   docker compose up -d --build
   ```

4. **Run Database Migrations Inside Container:**
   ```bash
   docker compose exec web flask db upgrade
   ```

5. **Verify Service Health:**
   ```bash
   curl -f http://localhost:5000/health
   ```

---

### Option C: Ubuntu Linux VPS (Nginx + Gunicorn + Systemd + SSL)

1. **System Provisioning:**
   ```bash
   sudo apt update && sudo apt install -y python3-venv python3-pip postgresql nginx certbot python3-certbot-nginx
   ```

2. **Setup Application Directory:**
   ```bash
   sudo mkdir -p /var/www/blogsphere && sudo chown -R $USER:$USER /var/www/blogsphere
   git clone https://github.com/sidhesh1010/Blogging_Platform.git /var/www/blogsphere
   cd /var/www/blogsphere
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   flask db upgrade
   ```

3. **Create Systemd Service (`/etc/systemd/system/blogsphere.service`):**
   ```ini
   [Unit]
   Description=BlogSphere Gunicorn Daemon
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/blogsphere
   Environment="PATH=/var/www/blogsphere/venv/bin"
   Environment="FLASK_ENV=production"
   EnvironmentFile=/var/www/blogsphere/.env
   ExecStart=/var/www/blogsphere/venv/bin/gunicorn --workers 4 --bind unix:/var/www/blogsphere/blogsphere.sock run:app

   [Install]
   WantedBy=multi-user.target
   ```
   Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start blogsphere
   sudo systemctl enable blogsphere
   ```

4. **Configure Nginx (`/etc/nginx/sites-available/blogsphere`):**
   ```nginx
   server {
       server_name yourdomain.com www.yourdomain.com;

       location / {
           include proxy_params;
           proxy_pass http://unix:/var/www/blogsphere/blogsphere.sock;
       }

       location /static/ {
           alias /var/www/blogsphere/app/static/;
           expires 30d;
           add_header Cache-Control "public, no-transform";
       }
   }
   ```
   Activate and issue SSL:
   ```bash
   sudo ln -s /etc/nginx/sites-available/blogsphere /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl restart nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

---

## 🗄️ 4. Database Migrations Workflow

BlogSphere utilizes **Alembic via Flask-Migrate**:

```bash
# Check current migration status
flask db current

# Apply all pending migrations to the database
flask db upgrade

# Rollback to the previous migration
flask db downgrade

# Generate a new migration script after model changes
flask db migrate -m "Description of model change"
```

---

## 🩺 5. Monitoring & Health Checking

Query the automated health monitor anytime:

```bash
curl -i http://localhost:5000/health
```

**Healthy Response (HTTP 200 OK):**
```json
{
  "app": "BlogSphere",
  "database": "connected",
  "environment": "production",
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## 🧪 6. Automated Testing Verification

Execute the test suite verifying all 48 test scenarios:

```bash
pytest -v
```
