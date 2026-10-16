# Planning audit v01

## 1. Metadatos de auditoría

- **Proyecto:** SubsonicFestival / Web Solutions SL.
- **Modo:** INITIAL.
- **Fecha y hora de revisión:** 2026-10-16 16:40:30 +02:00 (proporcionada en la invocación).
- **Baseline/snapshot:** snapshot accesible del workspace durante esta revisión. No se proporcionó commit, versión ni fecha de baseline; no se atribuye una versión a los archivos actuales.
- **Horizonte:** global, según el encargo; no se pudo determinar el horizonte temporal efectivo de los `.pod`.
- **Alcance solicitado:** épicas y requisitos, sprints, recursos, riesgos, dependencias y viabilidad temporal y económica.
- **Alcance efectivamente inspeccionado:** constitución, misión, objetivos, DoR, DoD, informes de calidad v01/v02, cinco especificaciones EP-001–EP-005, informe previo de revisión inicial y archivos `.pod` de planificación en la medida en que fue posible leerlos. No se pudo inspeccionar el contenido estructurado de las planificaciones de ProjectLibre.
- **Idioma:** español.
- **Agente:** instrucciones de Planning Auditor suministradas en la invocación; versión no indicada. La ruta `.github/agents/planning-auditor.agent.md` no está presente. No se sustituyó por otro agente del repositorio.
- **Modelo/herramientas:** no indicado. Revisión documental mediante lectura de archivos; no se ejecutaron comandos, pruebas ni instalaciones.
- **Limitación principal:** por falta de una representación legible del plan actual, la conclusión global es **NOT_ASSESSABLE**. Este resultado no constituye aprobación ni rechazo de la planificación.

## 2. Inventario de fuentes y evidencia

| Fuente realmente revisada | Función y evidencia consultada | Versión/fecha y limitaciones |
|---|---|---|
| `.specify/memory/constitution.md` | Principios, alcance MVP, datos sintéticos, precedencia y gobierno. La constitución declara prioridad sobre el resto de documentos. | No indica versión ni fecha en el contenido leído. |
| `specs/product/mission.md` | Misión, problema, usuarios y propuesta de valor. | Sin versión indicada. |
| `specs/product/goals.md` | G-01–G-03, M-01–M-03, S-01–S-03, exclusiones y restricciones. | Sin versión indicada. |
| `specs/EP-001-autenticacion-y-roles/spec.md` | US-001, US-003, estimaciones, iteraciones declaradas, precedencias, desgloses y criterios. | Sin versión indicada. |
| `specs/EP-002-catalogo-y-busqueda/spec.md` | US-006–US-007 y sus estimaciones, iteraciones, precedencias y criterios. | Sin versión indicada. |
| `specs/EP-003-gestion-eventos-entradas/spec.md` | US-008, estimación, iteración, predecesor y criterios. | Sin versión indicada. |
| `specs/EP-004-servicios-proveedores/spec.md` | US-011, estimación, iteración, predecesor y criterios. | Sin versión indicada. |
| `specs/EP-005-administracion-y-seguridad/spec.md` | US-017, estimación, iteración, predecesor y criterios. | Sin versión indicada. |
| `docs/quality/definition-of-ready.md` | Checklist DoR, incluidos prioridad justificada, predecesores, WIP y aprobación del PO. | Sin versión indicada. La ruta solicitada con `denitionof_ready.md` no existe. |
| `docs/quality/definition-of-done.md` | Checklist DoD de implementación, pruebas, integración, revisiones y documentación. | Sin versión indicada. La ruta solicitada con `denitionof_done.md` no existe. |
| `docs/quality/requirements-report-v01.md` | Informe de revisión de requisitos v01; alcance, hallazgos y limitaciones declarados en ese informe. | Fecha consignada: 2026-10-07 10:14:27 +02:00. Documento secundario, no baseline del plan. |
| `docs/quality/requirements-report-v02.md` | Recheck de requisitos, hallazgos vigentes y matriz DoR. | Fecha consignada: 2026-10-14 10:43:12 +02:00. Sin registro de decisión humana según el propio informe. |
| `docs/project/reviews/initial-planning/initial-planning-review-v01.md` | Revisión previa de planificación y cálculos sobre un extracto de US-001–US-017. | Fecha consignada: 2026-10-10. El propio informe indica que el extracto no tenía ID/versión de baseline y que sus cálculos de capacidad eran condicionales. No es evidencia de la asignación actual de los `.pod`. |
| `docs/Subsonic_Festival-Planificacion_Epicas.pod` | Se intentó lectura directa. La vista muestra serialización binaria Java de ProjectLibre (`ProjectData`); no expone de forma interpretable el inventario, enlaces y asignaciones completos. | No se pudo establecer versión o fecha. |
| `docs/Subsonic_Festival-Planificacion_Sprints.pod` | Se intentó lectura directa. La vista muestra serialización binaria Java de ProjectLibre (`ProjectData`); no expone de forma interpretable el inventario, enlaces y asignaciones completos. | No se pudo establecer versión o fecha. |
| `docs/organization/` | Listado del directorio. Solo se encontró `.gitkeep`. | No aporta calendarios, capacidad, competencias, disponibilidad ni tarifas. |
| `docs/project/` | Listado para localizar los informes existentes `planning-audit-vNN.md`. Contiene `reviews/`; no se observó un informe previo con ese patrón en este directorio. | Se revisó también el informe previo de revisión inicial indicado arriba; no se encontró registro de decisiones humanas. |

