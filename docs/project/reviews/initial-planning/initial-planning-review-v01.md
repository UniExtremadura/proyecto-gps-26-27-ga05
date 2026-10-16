# Revisión de planificación inicial — v01

## 1. Metadatos de la revisión

- **Proyecto:** SubsonicFestival.
- **Modo:** CONSISTENCY.
- **Baseline/alcance revisado:** extracto de planificación proporcionado en la solicitud: US-001 a US-017, con estimaciones en horas-persona (h-p) y asignaciones IT-001, IT-002 e IT-003. No se proporcionó un identificador ni versión de baseline o manifiesto; por tanto, no se puede afirmar que este extracto sea la baseline versionada del equipo.
- **Horizonte y capacidad declarados:** seis semanas; capacidad total efectiva de 285 horas y 47,5 horas por Sprint, según la solicitud. No se declara expresamente si las horas de capacidad son horas-persona.
- **Cadencia de referencia:** el contexto del curso fija Sprint de una semana.
- **Fuentes/versiones:** datos de planificación copiados de la solicitud, sin fecha o versión documental; especificaciones bajo `specs/` y objetivos bajo `specs/product/`, sin versión indicada. La misión identifica el producto como SubsonicFestival. El documento de DoR y el de DoD aparecen en el listado del directorio, pero no se pudieron leer en esta revisión.
- **Workbook/extract:** extracto en el mensaje del usuario; no se encontró workbook o manifiesto en `docs/project/`.
- **Fecha de revisión:** 2026-10-10.
- **Informe previo / RECHECK:** no consta informe previo consultable; no es una revisión de recheck.
- **Commit:** no proporcionado.

## 2. Resumen

**Resultado asesor: NOT_READY.** Se identifican **seis hallazgos bloqueantes**. Bajo la interpretación de que las 47,5 horas por Sprint son comparables con las estimaciones en h-p, IT-001 suma **122 h-p**, excede esa capacidad en **74,5 h-p** y equivale a **2,57 veces** su capacidad declarada. IT-002 también excede 47,5 en **18,5 h-p**. Además, el total, la cadencia y el número de iteraciones declarados no son compatibles entre sí sin una aclaración, y las cifras para US-008, US-009 y US-012 difieren de sus especificaciones disponibles.

El alcance de esta conclusión es el extracto y la evidencia legible aquí. No se pudo verificar una baseline versionada, el estado de DoR/DoD ni la consistencia del resto de las historias contra una fuente de planificación canónica. El resultado no determina viabilidad de calendario o asignación individual.

## 3. Inventario de evidencia y matriz de compatibilidad

| Dimensión | Estado | Evidencia | Límite |
|---|---|---|---|
| Identidad y alcance de baseline | Incompatible/incompleto | La solicitud identifica US-001–US-017; no hay ID/versionado de baseline, manifiesto ni workbook visible en `docs/project/`. | Se revisa el extracto del mensaje como entrada declarada, no se confirma que coincida con la baseline oficial. |
| Objetivo y alcance de producto | Parcial | `specs/product/goals.md` define G-01–G-03, S-01–S-03 y EX-01–EX-03. | No se proporcionó una decisión de alcance que vincule cada una de las 17 historias con el alcance de entrega. La cobertura de historias de proveedor y otras capacidades no queda confirmada por esos objetivos. |
| Prioridades | No evaluable | Las especificaciones legibles indican prioridades para algunas historias. | El extracto no incluye prioridades para US-001–US-017; no puede revisarse coherencia de priorización del conjunto. |
| Madurez/DoR | No evaluable | Los archivos de DoR/DoD aparecen en el listado de `docs/organization/`. | No fue posible leer su contenido ni verificar evidencia de cumplimiento historia por historia. |
| Estimaciones y unidades | Parcial/incompatible | El extracto declara h-p; estimaciones fuente disponibles para US-001, US-003, US-006, US-008, US-009 y US-012. | Tres de esas seis no coinciden con la solicitud. No se conoce la unidad explícita de capacidad, ni se dispone de estimaciones de fuente para las demás historias del extracto. |
| Capacidad efectiva | Incompatible/incompleta | Se declaran 285 horas en seis semanas y 47,5 por Sprint. | Falta aclarar si capacidad es h-p; 285/47,5 = 6 Sprint-equivalentes, mientras el extracto asigna a solo tres IT. |
| Horizonte/duración | Incompatible | Seis semanas y tres iteraciones planificadas; el contexto del curso establece Sprint de una semana. | Tres Sprints semanales abarcan tres semanas, no seis. No se debe presumir que cada IT dura dos semanas. |
| Dependencias/capacidades | Parcial | Las especificaciones legibles declaran precedencias para US-003, US-008, US-009 y US-012; las asignaciones de US-001/US-006/US-002/US-011 proporcionadas permiten comprobar parte del orden. | Faltan las especificaciones de varias historias incluidas; no hay matriz completa de dependencias ni datos de capacidades individuales. |
| Coste | N/A | No se declaró que el coste económico fuera requisito de esta revisión. | No se proporcionaron tarifas ni presupuesto. |
| Incertidumbre/supuestos | Parcial | Las especificaciones disponibles asignan niveles de incertidumbre a algunas historias y formulan supuestos. | No hay nivel de incertidumbre para todo el extracto ni validación de supuestos, disponibilidad de integraciones o responsables. |
| Viabilidad del plan | No demostrada | La suma de horas del extracto puede compararse aritméticamente con las capacidades declaradas, con límites de unidad y cadencia indicados. | No hay asignación de personas, calendario detallado, capacidad por habilidad ni evidencia de velocidad; no se evalúa factibilidad de ejecución. |

