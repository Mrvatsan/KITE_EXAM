# Deployment Guide - KGiSL Exam Portal on Render

This guide covers deploying the **KGiSL Exam Portal** (Django Backend + PostgreSQL Database + Next.js Frontend) to [Render](https://render.com).

Repository: `https://github.com/Mrvatsan/KITE_EXAM.git`

---

## 🚀 Option 1: 1-Click Render Blueprint (Recommended)

Render Blueprints automatically deploy the PostgreSQL database, Django backend, and Next.js frontend with all environment variables linked.

1. Push your latest code to GitHub:
   ```bash
   git add .
   git commit -m "Configure Render deployment ready"
   git push origin main
   ```
2. Log in to [Render Dashboard](https://dashboard.render.com).
3. Click **"New +"** → **"Blueprint"**.
4. Connect your GitHub repository: `Mrvatsan/KITE_EXAM`.
5. Render will automatically detect `render.yaml` and configure:
   - **Database**: `exam-portal-db` (PostgreSQL)
   - **Backend Web Service**: `exam-portal-backend` (Django + Gunicorn)
   - **Frontend Web Service**: `exam-portal-frontend` (Next.js)
6. Click **"Apply"**.
7. Render will build and deploy all services automatically!

---

## 🛠️ Option 2: Manual Service Setup

If you prefer to set up services manually in the Render dashboard:

### Step 1: Create PostgreSQL Database
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `exam-portal-db`
   - **Database**: `exam_portal_db`
   - **User**: `exam_portal_user`
   - **Plan**: Free
4. Click **"Create Database"**
5. Copy the **Internal Database URL** (e.g. `postgresql://exam_portal_user:...@dpg-...-a/exam_portal_db`).

---

### Step 2: Deploy Django Backend
1. Click **"New +"** → **"Web Service"**
2. Connect repository: `Mrvatsan/KITE_EXAM`
3. Configure:
   - **Name**: `exam-portal-backend`
   - **Root Directory**: `KGiSL-Exam-Portal/backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn backend.wsgi:application`
   - **Plan**: Free
4. Under **"Environment Variables"**, add:
   | Key | Value |
   |-----|-------|
   | `PYTHON_VERSION` | `3.10.10` |
   | `DEBUG` | `False` |
   | `DATABASE_URL` | *Paste your Internal Database URL from Step 1* |
   | `SECRET_KEY` | *Generate a secure random string or click Generate* |
   | `ALLOWED_HOSTS` | `.onrender.com` |
   | `DJANGO_SUPERUSER_USERNAME` | `Kgkite` |
   | `DJANGO_SUPERUSER_PASSWORD` | `Kgkite@123` |
5. Set **Health Check Path** (under Advanced): `/health/`
6. Click **"Create Web Service"**.
7. Once deployed, copy your backend URL (e.g., `https://exam-portal-backend.onrender.com`).

> **Admin Login Credentials**:
> - **Username**: `Kgkite` (or `admin`)
> - **Password**: `Kgkite@123` (or `admin123`)
> - **Role**: `Admin`

---

### Step 3: Deploy Next.js Frontend
1. Click **"New +"** → **"Web Service"**
2. Connect repository: `Mrvatsan/KITE_EXAM`
3. Configure:
   - **Name**: `exam-portal-frontend`
   - **Root Directory**: `KGiSL-Exam-Portal/frontend`
   - **Runtime**: `Node`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Plan**: Free
4. Under **"Environment Variables"**, add:
   | Key | Value |
   |-----|-------|
   | `NODE_VERSION` | `20.18.0` |
   | `NEXT_PUBLIC_API_URL` | *Your Backend URL from Step 2 (e.g. https://exam-portal-backend.onrender.com)* |
5. Click **"Create Web Service"**.

---

## 🔒 Security & Optimization Highlights
- **CORS & CSRF**: Backend automatically trusts all `*.onrender.com` domains via wildcard regex.
- **Static Assets**: Django static files are compressed and cached using Whitenoise.
- **Superuser**: Automatically provisions an initial superuser during the build step.
- **LF Line Endings**: Enforced via `.gitattributes` to avoid bash interpreter errors on Linux.
- **Health Check**: Fast `/health/` endpoint ensures zero false downtime alerts.
