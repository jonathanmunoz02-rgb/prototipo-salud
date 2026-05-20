from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'medicita-demo-secret-key'
app.config['DATABASE'] = 'medicita.db'

DOCTORS = [
    ('Camilo Ruiz', 'Medicina general'),
    ('Laura Pérez', 'Pediatría'),
    ('Andrés Gómez', 'Cardiología'),
    ('Sara Martínez', 'Dermatología')
]


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        cedula TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('paciente','medico','admin')),
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        symptoms TEXT NOT NULL,
        urgency TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pendiente',
        created_at TEXT NOT NULL,
        FOREIGN KEY(patient_id) REFERENCES users(id)
    );
    ''')
    count = db.execute("SELECT COUNT(*) FROM users WHERE role='admin'").fetchone()[0]
    if count == 0:
        db.execute(
            'INSERT INTO users (full_name, cedula, password_hash, role, created_at) VALUES (?,?,?,?,?)',
            ('Administrador MediCita', '1000', generate_password_hash('admin123'), 'admin', datetime.now().isoformat())
        )
    db.commit()
    db.close()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión primero.', 'error')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


def evaluate_urgency(symptoms):
    text = symptoms.lower()
    critical_terms = ['dolor pecho', 'dificultad para respirar', 'desmayo', 'convuls']
    urgent_terms = ['fiebre', 'dolor intenso', 'sangrado', 'mareo fuerte']
    if any(term in text for term in critical_terms):
        return 'Crítica'
    if any(term in text for term in urgent_terms):
        return 'Urgente'
    return 'Normal'


@app.context_processor
def inject_user():
    return {'current_user': session}


@app.route('/')
def index():
    return render_template('index.html', doctors=DOCTORS)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name'].strip()
        cedula = request.form['cedula'].strip()
        password = request.form['password']
        role = request.form['role']
        db = get_db()
        exists = db.execute('SELECT id FROM users WHERE cedula = ?', (cedula,)).fetchone()
        if exists:
            flash('Ya existe un usuario con esa cédula.', 'error')
            return redirect(url_for('register'))
        db.execute(
            'INSERT INTO users (full_name, cedula, password_hash, role, created_at) VALUES (?,?,?,?,?)',
            (full_name, cedula, generate_password_hash(password), role, datetime.now().isoformat())
        )
        db.commit()
        flash('Cuenta creada correctamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cedula = request.form['cedula'].strip()
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE cedula = ?', (cedula,)).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('dashboard'))
        flash('Credenciales inválidas.', 'error')
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.', 'success')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    if session.get('role') == 'paciente':
        appointments = db.execute(
            'SELECT * FROM appointments WHERE patient_id = ? ORDER BY appointment_date, appointment_time',
            (session['user_id'],)
        ).fetchall()
    else:
        appointments = db.execute(
            'SELECT a.*, u.full_name AS patient_name, u.cedula AS patient_cedula FROM appointments a JOIN users u ON a.patient_id=u.id ORDER BY appointment_date, appointment_time'
        ).fetchall()
    return render_template('dashboard.html', appointments=appointments, doctors=DOCTORS)


@app.route('/appointments/create', methods=['POST'])
@login_required
def create_appointment():
    if session.get('role') != 'paciente':
        flash('Solo los pacientes pueden crear citas.', 'error')
        return redirect(url_for('dashboard'))
    doctor_info = request.form['doctor'].split('|')
    doctor_name, specialty = doctor_info[0], doctor_info[1]
    appointment_date = request.form['appointment_date']
    appointment_time = request.form['appointment_time']
    symptoms = request.form['symptoms'].strip()
    urgency = evaluate_urgency(symptoms)
    status = 'Confirmada' if urgency == 'Crítica' else 'Pendiente'
    db = get_db()
    db.execute(
        '''INSERT INTO appointments
        (patient_id, doctor_name, specialty, appointment_date, appointment_time, symptoms, urgency, status, created_at)
        VALUES (?,?,?,?,?,?,?,?,?)''',
        (session['user_id'], doctor_name, specialty, appointment_date, appointment_time, symptoms, urgency, status, datetime.now().isoformat())
    )
    db.commit()
    flash(f'Cita creada. Nivel detectado: {urgency}.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    db = get_db()
    if session.get('role') == 'paciente':
        db.execute('UPDATE appointments SET status = ? WHERE id = ? AND patient_id = ?', ('Cancelada', appointment_id, session['user_id']))
    else:
        db.execute('UPDATE appointments SET status = ? WHERE id = ?', ('Cancelada', appointment_id))
    db.commit()
    flash('Cita cancelada.', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