## 4. Hallazgos

### IPR-v01-001 — Sobrecarga de IT-001 respecto a la capacidad por Sprint

- **Categoría:** Capacidad.
- **Severidad:** CRITICAL.
- **Bloqueante:** SÍ.
- **Fuente/ID:** Extracto de planificación del usuario; US-001, US-002, US-004, US-006, US-008, US-014, US-016 y US-017.
- **Evidencia observada:** IT-001 suma 10 + 14 + 16 + 14 + 18 + 18 + 20 + 12 = **122 h-p**. Frente a 47,5 horas declaradas por Sprint, la diferencia es **+74,5** (122/47,5 = **2,57**). La comparación es condicional a que la capacidad también esté expresada en h-p.
- **Impacto:** IT-001 no cabe en la capacidad declarada de un Sprint si las unidades son comparables. La suma total de capacidad de seis semanas no elimina este exceso localizado por iteración.
- **Acción recomendada:** reconciliar la capacidad en unidades explícitas con la carga de IT-001 y revisar la asignación con el equipo; no se propone aquí mover ni seleccionar historias.
- **Pregunta/decisión requerida:** ¿Las 47,5 horas son horas-persona efectivas del equipo para cada iteración IT? Si sí, ¿qué disposición decide el equipo para el exceso de 74,5 h-p?
- **Posible rol propietario:** equipo de desarrollo y responsable de planificación.

### IPR-v01-002 — Capacidad total, cadencia y número de iteraciones incompatibles

- **Categoría:** Horizonte/capacidad.
- **Severidad:** MAJOR.
- **Bloqueante:** SÍ.
- **Fuente/ID:** Solicitud del usuario; contexto del curso (Sprint de una semana); IT-001–IT-003.
- **Evidencia observada:** 285/47,5 = **6** Sprints semanales equivalentes. El extracto asigna trabajo a tres iteraciones IT a lo largo de seis semanas. Si fueran tres Sprints de 47,5 horas, su capacidad conjunta sería **142,5 horas**, no 285. Si son seis Sprints semanales, no están identificados los otros tres en el extracto. Tres iteraciones de dos semanas serían una interpretación posible, pero contradice la duración de Sprint de una semana y no está declarada como decisión.
- **Impacto:** No se puede interpretar la capacidad efectiva por iteración ni determinar el margen agregado del horizonte con certeza.
- **Acción recomendada:** confirmar la duración de cada IT, el número de Sprints del horizonte y la unidad/periodo al que aplica 47,5; actualizar la fuente humana de planificación para que las cifras sean compatibles.
- **Pregunta/decisión requerida:** ¿El horizonte contiene tres o seis Sprints semanales, y a qué periodo corresponde cada IT y su capacidad?
- **Posible rol propietario:** responsable de planificación o Scrum Master.

### IPR-v01-003 — Datos de US-008 no coinciden con su especificación

