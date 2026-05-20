Sistema de Citas Médicas
Problema
Los pacientes tienen dificultades para agendar citas médicas de forma rápida y organizada.
Solución = App Inteligente
Aplicación web que permite a los pacientes agendar, cancelar y gestionar sus citas médicas en tiempo real, con priorización automática según urgencia.
Funcionalidades principales

Registro de pacientes
Agendamiento de citas por especialidad
Sistema de priorización de pacientes urgentes
Notificaciones de recordatorio
Historial de citas

Tecnologías

Frontend: HTML, CSS, JavaScript
Backend: Python (Flask)
Base de datos: SQLite

Sección: Priorización de Pacientes Urgentes
Criterios de priorización

Nivel 1 - Emergencia: Dolor severo, síntomas críticos → Atención inmediata
Nivel 2 - Urgente: Síntomas moderados → Atención en menos de 2 horas
Nivel 3 - Normal: Consulta de rutina → Agendamiento estándar

Algoritmo de priorización

El sistema evalúa los síntomas ingresados por el paciente
Asigna automáticamente un nivel de urgencia
Reordena la cola de espera según prioridad

## Priorización

Los pacientes se priorizan según:
1. Urgencia crítica (rojo)
2. Urgencia media (amarillo)
3. No urgente (verde)