### Precedencia, conflictos y límites del inventario

- Se aplicó la regla explícita de la constitución: prevalece sobre otros documentos. No se encontró una regla adicional de precedencia que resuelva qué versión de las planificaciones debe gobernar cuando difieren las referencias históricas.
- Las rutas inexistentes solicitadas y las rutas reales usadas se indican en el manifiesto; no se asumió que nombres parecidos sean la misma versión salvo por su contenido y ubicación en el repositorio.
- El informe previo de revisión inicial contiene un extracto y cálculos de carga anteriores. No se pudo comparar ese extracto con los datos actuales de los `.pod`; no se toma como baseline vigente ni como decisión del equipo.
- No se encontró un registro de riesgos independiente en las fuentes revisadas. Por ello no es posible hacer evaluación riesgo por riesgo de un registro que no fue proporcionado.
- No se aportaron exportaciones XML/CSV de ProjectLibre, calendario/capacidad por recurso, tarifas, registro de actuals, acta de decisiones, baseline aprobada ni horizonte fechado.
- Los resultados de ausencia se limitan a las rutas y documentos enumerados. No significan que esos artefactos no existan en otra ubicación.

## 3. Evaluación general

**Resultado recomendado: NOT_ASSESSABLE.**

El alcance global solicitado no puede evaluarse de forma fiable porque los dos archivos nativos de ProjectLibre no se pudieron interpretar como listas de tareas y recursos. Por tanto, no se pueden confirmar el contenido del cronograma, calendario efectivo, dependencias, asignaciones, carga temporal, costes, hitos, camino crítico ni holguras. La falta de esta evidencia es un bloqueo para emitir una conclusión de viabilidad global, no prueba de que el plan sea inviable.

Sí se pudieron revisar documentos de requisitos y planificación declarativa. Se detectan brechas que requieren resolución o evidencia adicional:

1. Las especificaciones citan US-002 como predecesor de US-008 y US-010 como predecesor de US-011; esos IDs no aparecen en los cinco `spec.md` revisados. La dependencia y su presencia en los planes quedan sin validar.
2. El DoR requiere justificación de negocio para la prioridad MoSCoW; las siete historias revisadas muestran prioridad pero no esa justificación. Tampoco hay evidencia del estado WIP ni de aprobación explícita del PO.
3. La revisión de planificación v01 consignó sobrecarga condicional y una discordancia de horizonte/capacidad a partir de un extracto no versionado. No se pudo confirmar ni descartar que esas cifras correspondan a los `.pod` actuales.
4. La DoD refiere seguridad a US-018, mientras que la especificación de seguridad actualmente revisada es US-017. Debe confirmarse la referencia de control aplicable.