- **Categoría:** Consistencia de estimación/asignación.
- **Severidad:** MAJOR.
- **Bloqueante:** SÍ.
- **Fuente/ID:** Extracto del usuario, US-008; `specs/EP-002-catalogo-y-busqueda/spec.md`, US-008.
- **Evidencia observada:** solicitud: **18 h-p, IT-001**. Especificación: **16 h-p, IT-003 (Sprint 3)**; además, la especificación declara dependencia de US-006. En el extracto US-006 se asigna a IT-001.
- **Impacto:** La carga de IT-001 y la distribución entre iteraciones dependen de cuál dato sea vigente. La precedencia con US-006 queda en la misma iteración en el extracto, sin orden intraiteración verificable.
- **Acción recomendada:** pedir al equipo que confirme el valor y la asignación aprobados, conservando el historial o versión de la decisión en la fuente canónica.
- **Pregunta/decisión requerida:** ¿Qué estimación y asignación corresponden a US-008 en la baseline que se pretende revisar?
- **Posible rol propietario:** Product Owner y equipo de desarrollo.

### IPR-v01-004 — Datos de US-009 no coinciden con su especificación

- **Categoría:** Consistencia de estimación/asignación.
- **Severidad:** MAJOR.
- **Bloqueante:** SÍ.
- **Fuente/ID:** Extracto del usuario, US-009; `specs/EP-003-gestion-eventos-entradas/spec.md`, US-009.
- **Evidencia observada:** solicitud: **16 h-p, IT-002**. Especificación: **18 h-p, IT-001 (Sprint 1)**; la especificación registra dependencia de US-002, que en el extracto está en IT-001.
- **Impacto:** Cambian en 2 h-p la carga total y la distribución; con la especificación, US-009 estaría en el mismo Sprint que su precedente US-002, pero no consta secuenciación dentro de la iteración.
- **Acción recomendada:** confirmar el dato vigente en la fuente canónica y verificar el orden de la dependencia sin asumir que una asignación al mismo Sprint demuestra precedencia satisfecha.
- **Pregunta/decisión requerida:** ¿Qué estimación, iteración y orden de dependencia se aceptaron para US-009?
- **Posible rol propietario:** Product Owner y equipo de desarrollo.

### IPR-v01-005 — Datos de US-012 no coinciden con su especificación

- **Categoría:** Consistencia de estimación/asignación.
- **Severidad:** MAJOR.
- **Bloqueante:** SÍ.
- **Fuente/ID:** Extracto del usuario, US-012; `specs/EP-004-servicios-proveedores/spec.md`, US-012.
- **Evidencia observada:** solicitud: **8 h-p, IT-003**. Especificación: **12 h-p, IT-002 (Sprint 2)**; declara dependencia de US-011, asignada a IT-002 en el extracto.
- **Impacto:** Cambian en 4 h-p la carga y la iteración; la especificación ubica US-012 en la misma iteración que su precedente, sin detalle de secuencia.
- **Acción recomendada:** confirmar la estimación y asignación aprobadas, y comprobar la precedencia en la planificación detallada.
- **Pregunta/decisión requerida:** ¿Qué valor y asignación son los vigentes para US-012 y cómo se ordena respecto a US-011?
- **Posible rol propietario:** Product Owner y equipo de desarrollo.

### IPR-v01-006 — Falta identificación/versionado del baseline y cobertura de fuentes

- **Categoría:** Trazabilidad/alcance.
- **Severidad:** MAJOR.
- **Bloqueante:** SÍ.
- **Fuente/ID:** Extracto del usuario, US-001–US-017; árbol de `docs/project/`; especificaciones de `specs/`.
- **Evidencia observada:** no se encontró manifiesto ni workbook de planificación en `docs/project/`; no se indicó versión del extracto. Las especificaciones legibles cubren solo parte de US-001–US-017 y también contienen US-018, ausente del extracto. No se pudo leer el contenido de DoR/DoD. El resultado de alcance de `specs/product/goals.md` no proporciona una matriz que relacione cada historia con el alcance aprobado.
- **Impacto:** No puede certificarse que los datos del mensaje representen la baseline exacta ni revisar compatibilidad de prioridades, alcance y madurez de todas las historias.
- **Acción recomendada:** aportar el manifiesto/workbook o extracto versionado que identifique la baseline, su alcance exacto y la disposición humana de requisitos; hacer accesibles las fuentes de DoR/DoD.
- **Pregunta/decisión requerida:** ¿Cuál es la versión oficial que se somete a revisión, qué IDs cubre y cuál fue la disposición humana de requisitos?
- **Posible rol propietario:** responsable de requisitos o Product Owner.

