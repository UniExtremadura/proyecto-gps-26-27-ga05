# Actas de Reuniones del Proyecto — Subsonic Festival (Web Solutions SL - GA05)

Este documento recoge el registro cronológico oficial de las reuniones bisemanales de seguimiento, planificación, refinamiento técnico y retrospectiva celebradas por el equipo **GA05 (Web Solutions SL)** a lo largo de las **6 semanas** de duración del proyecto de desarrollo para la Práctica 1 y Práctica 2 de Gestión de Proyectos Software (GPS).

Siguiendo el protocolo del *Team Charter*, el equipo mantiene una cadencia fija de **dos sesiones de trabajo semanales**:
- **Sesión Ordinaria 1 (Planificación, Análisis y Desarrollo):** Miércoles de 09:30 h a 11:30 h (2 horas).
- **Sesión Ordinaria 2 (Revisión, Auditoría y Consolidación):** Fines de semana (Viernes, Sábados o Domingos) de 10:00 h a 12:00 h (2 horas).

---

## Índice General de Actas (6 Semanas / 12 Sesiones)

| Semana | Código | Fecha | Día y Horario | Objetivo Principal de la Sesión |
| :---: | :---: | :---: | :--- | :--- |
| **Semana 1** | **ACTA-01** | 30/09/2026 | Miércoles (09:30 – 11:30) | Constitución de Web Solutions SL, Roles, Tarifas, Capacidad y *Team Charter*. |
| **Semana 1** | **ACTA-02** | 03/10/2026 | Sábado (10:00 – 12:00) | Estrategia de Producto (`constitution.md`, `mission.md`, `goals.md`) y Calidad (`DoR`/`DoD`). |
| **Semana 2** | **ACTA-03** | 07/10/2026 | Miércoles (09:30 – 11:30) | Definición del *Product Backlog* (5 Épicas, 17 US) y Auditoría `requirements-report-v01.md`. |
| **Semana 2** | **ACTA-04** | 09/10/2026 | Viernes (10:00 – 12:00) | Refinamiento de `spec.md` (`F01`–`F08`) y Auditoría `initial-planning-review-v01.md`. |
| **Semana 3** | **ACTA-05** | 14/10/2026 | Miércoles (09:30 – 11:30) | Recheck `requirements-report-v02.md` y Replanificación equilibrada en 6 Sprints (`Excel`). |
| **Semana 3** | **ACTA-06** | 16/10/2026 | Viernes (10:00 – 12:00) | Cronogramas en ProjectLibre (`.pod`), Tareas `MGT` y Auditoría `planning-audit-v01.md`. |
| **Semana 4** | **ACTA-07** | 21/10/2026 | Miércoles (09:30 – 11:30) | Inicio Práctica 2: Creación de Organización y Proyecto `GA05-GPS26` en Jira y Reparto. |
| **Semana 4** | **ACTA-08** | 25/10/2026 | Domingo (10:00 – 12:00) | Volcado de Backlog en Jira, Enlaces de Precedencia, Ramas Git / *Smart Commits* e Informes. |
| **Semana 5** | **ACTA-09** | 28/10/2026 | Miércoles (09:30 – 11:30) | Revisión de Feedback Docente (Entrega 1): Ajuste de Calendarios, Reuniones y Costes en `.pod`. |
| **Semana 5** | **ACTA-10** | 31/10/2026 | Sábado (10:00 – 12:00) | Revisión de Feedback Docente (Entrega 2): Subtareas en `IT-002`–`IT-006`, Etiquetas y `MGT` en Jira. |
| **Semana 6** | **ACTA-11** | 04/11/2026 | Miércoles (09:30 – 11:30) | Consolidación de Gráficas de Carga, Informes de Jira y Cierre de Tareas de Cierre. |
| **Semana 6** | **ACTA-12** | 07/11/2026 | Sábado (10:00 – 12:00) | Auditoría Final del Repositorio, Validación de Enlaces de Wiki y Preparación de Entrega. |

---

## SEMANA 1

### ACTA-01: Constitución de Web Solutions SL, Roles, Capacidad y Team Charter
- **Fecha:** Miércoles, 30 de septiembre de 2026 | **Horario:** 09:30 – 11:30 (2 h) | **Modalidad:** Presencial (Lab EPCC)
- **Asistentes:** 100% del equipo (Javier García, Jaime Arias, Álvaro Martín, Manuel Carvajal, Justo Cilleros).
- **Desarrollo:** Constitución formal del grupo `GA05` como **Web Solutions SL**. Asignación de tarifas ($35\text{ €/h}$ PO/TL, $30\text{ €/h}$ SM/QA, $25\text{ €/h}$ Dev). Se calcula una capacidad efectiva del equipo de **$47,5\text{ h-p/semana}$** (techo global de $285\text{ h-p}$ en 6 semanas). Se aprueba el *Team Charter* con comunicación vía Discord/WhatsApp y el establecimiento de dos reuniones semanales fijas.
- **Tareas Asignadas:** Redactar perfil de empresa y roles en la Wiki (Responsable: Jaime Arias).