**Bloqueo de evaluación:** la ausencia de datos legibles del plan actual impide contrastar épicas y sprints, y calcular viabilidad temporal o económica. La recomendación no aprueba, certifica ni compromete recursos.

## 4. Matriz de cobertura

| Dimensión/comprobación | Alcance inspeccionado | Estado | Evidencia y hallazgos |
|---|---|---|---|
| Alineación con misión, objetivos, alcance y exclusiones | Misión; G-01–G-03, S-01–S-03, EX-01–EX-03; EP-001–EP-005 | MET para identificar las reglas; NOT_ASSESSABLE para validar cobertura del plan | Constitución, misión y goals leídos; no se pudo relacionar cada tarea/milestone de ProjectLibre con objetivos. |
| Riesgos documentados y tratamientos | Fuentes configuradas y documentos enumerados | NOT_ASSESSABLE | No se encontró registro de riesgos en las fuentes revisadas; hallazgos R-01–R-03 son candidatos, no riesgos confirmados. |
| Calendario del proyecto y calendarios de recursos | Ambos `.pod`; `docs/organization/` | NOT_ASSESSABLE | `.pod` opacos y directorio de organización solo con `.gitkeep`; F-01. |
| IDs/nombres de tareas y estimaciones | Ambos `.pod`; requisitos de EP-001–EP-005 | NOT_ASSESSABLE | No se pudieron recuperar tareas de ProjectLibre. Las estimaciones de requisitos no prueban que se hayan copiado al plan. |
| Dependencias y restricciones | Predecesores declarados en siete historias y ambos `.pod` | NOT_ASSESSABLE en el plan; NOT_MET en trazabilidad de US-008/US-011 | F-02: US-002 y US-010 no están en los cinco specs revisados; vínculos del plan no legibles. |
| Asignaciones de recursos y capacidad por período | `.pod`; `docs/organization/` | NOT_ASSESSABLE | No hay asignaciones/capacidad legibles o evidencia organizativa; F-01. |
| Viabilidad de costes | `.pod`; información de tarifas/presupuesto | NOT_ASSESSABLE | Sin tasas, unidades, reglas de coste ni trabajo asignado legibles; F-01. |
| Hitos, fechas, secuencia, camino crítico y holguras | `.pod` | NOT_ASSESSABLE | No hay red de precedencias ni calendario legibles con los que calcularlos; F-01. |
| DoR aplicado a historias planificadas | US-001, US-003, US-006, US-007, US-008, US-011, US-017 | NOT_MET parcialmente; NOT_ASSESSABLE parcialmente | Prioridad sin justificación documentada (F-03). Predecesores, WIP, aprobación PO y estado de Ready no acreditados. |
| Verificación DoD | Reglas DoD y sus referencias | NOT_ASSESSABLE | La planificación no demuestra implementación ni pruebas; además, discrepancia US-018/US-017 (F-04). |
| Coherencia entre planning de épicas y sprints | `.pod` de épicas y `.pod` de sprints | NOT_ASSESSABLE | Ambos archivos se inspeccionaron directamente, pero su estructura serializada impide comparar registros de forma fiable; F-01. |

### Comprobaciones diferidas o fuera de alcance de evidencia

- Carga por persona y por sprint, holguras, camino crítico, nivelación de recursos, coste planeado y coste real.
- Disponibilidad y competencias por persona, tarifas, calendario laboral y excepciones.
- Confirmación de que las historias de los cinco specs representan la totalidad del alcance del proyecto.
- Verificación de cumplimiento DoD: no se inspeccionaron implementación, pruebas, PRs ni evidencias de integración.

## 5. Hallazgos

### 5.1 Índice

