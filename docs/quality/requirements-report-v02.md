# Requirements review v02

## 1. Run metadata

- **Proyecto:** SubsonicFestival / Web Solutions SL.
- **Modo:** RECHECK del informe `requirements-report-v01.md`.
- **Baseline/snapshot:** estado de los archivos accesibles durante esta revisión; no se proporcionó identificador de commit ni versión de baseline.
- **Fecha/hora:** 2026-10-14 10:43:12 +02:00 (proporcionada por la invocación).
- **Agente:** Requirements Reviewer, instrucciones de agente suministradas en la invocación; versión no indicada.
- **Modelo/herramientas:** modelo no indicado. Lectura documental del workspace y creación/verificación del informe.
- **Alcance:** los cinco `spec.md` de EP-001–EP-005 y todas las historias incluidas en ellos: US-001, US-003, US-006, US-007, US-008, US-011 y US-017. También se revisaron misión, objetivos, DoR, DoD e informe v01.
- **Idioma:** español.
- **Limitación de RECHECK:** no se proporcionó un registro de decisiones humanas ni fuentes revisadas específicamente para este recheck. Los estados del crosswalk reflejan los textos accesibles hoy; no certifican que un cambio fuese aprobado por el equipo.

## 2. Source manifest y limitaciones

### Archivos leídos

| Archivo | Papel | Secciones/IDs revisados |
|---|---|---|
| `docs/quality/requirements-report-v01.md` | Informe anterior | Hallazgos F01–F08, matriz DoR, omisiones, dependencias y preguntas |
| `docs/quality/definition-of-ready.md` | DoR compartido | Checklist A–E: 14 criterios concretos |
| `docs/quality/definition-of-done.md` | DoD compartido | Implementación, aceptación/pruebas, seguridad, rendimiento, integración y documentación |
| `specs/product/mission.md` | Misión y actores | Problema, asistentes, promotores/organizadores y propuesta de valor |
| `specs/product/goals.md` | Objetivos y alcance | G-01–G-03, M-01–M-03, S-01–S-03, EX-01–EX-03 y restricciones |
| `specs/EP-001-autenticacion-y-roles/spec.md` | Especificación de épica | US-001 y US-003 |
| `specs/EP-002-catalogo-y-busqueda/spec.md` | Especificación de épica | US-006 y US-007 |
| `specs/EP-003-gestion-eventos-entradas/spec.md` | Especificación de épica | US-008 |
| `specs/EP-004-servicios-proveedores/spec.md` | Especificación de épica | US-011 |
| `specs/EP-005-administracion-y-seguridad/spec.md` | Especificación de épica | US-017 |

### Fuentes no disponibles y límites

- `docs/quality/` contiene el informe v01, DoR y DoD; no contiene un registro de decisiones humanas. `docs/organization/` solo contiene `.gitkeep`; no se encontró allí una constitución o Team Charter.
- No se proporcionaron rutas de constitución, DoR/DoD más recientes, registro de decisiones ni especificaciones revisadas alternativas. Se usaron las fuentes indicadas arriba; no se presume que sean la última autoridad si existen otras.
- La carpeta `docs/project/reviews/initial-planning/` aparece en el árbol disponible, pero no se leyó: no se identificó como registro de decisiones de este recheck y queda fuera del alcance documental solicitado.
- US-002 y US-010 no aparecen en los cinco specs leídos; no se afirma que no existan fuera de estas fuentes.
- Se inspeccionó la evidencia de requisitos, no código, datos, pruebas, despliegues, servicios externos ni decisiones de equipo. No se afirma cumplimiento del DoD.
- No se suministró commit; los cambios entre v01 y los specs actuales solo pueden compararse por su contenido. No se atribuyen a una decisión humana.

## 3. Scoped assessment

**Recomendación: NEEDS_REFINEMENT.**

El alcance revisado comprende siete historias detalladas de EP-001–EP-005. Persisten bloqueos confirmados para Ready:

