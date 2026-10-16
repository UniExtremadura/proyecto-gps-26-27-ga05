# Planning audit v01

## 1. Metadatos de auditoría

- **Proyecto:** SubsonicFestival / Web Solutions SL.
- **Modo:** INITIAL.
- **Baseline revisado:** snapshot del repositorio disponible en esta revisión; no se suministró commit ni versión aprobada de planificación.
- **Versiones/fechas identificables:** los dos XML contienen `SaveVersion=14` (formato del archivo, no versión de baseline) y `CurrentDate=2026-10-16T18:00:00`. El XML de épicas programa del 15 al 22 de octubre de 2026; el de sprints, del 14 de octubre al 3 de noviembre de 2026. No se indica que uno sustituya al otro.
- **Fecha de revisión:** 2026-10-16 18:19 +02:00, suministrada en la invocación.
- **Agente/versión:** las instrucciones de auditoría se suministraron con la invocación; versión no indicada. No se encontró `.github/agents/planning-auditor.agent.md`. Se consultó `.github/agents/initial-planning-reviewer.agent.md`, que tiene un mandato y destino de informe distintos; no se trató como sustituto del agente de auditoría solicitado.
- **Herramientas/modelo:** no indicados.
- **Alcance solicitado:** planificación global, épicas, sprints, requisitos, tareas, riesgos, dependencias, recursos, costes y viabilidad temporal/económica.
- **Alcance efectivamente evaluable:** constitución, misión, objetivos, las cinco especificaciones actuales de épica, DoR/DoD, informe de revisión de requisitos v01, inventario de `docs/organization/` y secciones de metadatos, calendario, tareas, recursos y asignaciones de ambos XML exportados. Las tareas y filas timephased de los XML no se leyeron íntegramente elemento por elemento; por ello no se afirma haber agregado todas las cargas ni verificado cada enlace.
- **Idioma:** español.
- **Horizonte:** el XML de épicas declara 2026-10-15–2026-10-22; el XML de sprints declara 2026-10-14–2026-11-03. No se eligió uno como baseline.
- **Versionado del informe:** `v01`; al inspeccionar `docs/quality/` no se encontraron archivos con el patrón `planning-audit-vNN.md`.

## 2. Inventario de fuentes y limitaciones

| Fuente leída | Función y evidencia revisada | Versión/limitaciones |
|---|---|---|
| `.specify/memory/constitution.md` | Principios de MVP, seguridad/datos sintéticos, trazabilidad, reglas de documentación y precedencia. | Sin versión o fecha identificable en el texto leído. Establece que la constitución prevalece. |
| `specs/product/mission.md` | Misión, problema y usuarios principales: comprador y promotor/organizador. | Sin versión identificable. |
| `specs/product/goals.md` | G-01–G-03, M-01–M-03, S-01–S-03, exclusiones EX-01–EX-03 y restricciones. | Sin versión identificable. |
| `specs/EP-001-autenticacion-y-roles/spec.md` | US-001 y US-003; criterios, estimaciones, incertidumbre, planes iniciales y predecesores. | Sin versión identificable. |
| `specs/EP-002-catalogo-y-busqueda/spec.md` | US-006 y US-007. | Sin versión identificable. |
| `specs/EP-003-gestion-eventos-entradas/spec.md` | US-008. | Sin versión identificable. |
| `specs/EP-004-servicios-proveedores/spec.md` | US-011. | Sin versión identificable. |
| `specs/EP-005-administracion-y-seguridad/spec.md` | US-017. | Sin versión identificable. |
| `docs/quality/definition-of-ready.md` | Criterios de identificación, aceptación, estimación, incertidumbre, predecesores, iteración, restricciones, supuestos, WIP y aprobación del PO. | Nombre real distinto del indicado en la invocación; sin versión identificable. |
| `docs/quality/definition-of-done.md` | Checklist técnico, pruebas, seguridad, rendimiento, revisión, aprobación, integración y documentación. | Nombre real distinto del indicado en la invocación; sin versión identificable. La planificación no demuestra que historias estén terminadas. |
| `docs/quality/requirements-report-v01.md` | Informe previo de requisitos, fechado allí 2026-10-07 10:14 +02:00; matriz DoR, hallazgos, dependencias y preguntas. | Informe de requisitos, no informe previo de planificación. Describe IDs y contenido diferentes de las especificaciones actuales; no hay regla que resuelva si es obsoleto o si corresponde a otro baseline. |
| `docs/Subsonic_Festival-Planificacion_Epicas.pod.xml` | Encabezado del proyecto, calendario, muestras de tareas, enlaces, recursos y asignaciones. | Exportación XML compatible Project; `SaveVersion=14`, `CurrentDate=2026-10-16T18:00:00`. No se abrió el archivo nativo `.pod`; inspección de XML por secciones, no de cada registro. |
| `docs/Subsonic_Festival-Planificacion_Sprints.pod.xml` | Encabezado, calendario, muestras de tareas y enlaces, recursos y asignaciones. | Exportación XML compatible Project; `SaveVersion=14`, `CurrentDate=2026-10-16T18:00:00`. No se abrió el archivo nativo `.pod`; inspección de XML por secciones, no de cada registro. |
| `docs/organization/` | Inventario del directorio. | Solo se encontró `.gitkeep`; no es evidencia de roles, disponibilidad, habilidades o tarifas del equipo. |
| `.github/agents/initial-planning-reviewer.agent.md` | Instrucciones locales consultadas para identificar la función del agente existente. | No equivale a un agente de auditoría de planificación; sus reglas de READINESS/CONSISTENCY y su ruta de informe difieren. |