| ID | Categoría | Severidad | Confianza | Bloqueador en el alcance |
|---|---|---|---|---|
| F-01 | Evidencia/ProjectLibre y evaluabilidad global | MAJOR | Alta | Sí, bloquea evaluar viabilidad global |
| F-02 | Dependencias y trazabilidad de requisitos | MAJOR | Alta dentro de las fuentes revisadas | Sí, para verificar secuencia de US-008 y US-011 |
| F-03 | DoR/prioridad y estado de preparación | MAJOR | Alta para la ausencia de justificación; no evaluable para aprobaciones/WIP | Sí, para afirmar Ready de las historias afectadas |
| F-04 | Consistencia de la referencia DoD/seguridad | MINOR | Alta | No; requiere aclaración de trazabilidad |
| F-05 | Evidencia histórica de carga no reconciliada | QUESTION | Media | No es defecto confirmado del plan actual; pregunta pendiente antes de reutilizar esos cálculos |

### 5.2 Registros detallados

#### F-01 — Los archivos ProjectLibre no permiten verificar la planificación global

- **Fuentes y referencia:** `docs/Subsonic_Festival-Planificacion_Epicas.pod` y `docs/Subsonic_Festival-Planificacion_Sprints.pod`; lectura directa del encabezado y contenido disponible, que muestra un flujo binario de serialización Java de clases ProjectLibre como `ProjectData`.
- **Observación/evidencia:** no fue posible leer de forma fiable filas de tareas, duraciones, asignaciones, recursos, predecesores ni costos. Aunque aparecen datos serializados (incluidos nombre de proyecto y un calendario rotulado `Estandar`), no se pueden interpretar con seguridad como un calendario o cronograma completos.
- **Impacto:** no se puede reconciliar el plan de épicas con el de sprints ni evaluar capacidad, secuencia, costos, hitos, camino crítico o margen. No se puede establecer qué baseline representan los archivos.
- **Severidad/confianza:** MAJOR, porque faltan datos esenciales para la evaluación solicitada; confianza ALTA respecto a la limitación de lectura.
- **Bloqueador:** sí para la conclusión de viabilidad global; no afirma que el plan sea defectuoso.
- **Acción/pregunta:** facilitar exportación legible compatible con ProjectLibre, preferiblemente XML o tablas de tareas, recursos, asignaciones, calendarios, vínculos, unidades, costos y fechas, e identificar baseline/versión. ¿Qué exportación es la referencia aprobada para comparar ambos planes?
- **Cálculo:** no realizado; faltan datos interpretables.

#### F-02 — Dos predecesores declarados no están trazados en las especificaciones revisadas

- **Fuentes y referencias:** `specs/EP-003-gestion-eventos-entradas/spec.md`, US-008, campo **Predecesores: US-002**; `specs/EP-004-servicios-proveedores/spec.md`, US-011, campo **Predecesores: US-010**. Se revisaron los cinco `specs/EP-*/spec.md` listados en el manifiesto.
- **Observación/evidencia:** US-002 y US-010 no aparecen en esos cinco documentos. El informe de requisitos v02 también señala que no localizó esos IDs en los cinco specs. Esto no demuestra que no existan fuera del alcance revisado.
- **Impacto:** no se conoce el entregable ni el estado de los predecesores y no se puede verificar la secuencia ni el criterio DoR de US-008 y US-011. Los enlaces del plan ProjectLibre tampoco pudieron leerse.
- **Severidad/confianza:** MAJOR; confianza ALTA dentro de las fuentes nombradas y consultadas.
- **Bloqueador:** sí para validar la secuencia/readiness de US-008 y US-011, no prueba un ciclo ni una secuencia incorrecta.
- **Acción/pregunta:** aportar la especificación autorizada de US-002 y US-010 o aclarar los IDs; confirmar si cada relación es un prerrequisito obligatorio, una interfaz compartida o solo preferencia de secuenciación.

#### F-03 — No se acredita el cumplimiento del DoR para priorización y preparación