### ACTA-02: Estrategia de Producto, Constitución y Puertas de Calidad DoR/DoD
- **Fecha:** Sábado, 3 de octubre de 2026 | **Horario:** 10:00 – 12:00 (2 h) | **Modalidad:** Online (Discord)
- **Asistentes:** 100% del equipo.
- **Desarrollo:** Redacción y aprobación de `.specify/memory/constitution.md` (principios inviolables: trazabilidad, MVP, datos sintéticos obligatorios sin información real). Aprobación de `specs/product/mission.md` y `specs/product/goals.md` (fijando los objetivos `G-01` a `G-03` y las exclusiones de pagos y facturas reales `EX-01`–`EX-03`). Redacción y validación de `definition-of-ready.md` y `definition-of-done.md`.
- **Tareas Asignadas:** Consolidar los ficheros Markdown fundacionales en el repositorio Git (Responsable: Javier García).

---

## SEMANA 2

### ACTA-03: Definición del Product Backlog y Primera Auditoría de Requisitos `v01`
- **Fecha:** Miércoles, 7 de octubre de 2026 | **Horario:** 09:30 – 11:30 (2 h) | **Modalidad:** Presencial (Lab EPCC)
- **Asistentes:** 100% del equipo.
- **Desarrollo:** Estructuración del *Product Backlog* en 5 Épicas (`EP-001` a `EP-005`) y 17 Historias de Usuario (`US-001` a `US-017`) con un esfuerzo de desarrollo de 228 h-p. Ejecución del agente `requirements-reviewer` que genera `docs/quality/requirements-report-v01.md` (`NEEDS_REFINEMENT`, con hallazgos `F01`–`F08`).
- **Tareas Asignadas:** Aplicar mejoras en los archivos `spec.md` para mitigar las incidencias detectadas por la IA (Responsables: Álvaro Martín y Justo Cilleros).

### ACTA-04: Refinamiento de Especificaciones y Auditoría de Planificación `v01`
- **Fecha:** Viernes, 9 de octubre de 2026 | **Horario:** 10:00 – 12:00 (2 h) | **Modalidad:** Online (Discord)
- **Asistentes:** 100% del equipo.
- **Desarrollo:** Análisis detallado del primer borrador de planificación y ejecución del agente `initial-planning-reviewer` (`docs/project/reviews/initial-planning/initial-planning-review-v01.md`). Se detecta una sobrecarga crítica en `IT-001` (122 h-p frente a las 47,5 h-p de capacidad semanal) y desfases de numeración de historias. Se acuerda migrar de 3 iteraciones a **6 Sprints semanales (`IT-001` a `IT-006`)**.
- **Tareas Asignadas:** Reestructurar el Excel canónico de planificación y alinear los identificadores de los `spec.md` (Responsables: Javier García y Jaime Arias).

---

## SEMANA 3

### ACTA-05: Recheck de Requisitos `v02` y Replanificación Equilibrada en 6 Sprints
- **Fecha:** Miércoles, 14 de octubre de 2026 | **Horario:** 09:30 – 11:30 (2 h) | **Modalidad:** Presencial (Lab EPCC)
- **Asistentes:** 100% del equipo.
- **Desarrollo:** Ejecución del recheck de requisitos (`docs/quality/requirements-report-v02.md`), certificando la resolución de `F01` (revocación JWT) y mejoras parciales en rendimiento y seguridad. Aprobación definitiva de la distribución de trabajo en `docs/plan-subsonic-festival.xlsx` repartiendo las 17 historias de usuario de forma equilibrada en 6 Sprints para que ninguna iteración supere las 47,5 h-p.
- **Tareas Asignadas:** Consolidar el libro Excel en la rama principal del repositorio (Responsable: Javier García).

### ACTA-06: Cronogramas en ProjectLibre, Tareas de Gestión `MGT` y Auditoría de Planificación
- **Fecha:** Viernes, 16 de octubre de 2026 | **Horario:** 10:00 – 12:00 (2 h) | **Modalidad:** Online (Discord)
- **Asistentes:** 100% del equipo.
- **Desarrollo:** Creación y exportación de los ficheros de ProjectLibre (`Subsonic_Festival-Planificacion_Sprints.pod` y `Epicas.pod`). Incorporación de las **48 h de gestión Scrum (`MGT`)** distribuidas en los 6 Sprints (4 h de *Planning & Grooming* y 2 h de *Retrospective* facilitadas por Jaime Arias, más 2 h de *Sprint Review* lideradas por Javier García). Ejecución del agente `planning-auditor` (`docs/quality/planning-audit-v01.md`).
- **Tareas Asignadas:** Preparar el entorno para el inicio de la Práctica 2 en Jira (Responsables: Todos los miembros).

---

## SEMANA 4