1. **Criterio DoR de prioridad incompleto (F12):** todas las historias declaran prioridad, pero ninguna acompaña la prioridad MoSCoW de una justificación de negocio explícita, requerida por el DoR.
2. **Comportamiento de búsqueda no cubierto (F09):** US-006 incluye búsqueda por fecha en la historia, pero sus criterios solo definen filtrado por nombre de festival o artista.
3. **Regla de alerta de inventario ambigua (F10):** US-011 no determina con precisión cuándo una venta constituye el evento único de cruce del umbral, ni cómo se coordina con reposición y agotamiento de stock.
4. **Seguridad de datos sin superficie verificable (F04):** US-017 exige cifrado AES-256 de datos personales sensibles en reposo, pero no identifica el conjunto de campos/datos cubierto ni el límite de almacenamiento al que aplica.
5. **Predecesores no trazables (F05):** US-008 sigue citando US-002, no localizada; US-011 cita US-010, tampoco localizada. No hay evidencia de que se cumpla el DoR sobre estado de predecesores.
6. **DoR operativo no demostrable:** aprobación del PO y límite WIP no están acreditados para ninguna historia. No hay evidencia de que el predecesor de las historias con dependencia esté completado o planificado en la misma iteración.

El informe no decide estimaciones, prioridades, divisiones de historias, inclusión de EP-004 ni aceptación de riesgos. Los hallazgos sobre integraciones y granularidad deben confirmarse con el equipo antes de tratarlos como bloqueos de planificación.

## 4. Coverage matrix

| Dimensión | IDs inspeccionados | Resultado | Hallazgos |
|---|---|---|---|
| Claridad y consistencia | US-001, US-003, US-006, US-007, US-008, US-011, US-017 | Requiere refinamiento en fechas de búsqueda, perfiles, rendimiento, estados, alertas y alcance de cifrado | F02, F03, F04, F06, F09, F10, F12 |
| Cobertura y alineación de alcance | EP-001–EP-005; G-01–G-03; S-01–S-03; EX-01–EX-03 | Parcial; faltan decisiones sobre proveedores, reserva y roles | F04, F08; §7 |
| Elementos de especificación | Siete historias; criterios, restricciones, reglas, supuestos y casos límite | Mejoras respecto a v01, pero quedan comportamientos y límites sin criterio observable suficiente | F02, F03, F04, F06, F09, F10, F12 |
| Tamaño/granularidad (INVEST) | US-006, US-007, US-008, US-017 | Varias historias mantienen resultados diferenciables; es una señal para refinar, no una decisión de división | F07 |
| Aceptación y DoR | Siete historias; todos los criterios A–E del DoR | Criterio de prioridad no satisfecho; ambigüedades locales; WIP y aprobación PO no evaluables | F09–F12 |
| Dependencias y supuestos | Predecesores y supuestos de las siete historias; misión y objetivos | Dependencias explícitas no trazadas a fuentes disponibles; integraciones siguen como supuestos | F05, F08 |

## 5. Findings

### 5.1 Índice de hallazgos vigentes

Los identificadores F01–F08 se conservan para el crosswalk. F09–F12 son nuevos hallazgos de este informe.

| ID | Severidad | Categoría | Historias | Confianza | ¿Bloqueador? |
|---|---|---|---|---|---|
| F02 | MAJOR | Aceptación y reglas de negocio | US-003 | Alta | Sí, para el resultado aún ambiguo |
| F03 | MAJOR | Verificabilidad de rendimiento/infraestructura | US-006, US-007 | Media | Parcial: medir de forma reproducible |
| F04 | MAJOR | Seguridad y límites de datos | US-017 | Alta | Sí, para definir alcance verificable de cifrado |
| F05 | MAJOR | Dependencias y trazabilidad | US-008, US-011 | Alta | Sí, para el predecesor obligatorio no localizado |
| F06 | MINOR | Límites y errores de dominio | US-006, US-008, US-011 | Media | No, salvo que el equipo declare esencial un caso omitido |
| F07 | MAJOR | Granularidad INVEST | US-006, US-007, US-008, US-017 | Alta | Por confirmar; depende de estimabilidad/aceptación |
| F08 | QUESTION | Integraciones externas no confirmadas | US-006, US-007, US-011, US-017 | Media | No confirmado |
| F09 | MAJOR | Cobertura de aceptación | US-006 | Alta | Sí, para búsqueda por fecha declarada |
| F10 | MAJOR | Regla de transición de stock/alerta | US-011 | Alta | Sí, para determinar alertas únicas y repetibles |
| F11 | MAJOR | DoR, justificación de prioridad | US-001, US-003, US-006, US-007, US-008, US-011, US-017 | Alta | Sí, incumplimiento explícito del DoR |
| F12 | MINOR | Máquina de estados incompleta | US-008 | Alta | No |

### 5.2 Registros de evidencia

#### F02 — Aún falta un resultado observable en la edición del perfil

