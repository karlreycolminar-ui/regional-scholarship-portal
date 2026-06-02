# 🎓 Regional Scholarship Application Portal

A production-ready, secure enterprise web application built with **Django 4.2**, **Django REST Framework**, and **JWT Authentication**.

---

## 👥 Team Roles

| Role | Responsibility |
|------|---------------|
| Lead Cloud & DevOps Engineer | Render/Railway deployment, Cloudinary, environment variables |
| API & IAM Engineer | DRF REST API, JWT auth, field-level masking |
| Database Architect & RBAC Lead | Data models, Anti-IDOR logic, RBAC |
| Frontend UI & Component Engineer | Dashboard templates, filters, forms |
| DevSecOps & Compliance Analyst | django-axes, honeypot, audit logging, SAST scans |

---

## 🚀 Quick Start (Local Development)

### 1. Clone & Setup
```bash
git clone https://github.com/karlreycolminar-ui/regional-scholarship-portal.git
cd regional-scholarship-portal

python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Windows:
copy env.example .env
# Mac/Linux:
cp env.example .env

# Edit .env with your values (SECRET_KEY at minimum)
```

### 3. Database & Seed
```bash
python manage.py migrate
python manage.py seed_data
```

### 4. Run Server
```bash
python manage.py runserver
```
Visit: http://127.0.0.1:8000

---

## 🔑 Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `Admin@1234` |
| Reviewer | `reviewer1` | `Reviewer@1234` |
| Applicant | `juan.dela.cruz` | `Applicant@1234` |

---

## 📁 Project Structure

```
scholarship_portal/
├── scholarship_portal/     # Project settings & URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               # User management & auth
│   ├── models.py           # Custom User with RBAC roles
│   ├── views.py            # Login, register, profile, user management
│   ├── api_views.py        # DRF API endpoints
│   ├── serializers.py      # With field-level email masking
│   ├── permissions.py      # IsApplicant, IsReviewer, IsAdmin, IsOwnerOrAdmin
│   ├── forms.py            # Registration with honeypot
│   ├── urls.py             # Template view URLs
│   ├── api_urls.py         # API URLs
│   └── management/
│       └── commands/
│           └── seed_data.py
├── scholarships/           # Scholarship listings
├── applications/           # Application submission & review
│   ├── models.py           # Applications, review fields, documents
│   ├── views.py            # Apply, detail, withdraw, reviewer workflows
│   ├── forms.py            # Application, document upload, review forms
│   ├── api_views.py        # DRF endpoints for applications and reviews
│   └── urls.py             # Template view URLs
├── audits/                 # Audit logging system
└── templates/              # HTML templates
    ├── base.html
    ├── accounts/
    ├── scholarships/
    ├── applications/
    │   ├── apply.html
    │   ├── detail.html
    │   ├── my_applications.html
    │   ├── review_list.html
    │   └── review.html
    ├── dashboard/
    └── audits/
```

---

## 📝 Reviewer Workflow

Reviewers and admins can manage applications from `/applications/review/`.

| Page | Purpose |
|------|---------|
| `/applications/review/` | Filter applications by status or scholarship |
| `/applications/review/<id>/` | Review one application, inspect applicant details and documents, then mark as Under Review, Approved, or Rejected |
| `/applications/<id>/` | Read-only application detail page with timeline and review notes |

When a review decision is saved, the application records the reviewer, timestamp, status, notes, and an audit log entry.

---

## 🔐 Security Features

| Feature | Implementation |
|---------|---------------|
| Authentication | JWT via `djangorestframework-simplejwt` |
| Session Auth | Django session for template views |
| RBAC | Custom role field + permission classes |
| Anti-IDOR | All querysets filtered by `request.user` |
| Brute Force Protection | `django-axes` (5 attempts → 30min lockout) |
| Honeypot | Hidden field in registration form |
| Input Validation | Server-side form + serializer validation |
| File Validation | MIME type + size checks (10MB limit) |
| Audit Logging | All actions logged to `AuditLog` model |
| Field Masking | Email masked for non-owners in API |
| SQL Injection | ORM-safe queries throughout |
| CSRF | Django CSRF middleware on all forms |
| XSS | Django template auto-escaping |

---

## 🌐 REST API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new applicant |
| POST | `/api/auth/login/` | Login → JWT tokens |
| POST | `/api/auth/logout/` | Blacklist refresh token |
| POST | `/api/auth/refresh/` | Refresh access token |
| GET/PATCH | `/api/auth/profile/` | Get/update own profile |
| POST | `/api/auth/change-password/` | Change password |

### Users (Admin only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/` | List all users |
| GET/PUT/DELETE | `/api/users/<id>/` | User detail |

### Scholarships
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/scholarships/` | List open scholarships |
| GET | `/api/scholarships/<id>/` | Scholarship detail |
| POST | `/api/scholarships/create/` | Create (Admin) |
| PUT/PATCH/DELETE | `/api/scholarships/<id>/manage/` | Manage (Admin) |

### Applications
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/applications/` | My applications (Applicant) / All (Admin/Reviewer) |
| POST | `/api/applications/` | Submit new application |
| GET/DELETE | `/api/applications/<id>/` | Detail / Withdraw |
| POST | `/api/applications/<id>/review/` | Submit review decision |
| POST | `/api/applications/<id>/documents/` | Upload document |
| GET | `/api/admin/applications/` | Admin full list |

---

## ☁️ Deployment (Render)

1. Push code to GitHub
2. Create new **Web Service** on [render.com](https://render.com)
3. Connect your GitHub repository
4. Set environment variables:
   - `SECRET_KEY` → generate a strong random key
   - `DEBUG` → `False`
   - `DATABASE_URL` → Render PostgreSQL URL
   - `ALLOWED_HOSTS` → `your-app.onrender.com`
   - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
5. Set **Build Command**: `bash build.sh`
6. Set **Start Command**: `gunicorn scholarship_portal.wsgi`

---

## 🔍 Security Audit Commands

```bash
# Install audit tools
pip install bandit pip-audit

# Run Bandit SAST scan
bandit -r . -x venv/ --format txt -o bandit_report.txt

# Run pip dependency audit
pip-audit -r requirements.txt -o pip_audit_report.txt

# Django security check
python manage.py check --deploy
```

Generated reports such as `bandit_report.txt` and `pip_audit_report.txt` are ignored by Git.

---

## 📦 Key Dependencies

| Package | Purpose |
|---------|---------|
| `django` | Web framework |
| `djangorestframework` | REST API |
| `djangorestframework-simplejwt` | JWT authentication |
| `django-axes` | Brute-force protection |
| `django-honeypot` | Bot/spam protection |
| `django-cors-headers` | CORS headers |
| `cloudinary` | Cloud media storage |
| `whitenoise` | Static file serving |
| `gunicorn` | Production WSGI server |
| `psycopg[binary]` | PostgreSQL adapter |
| `python-dotenv` | Environment variables |