**Precedencia y conflictos:** la constitución declara precedencia sobre los demás documentos. No se encontró una regla que establezca cuál XML de planificación es el baseline vigente ni cómo resolver las divergencias entre `requirements-report-v01.md` y las especificaciones actuales. Se informan ambos lados sin elegir silenciosamente. Los XML están en formato Project XML exportado, no se validaron mediante recálculo en ProjectLibre.

## 3. Evaluación general

**Recomendación: NEEDS_REPLANNING.**

La evaluación se refiere a la planificación global contenida en los dos XML citados y a su coherencia con las fuentes de producto leídas; no constituye una evaluación de la implementación ni una aprobación de baseline. Se identifican bloqueos que impiden tratar los dos archivos como una planificación única y demostrar su viabilidad:

1. Las cabeceras de los planes declaran horizontes y duraciones de proyecto diferentes, sin una decisión de precedencia.
2. Los recursos referencian calendarios UID 4–8, mientras que la sección `Calendars` revisada define UID 1–3; no se puede verificar la disponibilidad efectiva por persona.
3. En ambos planes, una asignación revisada registra 100% de unidades para un recurso con `MaxUnits=0.25`; el XML marca `OverAllocated=0`. La carga total por persona/periodo no se ha agregado y requiere reconciliación.
4. Los IDs y alcance de las tareas no trazan limpiamente a las especificaciones actuales y al informe previo; por ejemplo, el plan incluye US-002/US-004/US-009/US-014/US-015/US-016, no halladas en las cinco especificaciones actuales leídas, y el informe previo describe US-009/US-012/US-018 donde las especificaciones actuales leídas describen otros IDs.

La matriz de cobertura y los registros de hallazgos detallan qué es contradicción confirmada y qué requiere confirmación humana. El riesgo y coste global no pueden considerarse evaluados satisfactoriamente: no se proporcionó un registro de riesgos identificable ni hay base suficiente para reconciliar costes totales.

## 4. Matriz de cobertura

