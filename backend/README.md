# Edutrack Pro API

Django REST Framework backend for the React app. It uses MySQL 8, paginated list responses, and the existing `/user/`, `/student/`, `/subject/`, and `/attendance/` API paths. API endpoints are open and do not require a session or token. Local defaults are `root/root`.

## Prerequisites

- Python 3.12 or newer
- MySQL 8 running locally
- Create the database from `backend/.env` once: `CREATE DATABASE edutrackpython CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

## Setup (PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `DJANGO_SECRET_KEY` to a long random value. The supplied `root/root` values are for a local development MySQL server only. Configure a restricted MySQL user for any shared or deployed environment.

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8092
```

The superuser's role is set to `admin` automatically. Regular users can be added from the admin UI or API. The Vite app should use `VITE_API_URL=http://localhost:8092`.

To create quick demo records after migrating, use the Django shell:

```powershell
python manage.py shell -c "from users.models import User; from students.models import Student; from subjects.models import Subject; User.objects.get_or_create(username='faculty1', defaults={'email':'faculty1@example.com','first_name':'Asha','last_name':'Shah','role':'faculty'}); u=User.objects.get(username='faculty1'); u.set_password('Faculty123!'); u.save(); Subject.objects.get_or_create(name='Mathematics'); Student.objects.get_or_create(email='student1@example.com', defaults={'name':'Riya Patel'})"
```

## API notes

- Login with `POST /user/login-user/` and `{ "username", "password" }`; the response returns username and role for frontend navigation only.
- User JSON keeps frontend camelCase fields (`firstName`, `lastName`). Passwords are stored as plain text to match the existing Java table and are never returned by the API.
- Attendance submission follows the UI payload. Listed students are present; all other current students receive absent entries. Response `students` and `numberOfStudents` refer to present students, matching the current attendance table/modal.
- List routes use DRF pagination (`count`, `next`, `previous`, `results`).
- Admin manages users and subjects and views all attendance. Faculty can list subjects, manage the student roster, and view/mark only their own attendance.

## Frontend integration

List helpers normalize DRF's `results` field to arrays so existing screens continue to work. Frontend role checks only control navigation; API endpoints do not enforce roles.
