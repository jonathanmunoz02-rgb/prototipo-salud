# Sistema de Citas Médicas

## Problema
Los pacientes tienen dificultades para agendar citas médicas de forma rápida y organizada.

## Solución = App Inteligente
Aplicación web que permite a los pacientes agendar, cancelar y gestionar sus citas médicas en tiempo real, con priorización automática según urgencia.

## Funcionalidades principales
- Registro de pacientes
- Agendamiento de citas por especialidad
- Sistema de priorización de pacientes urgentes
- Notificaciones de recordatorio
- Historial de citas

## Tecnologías
- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- Base de datos: SQLite


## Sección: Priorización de Pacientes Urgentes

### Criterios de priorización
1. **Nivel 1 - Emergencia**: Dolor severo, síntomas críticos → Atención inmediata
2. **Nivel 2 - Urgente**: Síntomas moderados → Atención en menos de 2 horas
3. **Nivel 3 - Normal**: Consulta de rutina → Agendamiento estándar

### Algoritmo de priorización
- El sistema evalúa los síntomas ingresados por el paciente
- Asigna automáticamente un nivel de urgencia
- Reordena la cola de espera según prioridad

# MediCita funcional

Aplicación básica en Flask + SQLite para:
- Registrar usuarios
- Iniciar sesión
- Crear citas médicas
- Ver citas por paciente o de forma general para médico/admin
- Cancelar citas
- Clasificar urgencia según síntomas

## Cómo ejecutar

```bash
cd output/medicita-full
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Luego abre `http://127.0.0.1:5000`.

## Usuario admin por defecto
- Cédula: `1000`
- Contraseña: `admin123`