| Dimensión/comprobación | Alcance inspeccionado | Estado | Evidencia y hallazgos |
|---|---|---|---|
| Alineación con misión, objetivos, alcance y exclusiones | Misión; G-01–G-03, S-01–S-03, EX-01–EX-03; tareas muestreadas | NOT_MET | El plan contiene varios resultados fuera de la descripción explícita del MVP; la decisión de alcance no está documentada. PA-004. |
| Requisitos, épicas y trazabilidad de IDs | Cinco `spec.md`; informe requirements v01; tareas planificadas revisadas | NOT_MET | Diferencias de IDs entre especificaciones, plan e informe; predecesores y tareas no trazan en todos los casos. PA-004. |
| Definition of Ready | Criterios DoR; historias y asignaciones revisadas | NOT_ASSESSABLE | El DoR exige aprobación PO y WIP ≤2; no hay registro de esas decisiones. La discrepancia de baseline impide validar las historias planificadas que no tienen especificación actual. PA-004, PA-007. |
| Definition of Done | Checklist DoD | NOT_ASSESSABLE | La planificación no prueba implementación, pruebas, revisión, aprobación ni fusión; no se declara ninguna historia terminada. Referencia US-018 en DoD frente a US-017 actual: PA-004. |
| Riesgos documentados y tratamientos | Fuentes de planificación/producto y directorio `docs/organization/` | NOT_ASSESSABLE | No se encontró un registro de riesgos entre las fuentes revisadas. Los candidatos se separan en §6. PA-006. |
| Integridad de calendarios y fechas | Cabeceras y secciones `Calendars`/`Resources` de ambos XML | NOT_MET | Diferencia de horizonte y referencias de calendarios sin correspondencia comprobada. PA-001, PA-002. |
| Tareas, IDs, esfuerzo y duración | Árboles/muestras de tareas; IDs funcionales visibles en XML | NOT_ASSESSABLE | No se leyó cada tarea ni se reconcilió el catálogo completo contra todas las historias; las muestras reflejan duración y trabajo distintos de una fuente a otra. PA-001, PA-004. |
| Dependencias | Muestras de `PredecessorLink`, predecesores de historias y tareas | NOT_ASSESSABLE | Algunos enlaces de tareas son explícitos (p. ej. secuencia TK-001-1 → TK-001-2 → TK-001-3), pero no se pudo validar la red completa ni toda dependencia de requisitos. PA-004, PA-008. |
| Asignaciones y capacidad | Muestras de asignaciones y recursos en ambos XML | NOT_MET | Se observa `Units=1` frente a `MaxUnits=0.25` y `OverAllocated=0`; la falta de calendarios referenciados impide calcular la carga completa. PA-002, PA-003. |
| Costes | Moneda/rates del encabezado y tarifas de recursos revisados | NOT_ASSESSABLE | Los proyectos declaran `$` y tarifas por recurso, pero no se estableció moneda/unidad de tarifa ni se conciliaron todos los costes de asignación y presupuesto. PA-005. |
| Secuencia, hitos, camino crítico y holgura | Fechas, tareas y dependencias revisadas; banderas `Critical` observadas | NOT_ASSESSABLE | Horizontes en conflicto, calendarios incompletos y ausencia de cálculo verificable de float/camino crítico. No se confirma ningún camino crítico. PA-001, PA-002, PA-008. |
| Recursos, habilidades y disponibilidad externa | `docs/organization/` y recursos XML | NOT_ASSESSABLE | `.gitkeep` no acredita capacidades; los calendarios vinculados no están disponibles en `Calendars`. PA-002. |

**Comprobaciones diferidas/no cubiertas:** no se leyeron todos los elementos `<Task>`, `<PredecessorLink>` y `<Assignment>` de los dos XML, ni se recalculó ningún archivo nativo ProjectLibre. No se agregaron cargas horarias por todos los recursos y periodos, no se compararon costes de todas las asignaciones y no se certificó ausencia global de tareas o riesgos no encontrados en las fuentes acotadas.

## 5. Hallazgos

### Índice

| ID | Categoría | Severidad | Confianza | ¿Bloqueador? |
|---|---|---|---|---|
| PA-001 | Baseline/horizonte de planificación | MAJOR | ALTA | Sí |
| PA-002 | Calendarios de recursos | MAJOR | ALTA | Sí |
| PA-003 | Unidades de asignación frente a disponibilidad | MAJOR | ALTA para la inconsistencia declarada; MEDIA para el impacto exacto por periodo | Sí |
| PA-004 | Trazabilidad de requisitos, versiones y alcance | MAJOR | ALTA dentro de las fuentes leídas | Sí |
| PA-005 | Base económica y moneda | QUESTION | ALTA para la falta de base verificable | No confirmado |
| PA-006 | Riesgos y tratamiento | QUESTION | ALTA para la limitación de evidencia | No por sí solo |
| PA-007 | DoR, decisiones y estado de preparación | QUESTION | ALTA para la falta de evidencia | No confirmado |
| PA-008 | Lógica de secuencia, hitos y margen | MAJOR | MEDIA | Sí para validar fechas/camino crítico; no prueba que el plazo sea imposible |

### Registros de evidencia

#### PA-001 — Los XML no establecen un único horizonte de planificación

- **Fuentes/datos:** `docs/Subsonic_Festival-Planificacion_Epicas.pod.xml`, encabezado: `StartDate=2026-10-15T08:00:00`, `FinishDate=2026-10-22T17:00:00`, duración sumaria `PT48H0M0S`. `docs/Subsonic_Festival-Planificacion_Sprints.pod.xml`, encabezado: `StartDate=2026-10-14T08:00:00`, `FinishDate=2026-11-03T13:00:00`, duración sumaria `PT116H0M0S`.
- **Observación:** ambos archivos describen SubsonicFestival y tienen fecha de snapshot `2026-10-16T18:00:00`, pero el primero termina antes de que termine el segundo y ambos asignan distinta duración global. No hay una regla que diga que uno es una vista de alcance parcial o que prevalece sobre el otro.
- **Impacto:** no existe una fecha final y duración de baseline inequívocas para verificar entregas, dependencias, margen, compromisos o coherencia temporal entre la vista de épicas y la de sprints.
- **Acción/pregunta:** ¿cuál archivo representa la planificación vigente? Si son vistas distintas, ¿qué scope y regla de agregación explican la diferencia entre 22 de octubre y 3 de noviembre?
- **Severidad/confianza:** MAJOR, porque impide evaluar el horizonte global; ALTA, porque las fechas aparecen expresamente en ambos encabezados.
- **Bloqueador:** Sí, hasta identificar baseline y relación entre vistas.

