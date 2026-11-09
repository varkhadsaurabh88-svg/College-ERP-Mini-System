from flask import Blueprint, request, jsonify
from database.db import get_db

routes = Blueprint('routes', __name__)

@routes.get('/api/health')
def health():
    return jsonify(status='success', message='College ERP backend is running', database='connected'), 200

def collection(table, fields, required=()):
    if request.method == 'GET':
        with get_db() as db:
            rows = db.execute(f'SELECT * FROM {table} ORDER BY id DESC').fetchall()
            return jsonify([dict(r) for r in rows]), 200
    data = request.get_json(silent=True) or request.form.to_dict()
    missing = [f for f in required if data.get(f) in (None, '')]
    if missing: return jsonify(error='Missing required fields', fields=missing), 400
    if request.method == 'POST':
        vals = [data.get(f) for f in fields]
        try:
            with get_db() as db:
                cur = db.execute(f"INSERT INTO {table} ({','.join(fields)}) VALUES ({','.join(['?']*len(fields))})", vals)
                row = db.execute(f'SELECT * FROM {table} WHERE id=?',(cur.lastrowid,)).fetchone()
                return jsonify(message='Record created', record=dict(row)), 201
        except Exception as e: return jsonify(error=str(e)), 400
    if request.method in ('PUT','PATCH'):
        rid=request.view_args.get('record_id')
        updates=[f for f in fields if f in data]
        if not updates: return jsonify(error='No fields to update'), 400
        try:
            with get_db() as db:
                cur=db.execute(f"UPDATE {table} SET {','.join(f+'=?' for f in updates)} WHERE id=?",[data[f] for f in updates]+[rid])
                if not cur.rowcount: return jsonify(error='Record not found'),404
                row=db.execute(f'SELECT * FROM {table} WHERE id=?',(rid,)).fetchone()
                return jsonify(message='Record updated',record=dict(row)),200
        except Exception as e: return jsonify(error=str(e)),400
    if request.method == 'DELETE':
        rid=request.view_args.get('record_id')
        with get_db() as db:
            cur=db.execute(f'DELETE FROM {table} WHERE id=?',(rid,))
            if not cur.rowcount: return jsonify(error='Record not found'),404
            return jsonify(message='Record deleted'),200

@routes.route('/api/students', defaults={'record_id': None}, methods=['GET','POST'])
@routes.route('/api/students/<int:record_id>', methods=['GET','PUT','PATCH','DELETE'])
def students(record_id):
    if record_id is not None and request.method=='GET':
        with get_db() as db:
            r=db.execute('SELECT * FROM students WHERE id=?',(record_id,)).fetchone()
            return (jsonify(dict(r)),200) if r else (jsonify(error='Record not found'),404)
    return collection('students',['name','email','roll_number','prn','department','year'],('name',))

@routes.route('/api/faculty', defaults={'record_id': None}, methods=['GET','POST'])
@routes.route('/api/faculty/<int:record_id>', methods=['PUT','PATCH','DELETE'])
def faculty(record_id): return collection('faculty',['name','email','department','designation'],('name',))

@routes.route('/api/attendance', defaults={'record_id': None}, methods=['GET','POST'])
@routes.route('/api/attendance/<int:record_id>', methods=['PUT','PATCH','DELETE'])
def attendance(record_id): return collection('attendance',['student_id','subject','attendance_date','status'],('student_id','subject','attendance_date','status'))

@routes.route('/api/marks', defaults={'record_id': None}, methods=['GET','POST'])
@routes.route('/api/marks/<int:record_id>', methods=['PUT','PATCH','DELETE'])
def marks(record_id): return collection('marks',['student_id','subject','marks_obtained','total_marks'],('student_id','subject','marks_obtained','total_marks'))

@routes.route('/api/notices', defaults={'record_id': None}, methods=['GET','POST'])
@routes.route('/api/notices/<int:record_id>', methods=['PUT','PATCH','DELETE'])
def notices(record_id): return collection('notices',['title','message'],('title','message'))

@routes.route('/api/timetable', defaults={'record_id': None}, methods=['GET','POST'])
@routes.route('/api/timetable/<int:record_id>', methods=['PUT','PATCH','DELETE'])
def timetable(record_id): return collection('timetable',['day','start_time','end_time','subject','faculty','room'],('day','start_time','end_time','subject'))

@routes.post('/api/login')
def login():
    data=request.get_json(silent=True) or {}
    username=(data.get('username') or '').strip()
    password=data.get('password') or ''
    role=(data.get('role') or 'student').lower()
    # Demo-only credentials; replace with hashed database authentication before deployment.
    demo={'admin':('admin','admin123'),'student':('student','student123'),'faculty':('faculty','faculty123')}
    if role not in demo or username != demo[role][0] or password != demo[role][1]:
        return jsonify(error='Invalid demo credentials'),401
    return jsonify(message='Login successful',role=role,username=username),200