### ACTA-07: Configuración de Jira Software (`GA05-GPS26`) y Reparto de Requisitos
- **Fecha:** Miércoles, 21 de octubre de 2026 | **Horario:** 09:30 – 11:30 (2 h) | **Modalidad:** Presencial (Lab EPCC)
- **Asistentes:** 100% del equipo.
- **Desarrollo:** Creación de la organización `GA05-GPS26` y el proyecto Scrum *Team-managed* en Jira Software. Configuración de los estados del tablero (`TO DO`, `IN PROGRESS`, `IN REVIEW`, `DONE`), creación de las 5 Épicas (`EP-001` a `EP-005`) y los 6 Sprints (`IT-001` a `IT-006`). Asignación nominal del reparto de introducción de requisitos por miembro (Javier, Jaime, Álvaro, Manuel y Justo).
- **Tareas Asignadas:** Dar de alta las épicas, historias y subtareas `TK` asignadas en Jira (Responsables: Todos los miembros).

### ACTA-08: Volcado de Backlog en Jira, Predecesores y Estrategia de Ramas Git
- **Fecha:** Domingo, 25 de octubre de 2026 | **Horario:** 10:00 – 12:00 (2 h) | **Modalidad:** Online (Discord)
- **Asistentes:** 100% del equipo.
- **Desarrollo:** Verificación del volcado completo en Jira, configuración de los enlaces de dependencia (*is blocked by*) según el flujo del Excel, asignación de etiquetas (`Must`/`Should`/`Could` y categorías técnicas) y establecimiento del flujo operativo de ramas (`feature/TK-xxx`) y *Smart Commits* (`TK-001-1 #comment ... #time 5h #done`) para la fase de desarrollo.
- **Tareas Asignadas:** Revisar la consistencia de los tickets creados en Jira y extraer las primeras capturas de informes (Responsables: Javier García y Manuel Carvajal).

---

## SEMANA 5

### ACTA-09: Revisión del Feedback Docente (Entrega 1) y Ajuste de ProjectLibre
- **Fecha:** Miércoles, 28 de octubre de 2026 | **Horario:** 09:30 – 11:30 (2 h) | **Modalidad:** Presencial (Lab EPCC)
- **Asistentes:** 100% del equipo.
- **Desarrollo:** Análisis de las observaciones del profesor sobre la Entrega 1 (duración errónea de sprints en ProjectLibre por calendarios por defecto, ceremonias de Scrum no asignadas a todo el equipo y coherencia de costes). Se ajustan los calendarios de recursos en ProjectLibre para que el proyecto abarque correctamente las 6 semanas completas y se programan las ceremonias con la participación de los 5 integrantes.
- **Tareas Asignadas:** Actualizar el archivo `.pod` y la matriz de costes en el repositorio (Responsable: Jaime Arias).

### ACTA-10: Revisión del Feedback Docente (Entrega 2) y Estructura en Jira
- **Fecha:** Sábado, 31 de octubre de 2026 | **Horario:** 10:00 – 12:00 (2 h) | **Modalidad:** Online (Discord)
- **Asistentes:** 100% del equipo.
- **Desarrollo:** Análisis del feedback de la Entrega 2 de Jira (necesidad de reflejar subtareas en `IT-002` a `IT-006` debido a la limitación de Jira de un solo `Assignee` por tarjeta, uso de etiquetas, descripciones completas con `spec.md` e inclusión de tareas de gestión `MGT`). Se acuerda dividir las historias compartidas en subtareas técnicas individuales y dar de alta las tareas `MGT` en los 6 Sprints.
- **Tareas Asignadas:** Modificar las tarjetas en Jira y actualizar las tablas de asignación en la Wiki (Responsables: Todos los miembros).

---

## SEMANA 6

### ACTA-11: Consolidación de Gráficas de Carga, Informes de Jira y Cierre de Tareas
- **Fecha:** Miércoles, 4 de noviembre de 2026 | **Horario:** 09:30 – 11:30 (2 h) | **Modalidad:** Presencial (Lab EPCC)
- **Asistentes:** 100% del equipo.
- **Desarrollo:** Verificación final de los informes de Jira Software, comprobando que la carga horaria semanal de cada iteración se mantiene por debajo del techo de 47,5 h-p y que los costes totales ascienden exactamente a **8.200,00 €** (276 h totales). Generación de capturas de los informes de carga de trabajo por miembro e inserción en el informe de la Wiki.
- **Tareas Asignadas:** Revisar la redacción final de las secciones 12.3 y 12.4 de la Wiki (Responsables: Javier García y Jaime Arias).

### ACTA-12: Auditoría Final del Repositorio, Validación de Enlaces y Preparación de Entrega
- **Fecha:** Sábado, 7 de noviembre de 2026 | **Horario:** 10:00 – 12:00 (2 h) | **Modalidad:** Online (Discord)
- **Asistentes:** 100% del equipo.
- **Desarrollo:** Revisión integral de los entregables: comprobación de enlaces públicos al proyecto de Jira (`GA05-GPS26`), verificación de la estructura del repositorio en GitHub (`proyecto-gps-26-27-ga05`), revisión de actas, informes de auditoría con agentes y archivos de planificación. Cierre formal de la documentación de la Práctica 2.
- **Tareas Asignadas:** Marcar la tarea como entregada enviando los enlaces definitivos de Git y Jira (Responsable: Jaime Arias - Scrum Master).