- **Categoría:** aceptación y reglas de negocio.
- **Fuente:** `specs/EP-001-autenticacion-y-roles/spec.md`, US-003 AC-02/03/04: la edición de correo requiere contraseña y verificación previa, pero no expresa el resultado tras verificar ni define expiración/reutilización de la verificación.
- **Observación:** US-003 mejoró respecto a v01 al añadir la verificación por correo y errores concretos, pero deja sin criterio de aceptación la confirmación exitosa del cambio.
- **Impacto:** UI y API podrían discrepar sobre cuándo el nuevo correo pasa a ser efectivo.
- **Acción sugerida:** especificar éxito y rechazo del cambio de correo, incluyendo el resultado observable tras la verificación.
- **Confianza:** Alta: la omisión está en los criterios citados.
- **Bloqueador:** Sí para completar esas rutas; no implica que todas las historias de las épicas estén bloqueadas.

#### F03 — Pruebas de rendimiento con condiciones y herramientas no plenamente alineadas

- **Categoría:** verificabilidad, restricciones y dependencias.
- **Fuente:** `specs/EP-002-catalogo-y-busqueda/spec.md`, US-006 RNF: filtrado cliente `< 100 ms (p95)` hasta 500 eventos, verificado con k6 / Postman CLI. US-007 AC-01/03 y RNF: LCP `< 2,0 s` en Fast 4G mediante DevTools/Lighthouse CLI, Redis con TTL 5 min e invalidación, y Lighthouse `> 85/100`.
- **Observación:** las métricas y límites son más concretos que en v01. Sin embargo, no se fija cómo k6/Postman CLI mide el filtrado ejecutado en cliente ni el dispositivo/navegador reproducible para LCP. “Condiciones normales” en la necesidad de US-007 tampoco se vincula a Fast 4G. La herramienta de filtrado podría medir una petición de red en vez de la operación cliente que define el RNF.
- **Impacto:** distintas ejecuciones pueden producir resultados no comparables o comprobar una operación distinta de la requerida.
- **Acción sugerida:** concretar entorno/dataset/navegador para las métricas y la instrumentación del filtrado en cliente; alinear la herramienta con la operación medida.
- **Confianza:** Media: umbrales están escritos, pero el procedimiento descrito admite interpretaciones.
- **Bloqueador:** Parcial; es bloqueador para declarar verificable el RNF, no para el catálogo funcional.

#### F04 — Alcance de seguridad todavía necesita acotar los datos cubiertos

- **Categoría:** seguridad, alcance y verificabilidad.
- **Fuente:** `specs/EP-005-administracion-y-seguridad/spec.md`, US-017 objetivo y restricción: cifrado de datos sensibles en tránsito y reposo, campos personales con AES-256 y credenciales con Bcrypt. Frente a ello, `specs/product/goals.md`, restricciones: prohibición de datos personales, bancarios o de contacto reales; EX-01 excluye pasarelas de pago reales.
- **Observación:** US-017 aclara expresamente que solo se operará con entornos de prueba/datos simulados y excluye pagos reales/PCI-DSS, resolviendo parte de la tensión de v01. No enumera qué campos ficticios deben cifrarse en reposo ni qué datos de prueba se incluyen en el control.
- **Impacto:** no se puede comprobar de forma completa el requisito AES-256 sin una superficie de datos acordada; el uso de datos reales contradiría las restricciones de goals.
- **Acción sugerida:** enumerar los campos ficticios cubiertos y confirmar que los entornos y ejemplos permanecen sin datos reales; definir la evidencia verificable del cifrado sin inventar obligaciones adicionales.
- **Confianza:** Alta para la falta de inventario; la exclusión de pagos está explícita.
- **Bloqueador:** Sí para aceptar el control de cifrado; no se identifica una obligación legal adicional.

#### F05 — Predecesores no trazados en las fuentes revisadas

- **Categoría:** dependencias y trazabilidad.
- **Fuente:** `specs/EP-003-gestion-eventos-entradas/spec.md`, US-008: `Predecesores: US-002`; `specs/EP-004-servicios-proveedores/spec.md`, US-011: `Predecesores: US-010`. Los cinco `spec.md` revisados incluyen US-001, US-003, US-006, US-007, US-008, US-011 y US-017, pero no US-002 ni US-010.
- **Observación:** no se puede comprobar el contenido, estado, contrato ni iteración de esos dos predecesores. US-011 sí está ahora descrita, a diferencia del material que sustentó una parte de F05 en v01, pero su propio predecesor US-010 no está localizado.
- **Impacto:** el criterio DoR de predecesores no puede validarse para US-008/US-011.
- **Acción sugerida:** proporcionar las especificaciones autorizadas de US-002/US-010 o confirmar/corregir sus IDs y clasificar cada dependencia como prerrequisito, contrato compartido o preferencia de secuencia.
- **Confianza:** Alta dentro de los cinco specs leídos; la ausencia no se afirma fuera de esas fuentes.
- **Bloqueador:** Sí para comprobar Ready de US-008 y US-011.