#### PA-002 — Recursos vinculados a calendarios que no aparecen definidos

- **Fuentes/datos:** ambos XML, sección `Calendars`, leída hasta `</Calendars>` antes de `<Tasks>`: se identifican calendarios UID 1, 2 y 3. En `Resources`, las personas Javier García, Álvaro Martín, Jaime Arias, Manuel Carvajal y Justo Cilleros declaran `CalendarUID` 4, 5, 6, 7 y 8 respectivamente. El calendario estándar define días laborables con tramos 08:00–12:00 y 13:00–17:00; el encabezado, en cambio, fija `DefaultStartTime=10:00` y `DefaultFinishTime=19:00`.
- **Observación:** no se encontró definición UID 4–8 dentro de las secciones `Calendars` inspeccionadas, y los horarios predeterminados no coinciden con los tramos del calendario estándar. No se puede establecer qué jornada, festivos ni excepciones rigen las personas asignadas.
- **Impacto:** capacidad efectiva por persona/periodo, disponibilidad, duración laborable, carga máxima y cálculos de coste basados en tiempo no son reproducibles desde la evidencia revisada.
- **Acción/pregunta:** confirmar si faltan calendarios de recursos en los XML o si los vínculos deben apuntar a los calendarios definidos; confirmar qué horario gobierna y si existen excepciones/festivos.
- **Severidad/confianza:** MAJOR/ALTA para las referencias UID y divergencia observadas; el efecto operativo exacto requiere validar el XML nativo.
- **Bloqueador:** Sí para declarar viabilidad de recursos, duración y costes por periodo.

#### PA-003 — Asignación de trabajo no conciliada con la disponibilidad declarada

- **Fuentes/datos:** en ambos XML, `Task UID=3`, `MGT IT-001. Sprint planning & grooming`, tiene duración `PT4H0M0S`; la asignación de esa tarea identifica `ResourceUID=3`, `Units=1` y `Work=PT4H0M0S`. El recurso UID 3, Jaime Arias, declara `MaxUnits=0.25` y `PeakUnits=1`, mientras el registro indica `OverAllocated=0`.
- **Observación:** la unidad asignada es 100%, cuatro veces el máximo declarado de 25%; el indicador de pico alcanza 100% aunque no se marca sobreasignación. No se puede reconciliar el dato con calendarios, pues el recurso apunta a `CalendarUID=6`, no definido en la sección de calendarios leída.
- **Cálculo condicional:** si aplicara el calendario estándar de 8 h/día, capacidad declarada al 25% = `8 h/día × 0.25 = 2 h/día`; la asignación de 4 h en la jornada de planificación sería el doble. Este cálculo es condicional, no una medición efectiva, debido al calendario UID 6 no verificado.
- **Impacto:** riesgo material de que el plan sobreestime la capacidad disponible o refleje unidades/capacidad inconsistentes; el estado `OverAllocated=0` no basta para certificar factibilidad.
- **Acción/pregunta:** confirmar si `MaxUnits=0.25` y `Units=1` son correctos para ambos planes y revisar las cargas por periodo frente al calendario real; explicar la bandera `OverAllocated=0`.
- **Severidad/confianza:** MAJOR; ALTA para la diferencia numérica declarada y MEDIA para el impacto de calendario/periodo.
- **Bloqueador:** Sí para el juicio de factibilidad de recursos; no se extrapola a todas las tareas sin agregación completa.

#### PA-004 — IDs y versiones de requisitos no se corresponden entre plan, especificaciones e informe previo