- **Fuentes y referencias:** `docs/quality/definition-of-ready.md`, §2.C y §2.E; siete historias de `specs/EP-001` a `specs/EP-005`; `docs/quality/requirements-report-v02.md`, §3, §6.2–6.3.
- **Observación/evidencia:** las siete historias revisadas contienen una prioridad Must/Should, pero no una justificación de negocio explícita, que es un criterio expreso del DoR. El DoR también exige que los predecesores obligatorios estén completados o planificados en la misma iteración, que no se exceda el WIP de dos tareas simultáneas por miembro y que exista aprobación explícita del PO. No se aportó evidencia de estado de predecesores, WIP ni aprobación.
- **Impacto:** las historias no pueden declararse Ready basándose solo en su presencia en el plan o en que tengan una prioridad y estimación. La planificación por iteraciones declarada en requisitos no acredita aprobación ni capacidad.
- **Severidad/confianza:** MAJOR, confianza ALTA sobre la falta de justificación de prioridad en los textos revisados; WIP y aprobación se clasifican como no evaluables, no como incumplimientos demostrados.
- **Bloqueador:** sí para afirmar que las siete historias cumplen íntegramente el DoR; la limitación de evidencias WIP/PO no se convierte por sí sola en prueba de incumplimiento.
- **Acción/pregunta:** documentar la justificación de negocio acordada y aportar evidencia de revisión/aprobación del PO, estado de predecesores y carga WIP para el período planificado.

#### F-04 — La DoD y la especificación actual usan IDs distintos para el control de seguridad

- **Fuentes y referencias:** `docs/quality/definition-of-done.md`, §2.C: seguridad e higiene remite a `US-018`; `specs/EP-005-administracion-y-seguridad/spec.md`: la historia de seguridad leída es US-017. `docs/quality/requirements-report-v01.md` contiene un alcance anterior que también citaba US-018; el informe v02 identifica US-017.
- **Observación/evidencia:** no está explicado si US-018 es un ID obsoleto, una historia adicional no incluida en los cinco specs o una referencia incorrecta de DoD.
- **Impacto:** trazabilidad de la condición de seguridad de la DoD y de sus pruebas incierta. No se afirma que la seguridad no esté planificada o implementada.
- **Severidad/confianza:** MINOR; confianza ALTA para la diferencia textual.
- **Bloqueador:** no para evaluar recursos, pero debe aclararse para verificar el gate de calidad aplicable.
- **Acción/pregunta:** ¿qué historia de seguridad debe gobernar la DoD y dónde está su especificación vigente?

#### F-05 — Los cálculos de capacidad del informe previo no se pueden confirmar para el plan actual

- **Fuentes y referencias:** `docs/project/reviews/initial-planning/initial-planning-review-v01.md`, §§1–2, 4–6; afirma que el extracto revisado no tenía versión de baseline y califica sus cálculos de capacidad como condicionales a que horas y h-p fueran comparables. Los `.pod` actuales no pudieron interpretarse (F-01).
- **Observación/evidencia:** la revisión anterior calcula para el extracto IT-001 = 122 h-p frente a 47,5 h declaradas (diferencia condicional +74,5 h-p), IT-002 = 66 h-p (+18,5 h-p), y registra discordancia entre seis semanas, tres iteraciones nombradas y la cadencia semanal citada en aquella revisión. No hay evidencia legible de que esos valores sean los de los `.pod` actuales ni de que el equipo los haya adoptado.
- **Impacto:** reutilizar esos números como actuales podría dar una falsa conclusión de sobrecarga o de capacidad suficiente; no se puede calcular carga actual ni afirmar que el hallazgo histórico siga abierto o resuelto.
- **Severidad/confianza:** QUESTION, confianza MEDIA: alta respecto a lo que documenta el informe previo, baja respecto a su aplicabilidad al snapshot actual.
- **Bloqueador:** no es un defecto confirmado de la baseline actual. La discrepancia histórica debe reconciliarse antes de usar esos cálculos para decisiones.
- **Acción/pregunta:** ¿el extracto citado en la revisión v01 corresponde a una revisión del plan anterior o a una decisión aceptada? Facilitar la decisión humana y los datos actuales de capacidad, unidad y duración por iteración.
- **Método/unidades:** cálculo citado del informe previo, no recalculado; 122 − 47,5 = 74,5 y 66 − 47,5 = 18,5, solo si h-p y horas disponibles son unidades comparables.

## 6. Auditoría de riesgos

