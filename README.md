# Ergonomics App (Flask)

Ergonomics assessments (RULA/REBA/NIOSH) with media uploads, list filters, CSV/PDF export, and RBAC (Admin/Assessor/Viewer).

## Quickstart (Windows PowerShell)
```powershell
cd ergo_app
py -3 -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
flask --app wsgi.py db-init
flask --app wsgi.py db-ensure-roles   # adds 'role' column if needed (SQLite)
# Create users:
flask --app wsgi.py create-user "Admin Name" admin@example.com "Passw0rd!" --role Admin
flask --app wsgi.py create-user "Assessor Name" assessor@example.com "Passw0rd!"
# Run:
flask --app wsgi.py run
```

Open http://127.0.0.1:5000 and login.