#### F06 — Algunos límites y fallos de dominio siguen sin criterios explícitos

- **Categoría:** reglas y casos límite.
- **Fuente:** EP-002 US-006 define búsqueda textual y estado sin resultados; EP-003 US-008 define validación de fechas, aforo y modalidades; EP-004 US-011 define alerta, reintentos y reposición.
- **Observación:** el material añade varios errores respecto a v01, pero no deja especificados todos los límites que el informe anterior señaló (p. ej., tratamiento de texto vacío/espacios o algunos resultados de fallo de dependencias).
- **Impacto:** según la regla elegida, pueden diferir resultados vacíos y notificaciones. No se asume que cada caso sea requisito esencial.
- **Acción sugerida:** decidir qué límites son esenciales al objetivo de cada historia y añadir solo los comportamientos aceptados, incluidos estados vacíos o de error pertinentes.
- **Confianza:** Media; la necesidad de algunos casos depende de decisiones del PO.
- **Bloqueador:** No por sí solo.

#### F07 — Outcomes independientes permanecen agrupados en historias

- **Categoría:** tamaño/granularidad (heurística INVEST).
- **Fuente:** EP-002 US-006 reúne catálogo, búsqueda y detalle; US-007 agrupa LCP, lazy-loading, caché, invalidación y fallback; EP-003 US-008 reúne creación/configuración, publicación, autorización y control de aforo; EP-005 US-017 reúne transporte, logs, cifrado y respuestas API.
- **Observación:** cada historia contiene varios comportamientos verificables que podrían fallar de forma independiente. El contenido actual no muestra si la estimación acordada contempla todos esos resultados.
- **Impacto:** puede dificultar la aceptación, refinamiento y planificación independiente.
- **Acción sugerida:** valorar cortes verticales que sigan entregando resultados útiles; el equipo decide si se divide y conserva IDs según su proceso.
- **Confianza:** Alta por la variedad explícita de outcomes.
- **Bloqueador:** Por confirmar; solo es bloqueador de Ready si el equipo no puede estimar/aceptar independientemente el alcance actual.

#### F08 — Dependencias de servicios siguen como supuestos sin decisión de entorno

- **Categoría:** dependencias y supuestos.
- **Fuente:** EP-002 US-006 presupone almacenamiento de objetos/CDN simulado; US-007 exige Redis, HTTP/2 y compresión; EP-004 US-011 presupone SMTP simulado o una pasarela; EP-005 US-017 presupone certificado TLS local/desarrollo.
- **Observación:** las fuentes describen candidatos y entornos, pero no evidencian su aprobación, contrato de disponibilidad ni alternativa cuando no estén disponibles.
- **Impacto:** podrían surgir trabajo de infraestructura y condiciones de aceptación adicionales.
- **Acción sugerida:** confirmar cuáles son restricciones de producto y cuáles solo opciones de implementación; documentar contratos/fallbacks antes de comprometerlos.
- **Confianza:** Media, ya que se expresan como supuestos en las historias.
- **Bloqueador:** No confirmado; mantener las dependencias como **UNCONFIRMED**.

#### F09 — La búsqueda por fecha está en la historia, pero no en los criterios

- **Categoría:** cobertura y aceptación.
- **Fuente:** `specs/EP-002-catalogo-y-busqueda/spec.md`, US-006 Historia: “buscar festivales por nombre, fecha o artista”; AC-02 solo filtra por “nombre de festival o artista”.
- **Observación:** falta resultado verificable para buscar por fecha, aunque es parte expresa del resultado solicitado.
- **Impacto:** una implementación que no permita búsqueda por fecha podría satisfacer todos los AC actuales y aun así incumplir la historia.
- **Acción sugerida:** añadir criterio observable y límites para la búsqueda por fecha o retirar esa dimensión de la historia mediante decisión del equipo.
- **Confianza:** Alta: diferencia directa entre historia y AC.
- **Bloqueador:** Sí, para el alcance declarado de US-006.