### Registro documentado

**Not found in the reviewed sources:** no se encontró un registro de riesgos ni registros de tratamientos en el manifiesto revisado. En consecuencia, no hay riesgos registrados que puedan evaluarse por contexto, evento, consecuencia, respuesta, responsable, indicador, exposición residual o vínculo a tarea. No se infiere que el registro no exista en otra ubicación.

### Riesgos potenciales detectados (CANDIDATE_RISK)

| ID | Evidencia y posible causa-evento-consecuencia | Tratamiento/trazabilidad observados | Pregunta |
|---|---|---|---|
| CANDIDATE_RISK-01 — Capacidad o secuencia distinta del extracto histórico | El informe anterior anota sobrecarga condicional en IT-001/IT-002 y ambigüedad de horizonte; el plan actual no fue legible. Si esas limitaciones siguieran en el baseline, podrían afectar entregas por sprint. | No se puede comprobar mitigación, reserva, asignación ni responsable en los `.pod`; F-01/F-05. | ¿Qué capacidad por sprint y qué versión del plan están vigentes? |
| CANDIDATE_RISK-02 — Dependencias no identificadas | US-008/US-011 dependen de US-002/US-010, no localizadas en los specs revisados. Si el trabajo requerido no está especificado o planificado, puede bloquear la secuencia de ambas historias. | No se pudo confirmar en los `.pod`; F-02. No se supone que los IDs estén ausentes fuera de los documentos revisados. | ¿Dónde están los artefactos de esos predecesores y qué condición de salida requieren? |
| CANDIDATE_RISK-03 — Servicios externos/infraestructura supuestos | US-006 supone almacenamiento de objetos/CDN simulado; US-007 menciona Redis, HTTP/2 y compresión; US-011 supone SMTP simulado o pasarela; US-017 supone certificado TLS. Si estos servicios no estuvieran disponibles o su trabajo no estuviera planificado, podrían afectar pruebas o secuencia. | Son supuestos escritos en las especificaciones; no se verificó disponibilidad, responsable, tarea de configuración ni plan de contingencia por la opacidad del plan. | ¿Qué servicios son decisiones confirmadas y cuáles alternativas, y dónde se planifican y prueban? |

Estos son candidatos para confirmación humana, no probabilidades, impactos cuantitativos ni riesgos aceptados. No se evaluó exposición con escalas no suministradas.

## 7. Auditoría de integridad de ProjectLibre

| Elemento | Resultado | Evidencia y límite |
|---|---|---|
| Archivo de épicas | NOT_ASSESSABLE | Se intentó leer `docs/Subsonic_Festival-Planificacion_Epicas.pod`; serialización binaria Java de ProjectLibre. No se pudieron recuperar registros de tareas con fiabilidad. |
| Archivo de sprints | NOT_ASSESSABLE | Se intentó leer `docs/Subsonic_Festival-Planificacion_Sprints.pod`; el mismo límite de interpretación. |
| Calendario base/horario/excepciones | NOT_ASSESSABLE | El flujo muestra referencias a calendario y un rótulo `Estandar`, pero no evidencia legible suficiente de jornadas, horas, festivos, excepciones ni calendarios por recurso. |
| Recursos, unidades, disponibilidad y tarifas | NOT_ASSESSABLE | No se pudieron extraer registros completos; `docs/organization/` solo contiene `.gitkeep`. |
| IDs, nombres, estimación, trabajo y duración de tareas | NOT_ASSESSABLE | No se recuperó la tabla de tareas. No se equipara esfuerzo (h-p) con duración transcurrida. |
| Fechas, hitos y restricciones | NOT_ASSESSABLE | No se pudieron verificar fechas ni relaciones con calendario o restricciones. |
| Dependencias, tipo de vínculo y adelantos/retrasos | NOT_ASSESSABLE | No se recuperaron vínculos. Las precedencias de los requisitos no prueban que existan en ProjectLibre. |
| Asignaciones y trabajo asignado | NOT_ASSESSABLE | Sin asignaciones legibles no se pueden reconciliar horas de tarea, unidades y calendario de recurso. |
| Integridad entre épicas y sprints | NOT_ASSESSABLE | No se pudieron contrastar los dos archivos. |