- **Fuentes/datos:** las cinco especificaciones actuales leídas contienen US-001, US-003, US-006, US-007, US-008, US-011 y US-017. Los XML planifican, entre otros, US-002, US-004, US-009, US-014, US-015, US-016 y US-017. En cambio, `requirements-report-v01.md` dice haber revisado US-001, US-003, US-006, US-008, US-009, US-012 y US-018; asocia US-009 a EP-003, US-012 a EP-004 y US-018 a EP-005. La especificación actual de EP-003 leída contiene US-008; EP-004, US-011; EP-005, US-017. La DoD actual referencia seguridad como `US-018`.
- **Observación:** no hay una explicación de versión/renumeración, reemplazo o autoridad que permita reconciliar esas diferencias. Las especificaciones actuales tampoco contienen, en las rutas leídas, definición para varias historias del plan, aunque este sí muestra tareas con esos IDs.
- **Impacto:** no se puede verificar que las tareas planificadas cubran requisitos vigentes, sus criterios de aceptación, predecesores ni DoR. También es incierto si las capacidades adicionales son parte del alcance aprobado.
- **Acción/pregunta:** ¿qué baseline de requisitos rige? Localizar o confirmar las especificaciones autorizadas de los IDs planificados no encontrados y aclarar la discrepancia US-017/US-018 antes de usar la matriz de DoR/DoD.
- **Severidad/confianza:** MAJOR/ALTA dentro de las cinco especificaciones y el informe v01 leídos; las ausencias se limitan a esas rutas.
- **Bloqueador:** Sí para trazabilidad y evaluación completa de alcance/prerrequisitos.

#### PA-005 — Moneda, tarifas y coste total no son comparables

- **Fuentes/datos:** ambos XML declaran `CurrencySymbol=$`, `DefaultStandardRate=10` y `DefaultOvertimeRate=15`. Los recursos revisados incluyen tarifas estándar 25–35 y los objetivos de producto describen precios de entradas en euros. No se encontró en los documentos leídos un presupuesto ni convención que identifique moneda/unidad de las tarifas y el método de coste.
- **Observación:** el símbolo `$` no identifica por sí solo moneda, y los costes de asignación no se conciliaron con el trabajo total de cada recurso, tiempo, reglas de acumulación y baseline.
- **Impacto:** no se puede confirmar coste planificado global ni coherencia económica entre XML. Tampoco se dispone de costes reales con los que comparar forecast.
- **Acción/pregunta:** ¿qué moneda y unidad representan las tarifas, qué regla de coste aplica y cuál es el presupuesto aprobado? Separar coste previsto de coste real.
- **Severidad/confianza:** QUESTION/ALTA para la insuficiencia de evidencia; no se afirma que las tarifas estén equivocadas.
- **Bloqueador:** No confirmado como defecto; sí impide concluir viabilidad económica.

#### PA-006 — No hay evidencia de un registro de riesgos en las fuentes revisadas

- **Fuentes/datos:** fuentes de producto, requisitos, calidad, XML y directorio `docs/organization/`; este último contiene solo `.gitkeep`.
- **Observación:** no se encontró un registro de riesgos, propietario, estado ni tratamiento entre las fuentes indicadas y leídas. Esto no significa que no exista fuera de ese alcance.
- **Impacto:** no es posible revisar riesgo por riesgo, residual, propietario, seguimiento ni correspondencia de mitigaciones con tareas/reservas.
- **Acción/pregunta:** ¿dónde está el registro vigente de riesgos y qué versión debe usarse para esta auditoría?
- **Severidad/confianza:** QUESTION/ALTA respecto de las fuentes revisadas.
- **Bloqueador:** No por sí mismo; la dimensión de riesgos queda NOT_ASSESSABLE.

#### PA-007 — No está demostrada la satisfacción del DoR para los elementos del plan

- **Fuentes/datos:** `definition-of-ready.md`, sección 2.E, exige límite WIP de dos tareas simultáneas y aprobación explícita del PO. No se leyó registro de WIP, aprobación PO ni confirmación de predecesores. El informe `requirements-report-v01.md` también marca WIP y aprobación del PO como NOT_ASSESSABLE para las historias que revisó.
- **Observación:** que las historias tengan campos de estimación o plan inicial no demuestra aprobación ni preparación; además, el plan contiene historias sin especificación actual en las rutas leídas.
- **Impacto:** no puede afirmarse que los elementos planificados fueran Ready al entrar en sus iteraciones.
- **Acción/pregunta:** ¿dónde se documentan la aceptación del PO, el WIP previsto y la verificación de predecesores por historia?
- **Severidad/confianza:** QUESTION/ALTA por ausencia de evidencia, no por confirmar que se incumplió el proceso.
- **Bloqueador:** No confirmado por sí solo; las historias sin trazabilidad quedan bloqueadas por PA-004.

#### PA-008 — Lógica de hitos, secuencia y márgenes no se puede certificar