#### F10 — No está definido el evento exacto que dispara una única alerta de stock

- **Categoría:** regla de negocio y casos límite.
- **Fuente:** `specs/EP-004-servicios-proveedores/spec.md`, US-011 AC-02/04 y regla: alerta cuando una venta deja stock igual o inferior al umbral; una vez por evento hasta reposición; el ejemplo describe bajar de 11 a 9 con umbral 10; el caso de stock 0 menciona alertas simultáneas de “Stock Bajo” y “Producto Agotado”.
- **Observación:** no se define si una alerta se genera únicamente al cruzar de encima a debajo/igual del umbral, cómo se rearma al reponer stock aún dentro del umbral, ni si “Producto Agotado” es otra notificación o solo otro indicador. “Una vez por evento” no identifica inequívocamente el evento.
- **Impacto:** ventas sucesivas, reposiciones parciales o concurrencia pueden producir alertas duplicadas, omitidas o con etiquetas inconsistentes.
- **Acción sugerida:** decidir transición de stock y rearme, identidad/deduplicación del evento, y comportamiento al llegar a cero; expresar escenarios de venta, reposición y reintento.
- **Confianza:** Alta: los términos citados permiten más de una interpretación.
- **Bloqueador:** Sí, para el comportamiento automático de alertas.

#### F11 — El DoR requiere justificación MoSCoW que no aparece en las historias

- **Categoría:** DoR, prioridad y planificación.
- **Fuente:** DoR, §2.C: “Prioridad MoSCoW: Tiene asignada una prioridad (Must, Should, Could) acompañada de su correspondiente justificación de negocio.” En cada una de las siete historias hay un campo Prioridad, pero no un campo o explicación explícita que justifique esa clasificación.
- **Observación:** el hecho de que cada historia tenga necesidad/objetivo no explica por qué su prioridad relativa es Must o Should frente a otras necesidades.
- **Impacto:** no se cumple un criterio obligatorio de Ready y no queda trazabilidad de la decisión de priorización.
- **Acción sugerida:** registrar la justificación de negocio acordada para cada prioridad, sin que este informe proponga ni cambie prioridades.
- **Confianza:** Alta: comparación directa entre DoR y campos de las historias.
- **Bloqueador:** Sí para Ready de las siete historias mientras no se documente.

#### F12 — La máquina de estados no enumera las transiciones desde Pausado

- **Categoría:** reglas y autorización.
- **Fuente:** `specs/EP-003-gestion-eventos-entradas/spec.md`, US-008 AC-03: “Borrador” -> “Publicado” -> “Pausado”; permite solo al propietario/administrador modificar estado/contenido y prohíbe Published -> Borrador cuando ya hay ventas.
- **Observación:** el recorrido enumera transición a Pausado, pero no declara si puede reanudarse a Publicado, quién puede hacerlo ni qué comportamiento se espera en transiciones no enumeradas.
- **Impacto:** podría haber comportamientos diferentes al intentar reactivar un evento.
- **Acción sugerida:** enumerar transiciones permitidas/prohibidas que sean parte del alcance y su resultado observable.
- **Confianza:** Alta: el AC presenta una máquina de estados parcial.
- **Bloqueador:** No de forma aislada; bloquea la interpretación de reanudación si esta se requiere.

## 6. DoR matrix

Estados usados: **MET**, **NOT_MET**, **NOT_ASSESSABLE**, **NOT_APPLICABLE**. La tabla evalúa evidencia documental. **MET** para estimación/prioridad/iteración significa que el campo aparece, no que se haya comprobado un acuerdo humano.

### 6.1 Clave de criterios DoR

- **A1:** ID único US-XXX en épica.
- **A2:** formato Como/Quiero/Para.
- **A3:** necesidad y objetivo.
- **B1:** al menos dos AC numerados y verificables.
- **B2:** reglas aplicables y al menos un caso límite/error.
- **B3:** suficientemente completa y sin ambigüedades que requieran aclaración.
- **C1:** prioridad MoSCoW con justificación de negocio.
- **C2:** estimación en horas-persona.
- **C3:** nivel de incertidumbre.
- **C4:** predecesores obligatorios identificados y completados o planificados en la misma iteración.
- **C5:** iteración objetivo asignada.
- **D1:** RNF/restricciones técnicas aplicables especificadas.
- **D2:** supuestos técnicos/infraestructura listados.
- **E1:** límite WIP de dos tareas simultáneas por miembro no excedido.
- **E2:** aprobación explícita del PO.