Las especificaciones sí declaran las siguientes asignaciones iniciales de iteración, que son evidencia de requisitos y no exportación del plan: US-001→IT-001, US-003→IT-004, US-006→IT-002, US-007→IT-006, US-008→IT-002, US-011→IT-004 y US-017→IT-005. No se verificó que los `.pod` reflejen esas declaraciones ni que las iteraciones estén fechadas o tengan capacidad asignada.

## 8. Viabilidad de recursos y costes

- **Capacidad por persona/período:** NOT_ASSESSABLE. No hay calendarios, disponibilidad, unidades de asignación o períodos legibles ni datos de recursos en `docs/organization/`.
- **Carga y sobreasignaciones:** NOT_ASSESSABLE. No se dispone de trabajo asignado por recurso y período; no se afirma que exista o no exista sobreasignación.
- **Esfuerzo/duración/disponibilidad:** NOT_ASSESSABLE. Las historias documentan estimaciones h-p, pero estas no indican por sí solas duración transcurrida, concurrencia, asignación efectiva ni capacidad.
- **Competencias:** NOT_ASSESSABLE. No se proporcionaron competencias requeridas ni perfil de recursos.
- **Tarifas/costos previstos:** NOT_ASSESSABLE. No hay tarifas, reglas monetarias, datos de asignaciones legibles ni presupuesto; no se calcula costo.
- **Costos reales:** NOT_ASSESSABLE / no suministrados. No se confunden costos planeados con costos reales.
- **Comparación histórica condicional:** los valores de la revisión de planificación v01 se presentan en F-05 únicamente como antecedente. No se consideran cálculo de capacidad actual ni evidencia de carga de recursos individuales.

No se concluye viabilidad numérica ni de competencias a partir de la mera asignación de una historia a un sprint.

## 9. Secuencialidad y viabilidad temporal

- **Orden/parallelización:** NOT_ASSESSABLE en los planes. Las especificaciones declaran US-003←US-001, US-007←US-006, US-008←US-002, US-011←US-010 y US-017←US-001; faltan los detalles de US-002/US-010 en el conjunto de specs inspeccionado y los vínculos reales del plan.
- **Dependencias técnicas/externas:** las especificaciones enumeran supuestos de servicios (CANDIDATE_RISK-03), pero no se verificaron tareas de aprovisionamiento, contratos, responsables ni disponibilidad.
- **Hitos/fechas:** NOT_ASSESSABLE. No se pudo recuperar calendario o fecha de hitos del `.pod`.
- **Camino crítico:** no calculado ni confirmado. Faltan dependencias, duraciones interpretables, calendarios, restricciones y método de cálculo.
- **Holgura/margen/reservas:** NOT_ASSESSABLE. No hay datos legibles de float ni reserva documentada.
- **Coherencia de iteraciones:** los specs dan las asignaciones iniciales enumeradas en §7, incluyendo IT-004, IT-005 e IT-006. El DoR menciona IT-001, IT-002 e IT-003 como ejemplos del campo iteración, lo cual merece confirmar como nomenclatura/plantilla frente a los IDs posteriores; no se declara una contradicción obligatoria porque el texto puede ser ejemplificativo.
- **Riesgo de acumulación de trabajo:** candidato, no defecto confirmado. Sin capacidad y carga por sprint no se puede establecer acumulación, margen o fecha inviable.

## 10. Trazabilidad, supuestos y cuestiones sin resolver

### Trazabilidad disponible

