from pathlib import Path
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from database.db import init_db
from routes.routes import routes

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / 'frontend'
load_dotenv(ROOT / '.env')
app = Flask(__name__, static_folder=str(FRONTEND), static_url_path='')
CORS(app)
app.register_blueprint(routes)
init_db()

@app.get('/')
def home(): return send_from_directory(FRONTEND, 'index.html')

@app.get('/<path:filename>')
def frontend_files(filename):
    target = FRONTEND / filename
    if target.is_file(): return send_from_directory(FRONTEND, filename)
    return jsonify(error='Not found'),404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(error='Method not allowed for this endpoint', allowed_methods=list(error.valid_methods or [])),405

@app.errorhandler(404)
def not_found(error): return jsonify(error='Endpoint or page not found'),404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