### 6.2 Matriz de estados

| Historia | A1/A2/A3 | B1/B2/B3 | C1/C2/C3/C4/C5 | D1/D2 | E1/E2 | Evidencia breve |
|---|---|---|---|---|---|---|
| US-001 | MET/MET/MET | MET/MET/MET | NOT_MET/MET/MET/NOT_APPLICABLE/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | ID y formato presentes; 5 AC, validación/error y límites; prioridad Must sin justificación explícita (F11); h-p/uncertidumbre/IT-001 indicados. |
| US-003 | MET/MET/MET | MET/MET/NOT_MET | NOT_MET/MET/MET/NOT_ASSESSABLE/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | 4 AC y caso de correo duplicado; resultado tras verificación de correo no está completo (F02); US-001 predecesora, pero estado no acreditado. Prioridad Should sin justificación (F11). |
| US-006 | MET/MET/MET | MET/MET/NOT_MET | NOT_MET/MET/MET/NOT_APPLICABLE/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | 4 AC y estado vacío/404; la fecha de la historia no está en AC (F09), y el método p95 requiere precisión (F03). Prioridad Must sin justificación (F11). |
| US-007 | MET/MET/MET | MET/MET/NOT_MET | NOT_MET/MET/MET/NOT_ASSESSABLE/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | 3 AC y fallback de caché; quedan condiciones reproducibles de medición (F03). US-006 predecesora, no hay estado de finalización. Prioridad Should sin justificación (F11). |
| US-008 | MET/MET/MET | MET/MET/NOT_MET | NOT_MET/MET/MET/NOT_ASSESSABLE/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | 5 AC, errores de fechas/capacidad y restricciones; US-002 no localizado (F05), estados incompletos (F12). Prioridad Must sin justificación (F11). |
| US-011 | MET/MET/MET | MET/MET/NOT_MET | NOT_MET/MET/MET/NOT_ASSESSABLE/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | 4 AC, error de umbral y reintentos; US-010 no localizado y semántica de alerta ambigua (F05/F10). Prioridad Must sin justificación (F11). |
| US-017 | MET/MET/MET | MET/MET/NOT_MET | NOT_MET/MET/MET/NOT_ASSESSABLE/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | 4 AC y restricciones de hashing/cifrado; falta concretar datos cifrados (F04). US-001 predecesora, estado no acreditado. Prioridad Should sin justificación (F11). |

### 6.3 Evidencia y criterios no evaluables

- **A1–A3:** todos MET; las siete historias contienen ID, estructura Como/Quiero/Para, necesidad y objetivo.
- **B1–B2:** todos MET en cuanto a presencia: cada historia tiene al menos dos AC numerados y al menos un ejemplo/caso límite o error. Ello no significa que se cubran todos los flujos.
- **B3:** NOT_MET donde persisten ambigüedades con impacto en los resultados; referencias detalladas en F02–F04, F09, F10 y F12.
- **C1:** NOT_MET en las siete historias por ausencia de justificación de negocio, conforme al texto literal del DoR (F11).
- **C2/C3/C5:** MET por presencia de estimación, incertidumbre e iteración en cada historia. No se verificó si las estimaciones fueron acordadas ni la validez de la estimación.
- **C4:** NOT_APPLICABLE para US-001 y US-006, que declaran no tener predecesores. NOT_ASSESSABLE para US-003/US-007/US-017 (predecesor declarado, estado no aportado) y US-008/US-011 (predecesor no localizado; F05). El DoR exige predecesores completados o planificados en la misma iteración; no hay evidencia de ello.
- **D1/D2:** MET por presencia de RNF/restricciones y supuestos en las siete historias. Las lagunas de precisión/alcance se registran en findings; no equivalen a ausencia total de esos campos.
- **E1/E2:** NOT_ASSESSABLE para todas. No se proporcionó estado WIP ni aprobación explícita del PO.
- **DoD:** no se declara cumplido. No se inspeccionó implementación, PR, pruebas ni evidencias de integración.

## 7. Candidate omissions, stakeholder questions y OUT_OF_SCOPE

Estas cuestiones no son defectos confirmados salvo cuando se vinculan expresamente a F09–F10.

### Candidatos de omisión