- **Fuentes/datos:** tareas y enlaces revisados en ambos XML; por ejemplo, TK-001-1 → TK-001-2 → TK-001-3 aparece como cadena Finish-to-Start en las muestras, mientras las dos cabeceras y varias tareas muestran fechas distintas entre planes. Los registros de tareas revisados tienen `Milestone=0`; se observaron banderas `Critical`, pero no se validó el cálculo.
- **Observación:** no se pudo verificar el grafo completo, los hitos de aceptación/entrega, float, margen ni relación de cada iteración con el horizonte global, especialmente con los calendarios de recursos sin correspondencia y la diferencia PA-001.
- **Impacto:** no es posible confirmar paralelización factible, camino crítico, margen para incertidumbre ni fechas de entrega. Una bandera `Critical=1` del XML no demuestra que el camino crítico esté correctamente calculado.
- **Acción/pregunta:** confirmar hitos y predecesores obligatorios contra el baseline elegido; suministrar la red de dependencias, calendarios aplicables y criterio de cálculo para revisar camino crítico y holguras.
- **Severidad/confianza:** MAJOR/MEDIA; está confirmada la falta de base suficiente para verificar, pero no que el plazo sea imposible.
- **Bloqueador:** Sí para declarar viabilidad temporal; no se afirma imposibilidad de entrega.

## 6. Auditoría de riesgos

### Riesgos documentados

**Not found in the reviewed sources:** no se encontró un registro de riesgos en los documentos listados en §2 ni en `docs/organization/` (solo `.gitkeep`). Por tanto, no se dispone de registros a evaluar por situación, evento, consecuencia, tratamiento, propietario, estado o seguimiento. La dimensión no es evaluable por riesgo individual.

### Riesgos candidatos — requieren confirmación humana

| ID | Etiqueta | Evidencia y posible consecuencia | Pregunta/tratamiento a confirmar |
|---|---|---|---|
| CR-01 | CANDIDATE_RISK — Calendarios de recursos sin resolver | UID 4–8 referenciados, no identificados en la sección `Calendars` leída; puede alterar disponibilidad, esfuerzo temporal y coste (PA-002). | ¿Faltan definiciones de calendarios o hay referencias incorrectas? Confirmar calendarios y excepciones. |
| CR-02 | CANDIDATE_RISK — Sobreasignación individual | Un recurso con disponibilidad máxima declarada de 25% tiene una asignación revisada con Units=1 y pico=1 (PA-003). | ¿La asignación es deliberada y compatible con el calendario y la disponibilidad humana? |
| CR-03 | CANDIDATE_RISK — Baseline y requisitos divergentes | Dos horizontes distintos y IDs no conciliados entre planificación, especificaciones e informe de requisitos (PA-001, PA-004). | ¿Cuál versión gobierna y cómo se documentaron las diferencias? |
| CR-04 | CANDIDATE_RISK — Alcance y flujo esencial incompletos/no trazados | G-01/S-01 requieren reserva simulada; los documentos consultados describen catálogo y selección, pero no se verificó un recorrido de reserva completo y el plan añade proveedores, OAuth, administración/analítica y seguridad avanzada. | ¿Qué capacidades y roles forman el incremento aprobado? ¿Qué historia cubre el recorrido medido por M-01? |
| CR-05 | CANDIDATE_RISK — Costes no comparables | Tarifas en el XML sin unidad/moneda aclarada y sin presupuesto o cálculo total contrastable (PA-005). | Confirmar moneda, base de tarifas, forecast y presupuesto. |

No se asignan probabilidades, impactos cuantitativos, dueños ni reservas a estos candidatos porque no están documentados. Las acciones sugeridas no son tratamientos aprobados.

## 7. Auditoría de ProjectLibre

