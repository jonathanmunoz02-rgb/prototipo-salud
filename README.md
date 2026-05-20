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