- **IN_SCOPE_CANDIDATE — Reserva simulada y resultado para comprador:** G-01/S-01 establecen selección y confirmación simulada; la misión menciona resultado tangible/entrada digital. No se localizó una historia de reserva en los cinco specs revisados. **Pregunta:** ¿qué historia cubre disponibilidad, reserva, confirmación y eventual entrada ficticia?
- **SCOPE_UNCLEAR — Proveedores/EP-004:** US-011 define alertas de stock y el rol Proveedor, pero la misión identifica como usuarios principales a asistente y promotor/organizador, y G-01–G-03 no menciona inventario de proveedores. **Pregunta:** ¿EP-004 pertenece al alcance de este incremento y qué objetivo apoya?
- **SCOPE_UNCLEAR — Recintos:** S-02 incluye creación de evento y aforo; US-008 presupone recinto registrado/aprobado. **Pregunta:** ¿registro/aprobación de recintos es una dependencia preparada o parte del alcance?
- **IN_SCOPE_CANDIDATE — Roles:** EP-001 se titula autenticación y roles; las historias nombran Cliente, Organizador, Proveedor y Administrador, pero no se encontró una historia que defina alta/asignación de esos roles. **Pregunta:** ¿dónde se especifica ese ciclo y qué autoridad asigna cada rol?
- **IN_SCOPE_CANDIDATE — Manejo de errores operativos:** los objetivos declaran fiabilidad, pero no todos los errores de persistencia, almacenamiento, SMTP, caché o certificado tienen comportamiento observable. **Pregunta:** ¿cuáles son esenciales para este incremento?
- **SCOPE_UNCLEAR — Datos ficticios en perfiles:** goals prohíbe datos personales/de contacto reales; US-001/US-003 manejan email y perfil. **Pregunta:** ¿qué datos ficticios y escenarios se permiten en demo/pruebas, y cómo se asegura su carácter no real?

### OUT_OF_SCOPE y exclusiones expresas

- **OUT_OF_SCOPE — Pagos bancarios reales y datos bancarios reales:** EX-01 y las restricciones de goals los excluyen; US-017 AC-03 también expresa exclusión. No se sugiere reintroducirlos.
- **OUT_OF_SCOPE — Factura fiscal real y reventa/asignación gráfica de butacas:** EX-02/EX-03, salvo que una fuente autorizada posterior cambie el alcance.
- **OUT_OF_SCOPE — Datos personales, bancarios o de contacto reales:** prohibidos por goals; cualquier prueba de perfil debe respetar esa frontera.

## 8. Dependencies, assumptions y traceability gaps

| Elemento | Tipo/estado | Evidencia y riesgo |
|---|---|---|
| US-002 → US-008 | Predecesor **UNCONFIRMED** | US-008 lo declara; no aparece en los cinco specs leídos. No se puede evaluar estado ni contrato (F05). |
| US-010 → US-011 | Predecesor **UNCONFIRMED** | US-011 lo declara; US-010 no aparece en los cinco specs leídos. No se puede evaluar estado ni contrato (F05). |
| US-001 → US-003, US-017 | Predecesores explícitos | Iteraciones planificadas IT-001, IT-004 e IT-005; no hay evidencia de finalización de US-001. |
| US-006 → US-007 | Predecesor explícito | Plan inicial IT-002 antes de IT-006; no hay evidencia de finalización. |
| Recinto registrado/aprobado → US-008 | Prerrequisito supuesto | US-008 lo declara; no se localizó historia/contrato de aprobación en fuentes revisadas. |
| Redis, almacenamiento de objetos/CDN, SMTP y TLS | Dependencias externas **UNCONFIRMED** | Aparecen como servicios/infraestructura supuestos o requeridos; proveedor, entorno y fallback no se documentan de forma uniforme (F08). |
| G-01/G-02/G-03 → historias | Brecha de trazabilidad | No hay enlace explícito por historia a objetivo/métrica; EP-004 carece de objetivo de alcance inequívoco. |
| Catálogo → selección/reserva | Contrato de negocio **UNCONFIRMED** | US-006 ofrece botón de selección; no se encontró flujo de reserva en los cinco specs revisados. |
| Datos de perfil → regla de datos ficticios | Restricción compartida | goals prohíbe datos reales; US-001/US-003 incluyen correo y datos de perfil. Debe asegurarse que los escenarios de prueba sigan siendo ficticios. |

No se detecta un ciclo explícito entre dependencias visibles. La falta de US-002/US-010 impide descartar dependencias/ciclos fuera del alcance leído.

## 9. Questions for humans (prioridad)