| Control | Evidencia | Resultado |
|---|---|---|
| Formato y baseline | Los dos `.pod.xml` son XML compatible Project, con `SaveVersion=14`, `CurrentDate=2026-10-16T18:00:00` y distinto alcance temporal. Los `.pod` nativos no se inspeccionaron. | NOT_MET como baseline único; PA-001. |
| Calendario base | El calendario estándar revisado contiene tramos 08:00–12:00 y 13:00–17:00. Encabezado indica horario predeterminado 10:00–19:00. | NOT_MET por discrepancia horaria sin regla aclaratoria; PA-002. |
| Calendarios de recursos | Recursos referencian UID 4–8; la sección `Calendars` revisada define UID 1–3. | NOT_MET; PA-002. |
| Recursos, capacidad y tarifas | Ambos planes listan Javier García, Álvaro Martín, Jaime Arias, Manuel Carvajal y Justo Cilleros, con MaxUnits 0.25–0.65 y tarifas estándar 25–35; calendarios UID 4–8. | NOT_ASSESSABLE para capacidad efectiva por falta de calendario resuelto; coste no reconciliado, PA-002/PA-005. |
| Tareas e IDs | Muestras incluyen gestión IT-001–IT-006 y tareas US/TK como US-001, US-006, US-008, US-009, US-014, US-015 y US-016. Se mantienen los IDs originales en este informe. | NOT_ASSESSABLE para completitud/duplicados globales; PA-004. |
| Estimación, esfuerzo y duración | Ejemplo: TK-001-1 aparece con 5 h de trabajo/duración; tareas sumarias tienen duración y fechas distintas entre XML. | NOT_ASSESSABLE para reconciliación completa; se distingue trabajo de duración; PA-001/PA-004. |
| Dependencias | Hay enlaces Finish-to-Start en la cadena de autenticación revisada y algunos vínculos de historias a tareas de gestión. | NOT_ASSESSABLE para consistencia de red completa; PA-008. |
| Asignaciones | Ejemplo de UID 3: 4 h de trabajo a Units=1 para recurso UID 3; el recurso declara MaxUnits=.25 y PeakUnits=1. | NOT_MET en la coherencia de esa asignación declarada; PA-003. |
| Hitos y restricciones | Muestras de tareas revisadas tienen `Milestone=0`; no se verificaron todas las tareas, restricciones ni fechas. | NOT_ASSESSABLE para hitos del proyecto y restricciones globales; PA-008. |

Los controles NOT_ASSESSABLE no se han rellenado con estimaciones inferidas. No se recalculó ni guardó ninguno de los archivos ProjectLibre.

## 8. Viabilidad de recursos y costes

### Capacidad y carga

- Los recursos declaran MaxUnits entre 25% y 65%; las tarifas estándar visibles son Javier 35, Álvaro 35, Jaime 30, Manuel 30 y Justo 25. El XML no proporciona en la sección revisada disponibilidad por calendario válida para UID 4–8, ni documentación externa de capacidad/ausencias.
- **Ejemplo medible, no agregado:** Jaime Arias, UID 3, `MaxUnits=0.25`; tarea `MGT IT-001. Sprint planning & grooming`, UID 3, se asigna al mismo recurso con `Units=1` y `Work=4 h`. Bajo el calendario estándar condicional de 8 h/día, 25% equivaldría a 2 h/día; 4 h excedería esa capacidad diaria en 2 h (factor 2). Como el recurso apunta a calendario UID 6 no definido en la sección leída, esta comparación es condicional y no constituye carga efectiva por calendario.
- Aunque el XML muestra `OverAllocated=0`, `PeakUnits=1` para el recurso, esos campos no resuelven la discrepancia entre unidades asignadas y máximo disponible. No se declara el resto de recursos globalmente sobreasignado ni libre de sobreasignación.
- Competencias: los nombres/initials de recurso no bastan para validar competencia; `docs/organization/` solo tiene `.gitkeep`. Adecuación de habilidades NOT_ASSESSABLE.

### Costes

- Los planes tienen `CurrencySymbol=$`, tarifas estándar/extra del proyecto 10/15 y tasas estándar individuales indicadas arriba. La unidad monetaria de las tasas, coste calculado por asignación, presupuesto y regla para horas extra no quedaron conciliados.
- No se aportaron costes reales; no se evalúa coste actual. Tampoco se afirma una cifra de coste planificado global porque requeriría validar todas las asignaciones, trabajo, unidad monetaria y reglas temporales.
- **Resultado:** viabilidad de recursos y costes NOT_ASSESSABLE en conjunto. El ejemplo de PA-003 es una inconsistencia de unidades que debe aclararse; no es un cálculo de la carga pico de todo el equipo.

## 9. Secuencialidad

- **Orden y paralelización:** las muestras contienen una cadena secuencial para TK-001-1 → TK-001-2 → TK-001-3. No se verificó que los productos/contratos compartidos permitan toda la actividad paralela entre épicas/sprints.
- **Dependencias explícitas de requisitos:** US-003 depende de US-001; US-007 de US-006; US-008 cita US-002; US-011 cita US-010. En el conjunto de especificaciones actuales leído no aparece US-002 ni US-010; sí hay historias con esos IDs en el plan u otras partes del informe anterior. La relación funcional completa requiere baseline de requisitos coherente (PA-004).
- **Dependencias no confirmadas:** dependencias de recintos aprobados, reservas, proveedores, pago/reserva simulada e infraestructura externa no pueden tratarse como enlaces aprobados por aparecer como supuestos en historias o por estar agrupadas en una secuencia.
- **Fechas e hitos:** las fechas de proyecto discrepan entre los dos XML (PA-001); no se obtuvo una definición compartida del final de cada sprint, del hito del MVP o de aceptación de G-01–G-03. Las muestras revisadas no acreditan hitos de entrega.
- **Camino crítico y holguras:** NOT_ASSESSABLE. Aunque hay campos `Critical` y `CriticalSlackLimit=0`, no se recalculó el plan ni se verificó la red completa, calendarios de recursos, restricciones, duraciones y baseline. No se declara camino crítico, float ni reserva.
- **Estimación e incertidumbre:** las historias actuales revisadas contienen estimaciones e incertidumbre, pero no se confirmó que correspondan a todas las tareas planificadas; el informe de requisitos v01 pertenece a un conjunto de IDs distinto. No se añade ni modifica ninguna estimación.