## 5. Observaciones aritméticas y de capacidad/recursos

Todos los valores de las historias del extracto se suman como h-p. La capacidad del usuario se declara en horas, sin especificar expresamente horas-persona; las comparaciones con estimaciones son, por tanto, condicionales a que las unidades sean equivalentes.

| Iteración declarada | Historias | Carga del extracto | Diferencia frente a 47,5 |
|---|---:|---:|---:|
| IT-001 | 8 | 122 h-p | +74,5 h-p |
| IT-002 | 6 | 66 h-p | +18,5 h-p |
| IT-003 | 3 | 40 h-p | -7,5 h-p |
| **Total** | **17** | **228 h-p** | — |

- **Suma del alcance informado:** 228 h-p. Frente a 285 horas declaradas para el horizonte, la diferencia aritmética es 57 horas de margen solo si ambas cantidades representan unidades compatibles y la capacidad puede agregarse sobre las iteraciones de ese alcance.
- **Capacidad por tres IT:** 3 × 47,5 = 142,5 horas. Frente a 228 h-p, la carga excede esta interpretación en 85,5 h-p.
- **Capacidad de seis Sprints semanales:** 6 × 47,5 = 285 horas, pero el extracto solo nombra tres iteraciones. No se distribuyen historias en otros Sprints y no se infiere dicha distribución.
- **Incertidumbre/exclusiones:** no se declara la composición del equipo, disponibilidad individual, deducciones de capacidad, habilidades, asignaciones, trabajo no incluido ni si el total de 285 se calculó desde disponibilidad efectiva. No se puede derivar capacidad individual ni evaluar cuellos de botella de personas.
- **Tamaño de historias:** la mayor estimación del extracto es US-016 con 20 h-p; ninguna historia individual alcanza por sí sola las 47,5 horas declaradas por Sprint. Sin embargo, eso **no demuestra** que una historia sea abarcable en un Sprint de una semana: h-p no equivalen a duración calendario, no hay capacidad por persona ni regla/umbral de tamaño máximo aprobado. Tampoco hay evidencia para afirmar que una historia individual sea demasiado grande. Lo que sí queda evidenciado es la sobrecarga del conjunto de IT-001 (y de IT-002) bajo la comparación condicional anterior.

## 6. Dependencias y observaciones de capacidades

- **US-003 depende de US-001:** la especificación declara esa precedencia; la solicitud asigna US-001 a IT-001 y US-003 a IT-002, compatible en orden de iteraciones.
- **US-008 depende de US-006:** según la especificación disponible, ambas están en IT-001 en el extracto. La ubicación en una misma iteración no confirma el orden de terminación; la especificación alternativa sitúa US-008 en IT-003.
- **US-009 depende de US-002:** la especificación disponible declara esa dependencia. El extracto sitúa US-002 en IT-001 y US-009 en IT-002, mientras la especificación sitúa US-009 en IT-001; si esa asignación de fuente es la vigente, falta orden intraiteración verificable.
- **US-012 depende de US-011:** la especificación declara la dependencia. El extracto asigna US-011 a IT-002 y US-012 a IT-003, mientras la especificación asigna US-012 a IT-002.
- No se identifica un ciclo con las dependencias que pudieron leerse. No es posible certificar ausencia de ciclos o dependencias externas para las demás historias, porque sus especificaciones no están en la evidencia accesible.
- No hay información de distribución de trabajo por competencias ni capacidades individuales; no se puede identificar un cuello de botella de habilidades ni producir una secuencia temporal.

## 7. Resultado de coste

**N/A:** no se indicó que el coste económico sea requisito de la revisión. No se proporcionaron tarifas, presupuesto ni costes; no se calcula ningún importe.

## 8. Preguntas y siguientes acciones sugeridas