1. **P0:** ¿Se añade a US-006 la búsqueda por fecha con comportamiento verificable, o se retira de la historia? (F09)
2. **P0:** ¿Cuál es la transición exacta que genera la alerta de US-011, cómo se rearma tras reposición y cómo se diferencia “Stock Bajo” de “Producto Agotado”? (F10)
3. **P0:** ¿Qué campos ficticios cubre el cifrado AES-256 de US-017, y qué evidencia demuestra cobertura sin usar datos reales? (F04)
4. **P0:** ¿Dónde están las especificaciones autorizadas de US-002 y US-010? ¿Son prerrequisitos obligatorios de US-008/US-011 o deben corregirse esos IDs? (F05)
5. **P0:** ¿Cuál es la justificación de negocio acordada de cada prioridad Must/Should para satisfacer el DoR sin cambiar ahora las prioridades? (F11)
6. **P1:** ¿Qué resultado confirma el cambio de correo en US-003 y qué transiciones desde Pausado admite US-008? (F02/F12)
7. **P1:** ¿Qué navegador/dataset/instrumentación se utilizarán para medir el p95 de filtrado en cliente y LCP? (F03)
8. **P1:** ¿Se incluye EP-004/proveedor en el alcance actual y qué objetivo G-01–G-03 cubre?
9. **P1:** ¿Qué historia cubre el flujo completo de reserva simulada y resultado para el comprador?
10. **P2:** ¿Qué estados de WIP y aprobación del PO se usarán como evidencia de E1/E2 del DoR?
11. **P2:** ¿Redis, SMTP, almacenamiento de objetos/CDN y certificados TLS están aprobados como dependencias o son opciones de implementación?
12. **P2:** ¿Se acepta el tamaño actual de US-006, US-007, US-008 y US-017 para estimación/aceptación independiente, o el equipo prefiere cortes verticales?

## 10. RECHECK crosswalk

No se proporcionó decisión log. Por ello, el estado se determina exclusivamente comparando los hallazgos v01 con el texto actual; no se infiere aceptación/rechazo humano. Se conserva cada referencia anterior:

| Hallazgo v01 | Estado RECHECK | Evidencia actual y relación con decisiones |
|---|---|---|
| F01 — Logout/revocación JWT | **RESOLVED** | US-001 AC-04 ahora exige revocación server-side en blacklist y AC-05 rechaza tokens revocados/expirados con 401. La evidencia textual resuelve la ambigüedad del informe anterior; no se recibió decisión humana ni se verifica implementación. |
| F02 — Perfil y publicación incompletos | **PARTIALLY_RESOLVED** | US-003 ahora exige contraseña y verificación por correo (AC-03/04), y US-008 define propietario/administrador, estados y regla de no revertir tras ventas. Persisten el resultado final del cambio de correo y las transiciones desde Pausado (F02/F12). |
| F03 — Rendimiento no reproducible | **PARTIALLY_RESOLVED** | US-006 fija 500 eventos y p95; US-007 fija Fast 4G/LCP, Lighthouse, peso y Redis/TTL. El método de filtrado cliente y condiciones de medición aún no quedan plenamente reproducibles (F03). |
| F04 — Seguridad/datos de pago no acotados | **PARTIALLY_RESOLVED** | US-017 explicita datos simulados, exclusión de pagos reales/PCI-DSS y Bcrypt/AES-256; sigue sin enumerar datos cubiertos por AES-256 en reposo (F04). |
| F05 — Predecesores no localizados | **PARTIALLY_RESOLVED** | US-011, antes no localizada en el contexto citado por v01, ahora tiene spec; sin embargo US-008 sigue citando US-002 no localizada y US-011 cita US-010 no localizada (F05). |
| F06 — Límites y errores incompletos | **PARTIALLY_RESOLVED** | US-006 añade estado vacío/404; US-008 define errores de fechas y aforo; US-011 define umbral inválido y reintentos. Persisten vacíos de búsqueda por fecha y semántica de alerta/rearme (F06, F09, F10). |
| F07 — Historias grandes | **OPEN** | Las historias actuales siguen agrupando outcomes diferenciables (F07); no hay decisión humana ni evidencia de división/aceptación independiente. |
| F08 — Integraciones externas no confirmadas | **OPEN** | Los supuestos de Redis, SMTP, almacenamiento/CDN y TLS siguen presentes sin decisión de entorno/proveedor o contrato uniforme (F08). Permanecen **UNCONFIRMED**, no se declaran bloqueadores confirmados. |

## 11. Explicit closure

This is an advisory review. No source requirement, priority, estimate, plan or human decision was changed. No baseline or gate was approved.
