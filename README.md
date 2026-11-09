# College ERP Mini System – Fixed Backend

## Run on Windows
1. Open PowerShell in this project folder.
2. `cd backend`
3. `py -m venv venv`
4. `venv\Scripts\Activate.ps1` (if blocked, run `Set-ExecutionPolicy -Scope Process Bypass`)
5. `py -m pip install -r requirements.txt`
6. `py app.py`
7. Open **http://127.0.0.1:5000/**. The Flask server also serves the frontend, so do not open HTML using `file:///`.

The backend initializes a local SQLite database automatically at `instance/college_erp.sqlite3`; no separate MySQL service is required for this runnable version. `database/college_erp.sql` is an optional MySQL schema reference.

## Demo login credentials
- Admin: username `admin`, password `admin123`, role Admin
- Student: username `student`, password `student123`, role Student
- Faculty: username `faculty`, password `faculty123`, role Faculty

These are demonstration credentials only. Do not deploy publicly without implementing proper password hashing, user storage, sessions, and authorization.

## API endpoints
- `GET /api/health`
- Students: `GET/POST /api/students`, `GET/PUT/DELETE /api/students/<id>`
- Faculty: `GET/POST /api/faculty`, `PUT/DELETE /api/faculty/<id>`
- Attendance: `GET/POST /api/attendance`, `PUT/DELETE /api/attendance/<id>`
- Marks: `GET/POST /api/marks`, `PUT/DELETE /api/marks/<id>`
- Notices: `GET/POST /api/notices`, `PUT/DELETE /api/notices/<id>`
- Timetable: `GET/POST /api/timetable`, `PUT/DELETE /api/timetable/<id>`
- Login: `POST /api/login` with JSON `{"username":"admin","password":"admin123","role":"admin"}`

A 405 response means the URL exists but the HTTP method is not allowed. Use the methods listed above.