| Acción/pregunta | Rol sugerido | Disparador de validación | Bloqueante |
|---|---|---|---|
| Confirmar si la capacidad por iteración es 47,5 h-p efectivas y reconciliar la carga de IT-001 e IT-002. | Equipo de desarrollo / responsable de planificación | Antes de considerar consistente la capacidad por iteración. | Sí |
| Aclarar si el horizonte tiene tres o seis Sprints de una semana y cómo se relacionan con IT-001–IT-003. | Scrum Master / responsable de planificación | Antes de evaluar el horizonte y el margen agregado. | Sí |
| Resolver las discrepancias fuente/extracto de US-008, US-009 y US-012. | Product Owner / equipo de desarrollo | Antes de fijar cifras de carga y dependencias. | Sí |
| Identificar la baseline exacta, su versión y el alcance aprobado; aportar manifest/workbook y disposición humana de requisitos. | Responsable de requisitos / Product Owner | Antes de emitir consistencia de una baseline oficial completa. | Sí |
| Leer DoR/DoD y verificar su cumplimiento por historia; confirmar el criterio acordado para considerar una historia demasiado grande para un Sprint. | Equipo de desarrollo / responsable de calidad | Antes de concluir sobre madurez y tamaño individual. | Sí |
| Revisar dependencias de todas las historias y disponibilidad por persona/competencia, si se busca evaluar factibilidad de ejecución. | Equipo de desarrollo | Antes de valorar viabilidad de calendario o recursos. | No, fuera del alcance de la evidencia actual |

## 9. Matriz de disposición RECHECK

No aplica: esta revisión no es un RECHECK y no se proporcionó informe previo ni referencias a decisiones humanas posteriores.

## 10. Consejo final y límites

Para el extracto de US-001–US-017, la planificación **no está lista para considerarse consistente**: la carga declarada de IT-001 supera en 74,5 h-p una capacidad de 47,5 por Sprint, si las unidades son comparables; IT-002 también supera ese valor; y la capacidad total, el horizonte y las iteraciones no quedan reconciliados. Asimismo, US-008, US-009 y US-012 discrepan entre el extracto y sus especificaciones disponibles.

No se concluye que una historia individual sea demasiado grande: no hay umbral de tamaño definido ni datos para traducir h-p a duración de una semana. La revisión tampoco acredita factibilidad de calendario, asignación de recursos, calidad de estimaciones o completitud de requisitos. Se requiere aclaración humana de las preguntas bloqueantes antes de construir o evaluar una hipótesis de planificación.

Las fuentes no se modificaron. Se creó únicamente este nuevo informe; no se aprobó compromiso, plan, baseline ni puerta de calidad. Esta revisión asesora exclusivamente sobre la consistencia del extracto y no constituye aprobación de planificación.

### Tabla de trazabilidad sobre la planificación corregida por el agente "initial-planning-reviewer.agent.md":

| Agente e ID | Entrada | Propuesta | Justificación | Decisión |
| :--- | :--- | :--- | :--- | :--- |
| initial-planning-reviewer (P01) | Excel Planificación (US-001 a US-017) y Capacidad | Reevaluar la asignación de historias en la iteración IT-001 e IT-002. | Existe una sobrecarga crítica. IT-001 suma 122 h-p y IT-002 suma 66 h-p, superando con creces la capacidad efectiva máxima del equipo (47,5 h-p por Sprint). | Aceptada (Se redistribuirán las historias hacia los Sprints posteriores para aplanar la curva de esfuerzo). |
| initial-planning-reviewer (P02) | Excel Planificación y `goals.md` | Aclarar la duración del horizonte del proyecto y el número de Sprints. | Se declaran 6 semanas (285 horas totales), pero el catálogo solo asigna tareas a 3 iteraciones (IT-001, IT-002 e IT-003), lo que descuadra el total. | Aceptada con cambios (Se ajustará el Excel para reflejar la distribución en los 6 Sprints o adaptar la duración de cada iteración). |
| initial-planning-reviewer (P03) | Excel Planificación y archivos `spec.md` | Unificar y corregir las estimaciones y dependencias de US-008, US-009 y US-012. | Los datos de esfuerzo e iteraciones reflejados en el Excel de planificación no coinciden con los documentados previamente en sus respectivos archivos de especificación. | Aceptada (Se actualizarán los archivos de especificación para que coincidan exactamente con la fuente principal del Excel). |