## 10. Trazabilidad, supuestos y preguntas no resueltas

### Trazabilidad

- G-01/M-01 y S-01 tratan de la compra/reserva simulada, pero la existencia de una historia completa y planificada para seleccionar, confirmar y representar el resultado no quedó establecida en las fuentes actuales leídas. **UNCONFIRMED:** que la selección de US-006 ya implique el recorrido de reserva medido en M-01.
- G-02/M-02 y S-02 exigen gestión de evento/aforo; US-008 se refiere a publicación y entradas, pero parte del plan también contiene recintos y administración con IDs no conciliados.
- G-03/M-03 requiere despliegue/documentación; no se verificó una tarea/hito rastreable en los extractos revisados que demuestre su cobertura.
- EP-004 y el rol Proveedor no tienen vínculo explícito a G-01–G-03 en los documentos leídos. No se concluye que estén excluidos; su inclusión precisa decisión de alcance.
- El plan muestra varias tareas sin especificación actual localizable dentro de las cinco rutas leídas. Esto es una brecha de trazabilidad en ese alcance, no prueba de que no haya documentos en otra ubicación.
- Las exclusiones EX-01–EX-03 prohíben pagos bancarios reales y facturas fiscales; no se encontró tarea explícita de integración real en las muestras. La cuestión es si las funciones adicionales se mantienen con datos simulados.

### Preguntas prioritarias para el equipo

1. **P0:** ¿Cuál XML y fecha de finalización constituyen el baseline vigente, y por qué los horizontes son 22 de octubre y 3 de noviembre?
2. **P0:** ¿Cuál versión de requisitos gobierna? ¿Qué documentación autoriza US-002, US-004, US-009, US-014, US-015 y US-016, y cómo se explica US-017 frente a US-018?
3. **P0:** ¿Dónde están definidos los calendarios UID 4–8? ¿Qué calendario/horario rige los recursos y las fechas de cada plan?
4. **P0:** ¿La asignación `Units=1` de Jaime para 4 h y su `MaxUnits=0.25` son intencionales? ¿Qué explica `PeakUnits=1` y `OverAllocated=0`?
5. **P1:** ¿Qué capacidades del plan son parte del MVP y cuáles son extras aprobados bajo el principio constitucional de disciplina del MVP?
6. **P1:** ¿Dónde está el registro de riesgos vigente y qué tareas, reservas, hitos o responsables implementan cada tratamiento?
7. **P1:** ¿Qué moneda/unidad representan tarifas y costos, qué presupuesto gobierna y cómo se calcula el coste previsto? ¿Hay actuals disponibles?
8. **P1:** ¿Qué historia cubre el recorrido de reserva simulada que mide M-01 y cómo se comprobará M-03?
9. **P2:** ¿Qué registro demuestra aprobación del PO, límite WIP y preparación DoR por historia? ¿Qué definición de hito/float y qué método de cálculo de camino crítico se usan?

## 11. RECHECK crosswalk

No aplica: modo **INITIAL**. No se recibió un informe previo de auditoría de planificación ni un decision log. `requirements-report-v01.md` es un informe de revisión de requisitos, se utilizó como evidencia de apoyo y sus divergencias se registran en PA-004; no se trató como una auditoría previa que haya que cerrar mediante crosswalk.

## 12. Cierre explícito

Esta es una auditoría consultiva. No se modificó ningún requisito fuente, registro de riesgos, estimación, asignación de recursos, calendario, tarifa, dependencia, planificación, coste, prioridad ni decisión humana. No se aprobó ningún baseline, compromiso ni puerta de calidad.

“This is an advisory planning audit. No source requirement, risk register, estimate, resource assignment, calendar, rate, dependency, schedule, cost, priority or human decision was changed. No baseline, commitment or gate was approved.”