- **Objetivos y límites:** goals define G-01–G-03, alcance S-01–S-03 y exclusiones EX-01–EX-03. Misión centra a compradores y promotores/organizadores; la constitución prioriza el flujo MVP, los datos ficticios y trazabilidad.
- **Requisitos e iteraciones declaradas:** EP-001–EP-005 incluyen las siete historias listadas en §7 con estimaciones, prioridad, incertidumbre y algunas dependencias. Esos campos no verifican la asignación en el ProjectLibre ni el estado de Ready.
- **Riesgos y tareas:** no se pudo establecer trazabilidad desde un registro de riesgos a tareas, reservas, hitos, recursos o responsables.
- **Tareas/subtareas:** US-001 contiene un desglose TK-001-1, TK-001-2 y TK-001-3 dentro de IT-001 con 5, 3 y 2 h-p respectivamente. Se inspeccionó en su especificación, pero no se pudo verificar su presencia, vínculos o asignación en el plan.

### Preguntas prioritarias para el equipo

1. **¿Puede facilitarse una exportación legible y versionada de ambos planes, con IDs, tareas, fechas, duraciones, trabajo, vínculos, calendario, recursos, unidades, asignaciones y costos?** Sin ella no se puede cerrar la evaluación global.
2. **¿Cuál es el baseline vigente y qué horizonte/cadencia/capacidad por sprint representa?** Aclarar específicamente si el extracto usado por la revisión v01 sigue aplicando y qué decisión humana se tomó sobre las cifras allí citadas.
3. **¿Dónde están las especificaciones autorizadas de US-002 y US-010 y qué condición define que sus dependencias estén satisfechas?**
4. **¿Se puede acreditar justificación de negocio para las prioridades, aprobación del PO y control WIP del DoR en las historias planificadas?**
5. **¿Qué recursos están disponibles por sprint, con qué calendario, competencias y porcentaje de asignación? ¿Qué tarifas y reglas se usan para costos?**
6. **¿Existe un registro de riesgos vigente y dónde se documentan responsables, respuestas y vínculos a tareas o reservas?**
7. **¿Debe la DoD referirse a US-017 o existe una US-018 vigente fuera de los specs revisados?**
8. **¿Qué servicios supuestos (CDN/almacenamiento, Redis, SMTP y TLS) están confirmados y qué tareas/hitos cubren su disponibilidad y verificación?**

### Supuestos e hipótesis

- No se ha supuesto que los archivos `.pod` sean equivalentes al extracto del informe previo.
- No se han inferido disponibilidad, dedicación, competencias, tasas, fechas, duración de sprint ni reservas.
- Las relaciones que no están respaldadas por una especificación o vínculo legible se consideran no verificadas, no dependencias confirmadas.

## 11. RECHECK crosswalk

Modo **INITIAL**. No se requiere crosswalk de recheck. Se consultó un informe previo de revisión inicial como antecedente documental, pero no se recibió registro de decisiones humanas ni se comparó una baseline anterior versionada con una baseline actual verificable. F-05 documenta esa limitación y no asigna estado de resolución a hallazgos previos.

## 12. Limitaciones y comprobaciones no evaluables

- No fue posible recuperar o validar de los `.pod` la estructura de tareas, predecesores, calendarios, recursos, asignaciones, fechas, costos, actuals o resultados de cálculo de ProjectLibre.
- No se suministró una exportación XML/tabla legible, baseline/commit, horizonte explícito, capacidad de recursos por período, competencias, tasas, presupuesto, registro de riesgos ni registro de decisiones.
- Los informes de requisitos son documentos secundarios y no sustituyen evidencia de planificación; el informe previo de planificación se basó en un extracto no versionado.
- La inspección de cinco especificaciones no demuestra ausencia de otros requisitos fuera de esos archivos.
- No se inspeccionó código, entregables, pruebas, PRs, integración ni datos reales; por tanto, no se afirma cumplimiento del DoD ni finalización de historias.
- Sin calendario, duraciones, dependencias y cálculo reproducible no se confirma camino crítico, float, factibilidad de fechas ni margen.
- Sin asignaciones, disponibilidad y tasas no se verifica capacidad, sobreasignación ni costo previsto; sin actuals no se evalúa costo real.

## 13. Cierre explícito

Esta es una auditoría consultiva. No se modificó ningún requisito fuente, registro de riesgos, estimación, asignación de recursos, calendario, tarifa, dependencia, planificación, costo, prioridad ni decisión humana. No se aprobó baseline, compromiso ni puerta de calidad.
