# Requirements review v01

## 1. Run metadata

- **Proyecto:** SubsonicFestival / Web Solutions SL.
- **Modo:** INITIAL. La invocación no suministró un identificador de commit ni una
  versión de baseline; por tanto, el baseline es **no indicado**.
- **Snapshot:** estado del repositorio disponible durante esta revisión. Fecha/hora
  proporcionada por la invocación: 2026-10-07 10:14:27 +02:00.
- **Agente:** `.github/agents/requirements-reviewer.agent.md`, versión no indicada.
- **Modelo/herramientas:** no indicado; revisión documental mediante lectura de
  archivos y creación de este informe.
- **Alcance:** todos los requisitos e historias encontrados en
  `specs/product/` y sus cinco especificaciones de épica relacionadas en `specs/`.
  Historias inspeccionadas: US-001, US-003, US-006, US-008, US-009, US-012 y
  US-018. Se revisaron también misión, objetivos, DoR y DoD.
- **Idioma:** español.

## 2. Source manifest y limitaciones

### Archivos leídos

| Archivo | Papel | Secciones/IDs relevantes |
|---|---|---|
| `.github/agents/requirements-reviewer.agent.md` | Protocolo de revisión | Secciones 1–7 |
| `specs/product/mission.md` | Misión, problema, usuarios y propuesta de valor | Usuarios Asistente y Promotor/Organizador; misión |
| `specs/product/goals.md` | Objetivos, alcance, exclusiones y restricciones | G-01–G-03, M-01–M-03, S-01–S-03, EX-01–EX-03 |
| `docs/quality/definition-of-ready.md` | DoR compartido | Checklist A–E |
| `docs/quality/definition-of-done.md` | DoD compartido | Seguridad, rendimiento y pruebas; sin evidencia de implementación |
| `specs/EP-001-autenticacion-y-roles/spec.md` | Especificación EP-001 | US-001, US-003 |
| `specs/EP-002-catalogo-y-busqueda/spec.md` | Especificación EP-002 | US-006, US-008 |
| `specs/EP-003-gestion-eventos-entradas/spec.md` | Especificación EP-003 | US-009 |
| `specs/EP-004-servicios-proveedores/spec.md` | Especificación EP-004 | US-012 |
| `specs/EP-005-administracion-y-seguridad/spec.md` | Especificación EP-005 | US-018 |

### Fuentes inaccesibles o no encontradas en el alcance revisado

- No se encontró un archivo de constitución/gobernanza ni un Team Charter accesible
  en las fuentes suministradas. Por ello, los controles sobre WIP y autoridad del
  equipo quedan **NOT_ASSESSABLE**.
- No se encontró un directorio de informes previamente configurado. Se utilizó
  `docs/quality/` como ubicación de calidad existente del repositorio; esto es una
  decisión operativa por ausencia de `REPORT_DIRECTORY`, no una nueva política.
- No se proporcionaron commit, baseline, decisión log ni informe previo; no aplica
  crosswalk de RECHECK.
- No se revisó implementación, datos, pruebas, GitHub ni servicios externos. En
  consecuencia, no se afirma cumplimiento del DoD.
- En `specs/product/` solo se encontraron `mission.md` y `goals.md`; las historias
  se encontraron en las cinco rutas `specs/EP-XXX-*/spec.md` indicadas arriba.
  La inspección de ausencia se limita a esas fuentes y no significa que los IDs no
  existan fuera de ellas.

## 3. Scoped assessment

**Recomendación: NEEDS_REFINEMENT.**

El alcance detallado revisado no está listo como conjunto completo de requisitos:
hay criterios contradictorios o no verificables, historias que agrupan varios
resultados verticales, predecesores no localizados y faltan decisiones sobre
alcance. Los bloqueadores principales son:

1. US-001 define logout como invalidación del token en cliente, mientras que la
   seguridad esperada para una sesión JWT requiere aclarar si existe revocación en
   servidor; el resultado observable no queda compartido.
2. US-006 y US-008 imponen servicios, cifras y condiciones de rendimiento sin
   método de medición suficientemente definido; además, US-008 agrupa optimización,
   caché, fallback y carga.
3. US-009 depende de US-002, pero US-002 no está en las especificaciones revisadas;
   US-012 depende de US-011, también no localizado. Esto impide comprobar
   predecesores y trazabilidad.
4. US-003, US-009 y US-018 contienen acciones o restricciones cuyo alcance,
   estados de error y reglas de autorización no se pueden probar completamente.
5. El DoR exige aprobación del PO, límite WIP y predecesores completados o
   planificados; no existe evidencia de esas decisiones en las fuentes leídas.

La recomendación afecta a US-001, US-003, US-006, US-008, US-009, US-012 y US-018,
no constituye aprobación de baseline ni de una puerta de calidad.

## 4. Coverage matrix

| Dimensión | IDs inspeccionados | Resultado | Hallazgos |
|---|---|---|---|
| Claridad y consistencia | US-001, 003, 006, 008, 009, 012, 018 | Requiere refinamiento | F01, F02, F03, F04 |
| Cobertura y alineación de alcance | EP-001–EP-005; G-01–G-03; S-01–S-03; EX-01–EX-03 | Parcial; decisiones pendientes | F05 |
| Elementos de especificación | Todas las US | Insuficiente en errores, límites, seguridad y medición | F02, F03, F04, F06 |
| Tamaño/granularidad (INVEST) | US-006, US-008, US-009, US-018 | Varias historias grandes o acopladas | F07 |
| Aceptación y DoR | Todas las US; DoR A–E | DoR no demostrable; AC incompletos en varias historias | F01, F02, F03, F04, F06 |
| Dependencias y supuestos | Predecessors y supuestos de todas las US | Trazabilidad incompleta; dependencias no confirmadas | F05, F08 |

## 5. Findings

### 5.1 Índice

| ID | Severidad | Categoría | Historias | Confianza | ¿Bloqueador? |
|---|---|---|---|---|---|
| F01 | MAJOR | Claridad/seguridad de sesión | US-001 | Alta | Sí |
| F02 | MAJOR | Aceptación incompleta y contradicción de alcance | US-003, US-009 | Alta | Sí |
| F03 | MAJOR | Verificabilidad de rendimiento/infraestructura | US-006, US-008 | Alta | Sí |
| F04 | MAJOR | Seguridad y restricciones no acotadas | US-018 | Alta | Sí |
| F05 | MAJOR | Dependencias y trazabilidad | US-009, US-012 | Alta | Sí |
| F06 | MINOR | Reglas y límites incompletos | US-006, US-009, US-012 | Media | No |
| F07 | MAJOR | Historia demasiado grande | US-006, US-008, US-009, US-018 | Alta | Sí |
| F08 | QUESTION | Integración externa/alcance no confirmado | US-006, US-012, US-018 | Media | No, hasta decisión |

### 5.2 Registros de evidencia

#### F01 — Logout y revocación JWT no tienen el mismo significado

- **Categoría:** claridad, seguridad, aceptación.
- **Fuente:** `specs/EP-001-autenticacion-y-roles/spec.md`, US-001,
  AC-02/AC-04: “emite un token JWT con tiempo de expiración de 24 horas” y
  “logout que invalida la sesión/token en el cliente”.
- **Observación:** “invalidar en el cliente” no define qué ocurre si se reutiliza
  un token antes de su expiración, ni distingue eliminación local de revocación
  del lado servidor.
- **Impacto:** dos implementaciones pueden producir resultados distintos y una
  sesión aparentemente cerrada puede seguir autorizando peticiones.
- **Acción sugerida:** decidir y especificar el modelo de logout (solo eliminación
  local o revocación server-side), la respuesta a token expirado/revocado y el
  comportamiento de múltiples sesiones. Añadir escenarios positivos y negativos.
- **Confianza:** Alta, porque la diferencia está expresamente en AC-02/AC-04.
- **Bloqueador:** Sí; impide una interpretación de seguridad compartida.

#### F02 — Edición de perfil y publicación no cubren todos los resultados

- **Categoría:** aceptación, reglas de negocio.
- **Fuente:** US-003 AC-02/AC-03: permite editar nombre/teléfono/dirección, pero
  menciona cambio de correo sin criterio de guardado exitoso. US-009 AC-03/AC-04:
  define estados y capacidad, pero no autorización operativa ni transiciones
  inválidas.
- **Observación:** US-003 no establece validación de teléfono/dirección, error de
  contraseña actual incorrecta, confirmación de cambio de correo ni qué ocurre al
  editar correo. US-009 no define quién puede publicar/pausar, si un evento
  publicado puede volver a borrador, ni qué sucede con fechas inválidas o aforo
  cero.
- **Impacto:** no se puede verificar el flujo completo ni evitar reglas
  contradictorias entre UI y API.
- **Acción sugerida:** añadir AC numerados para éxito, rechazo y estado vacío de
  cada campo/transición; definir autorización y máquina de estados.
- **Confianza:** Alta, por ausencia dentro de los AC y por las reglas declaradas.
- **Bloqueador:** Sí para considerar esas historias Ready.

#### F03 — Rendimiento y plataforma no son reproducibles

- **Categoría:** verificabilidad, restricciones, dependencias.
- **Fuente:** US-006 RNF “< 100 ms ... hasta 500 eventos”; US-008 AC-01
  “LCP inferior a 2,0 segundos en conexiones 4G estándar”, AC-03 Redis TTL 5
  minutos y ejemplo “100 usuarios simultáneos ... menos de 300 ms”.
- **Observación:** no se define dispositivo/navegador, dataset, percentil,
  ubicación, herramienta o número de mediciones. “4G estándar”, “carga” y
  “condiciones normales” son ambiguos. La invalidación inmediata de caché y TTL
  de 5 minutos necesitan una regla explícita cuando se modifica el contenido.
- **Impacto:** resultados no comparables y posible conflicto entre caché,
  consistencia e invalidación.
- **Acción sugerida:** acordar método de medición, entorno, métrica/percentil y
  dataset; separar el requisito observable de la solución Redis; especificar
  hit/miss, fallo de caché e invalidación.
- **Confianza:** Alta, porque los términos de medición no están definidos.
- **Bloqueador:** Sí para verificar los RNF y para el DoR de restricciones técnicas.

#### F04 — US-018 mezcla cumplimiento, cifrado, datos de pago y supuestos no acotados

- **Categoría:** seguridad, alcance, verificabilidad.
- **Fuente:** US-018: AC-01 TLS 1.3, AC-03 AES-256, regla RGPD,
  restricción de CVC/CVV2 y story “contraseñas, datos de pago, tokens”.
- **Observación:** la misión/objetivos solo declaran datos ficticios y excluyen
  pagos reales, mientras US-018 especifica datos de pago y PCI-DSS. No se define
  qué campos son “altamente sensibles”, gestión de claves, rotación, copias,
  logs fuera del servidor, ni cómo se verifica “RGPD”. Además, “encriptación” no
  distingue hash de contraseña de cifrado reversible.
- **Impacto:** riesgo de implementar una integración o tratamiento fuera de
  alcance y criterios que no tienen prueba observable.
- **Acción sugerida:** confirmar si US-018 cubre solo datos ficticios y la
  superficie de la aplicación; separar hashing, cifrado, transporte y
  enmascaramiento; definir inventario de campos, ubicación de claves y evidencias
  de verificación. No asumir obligaciones legales adicionales sin decisión humana.
- **Confianza:** Alta para la tensión de alcance; Media para el detalle legal.
- **Bloqueador:** Sí hasta resolver el alcance y hacer verificables los controles.

#### F05 — Predecesores referencian historias no localizadas

- **Categoría:** dependencia y trazabilidad.
- **Fuente:** US-009 `Predecessors: US-002`; US-012 `Predecessors: US-011`.
  En las cinco especificaciones leídas no se encontraron esos IDs.
- **Observación:** no puede determinarse si son historias omitidas, renombradas o
  dependencias externas. US-009 requiere un organizador/recinto, y US-012 requiere
  stock, correo y proveedor, pero esas capacidades no están descritas en las
  fuentes revisadas.
- **Impacto:** no se puede comprobar “predecesor completado o planificado en la
  misma iteración”, ni el contrato de datos necesario.
- **Acción sugerida:** localizar y añadir las especificaciones autorizadas o
  corregir los IDs; clasificar cada relación como prerrequisito, contrato
  compartido o preferencia de secuencia, y definir interfaces/datos mínimos.
- **Confianza:** Alta dentro del alcance leído; la ausencia no se afirma fuera de
  esas rutas.
- **Bloqueador:** Sí para US-009 y US-012.

#### F06 — Límites y errores de dominio no están completos

- **Categoría:** reglas, casos límite.
- **Fuente:** US-006 solo ejemplifica búsqueda “Rock”; US-009 fija precio
  `0.00–5.000.00 €`; US-012 define umbral y alerta.
- **Observación:** faltan búsquedas vacías, mayúsculas/acentos, fecha pasada,
  paginación y fallo de imagen/mapa en US-006; moneda/formato, aforo cero,
  fechas invertidas, duplicidad de tipos y concurrencia en US-009; umbral cero,
  reposición simultánea, duplicados y fallo permanente de correo en US-012.
  “Campo ejecutable” en US-012 no es un comportamiento observable claro.
- **Impacto:** validaciones y mensajes pueden divergir; la sobreventa o alertas
  duplicadas no quedan demostrablemente cubiertas.
- **Acción sugerida:** priorizar límites de negocio relevantes y añadir AC de
  rechazo, estado vacío, reintentos agotados y concurrencia.
- **Confianza:** Media; la necesidad concreta depende de decisiones de producto.
- **Bloqueador:** No por sí solo, salvo los casos que el PO declare esenciales.

#### F07 — Varias historias agrupan resultados verticales independientes

- **Categoría:** tamaño/granularidad INVEST.
- **Fuente:** US-006 reúne catálogo, búsqueda y detalle; US-008 reúne LCP,
  lazy-loading, Redis, invalidación y fallback; US-009 reúne wizard, entradas,
  estados y aforo; US-018 reúne transporte, logs, cifrado y APIs.
- **Observación:** cada grupo contiene resultados que podrían inspeccionarse y
  fallar independientemente. Las estimaciones de una sola historia (14, 16, 18
  y 12 h-p) no demuestran que el conjunto sea estimable como una sola unidad.
- **Impacto:** dificulta planificación, aceptación parcial y localización de
  dependencias; puede ocultar trabajo necesario.
- **Acción sugerida:** considerar cortes verticales independientes, por ejemplo
  descubrimiento/detalle, optimización/caché, configuración/publicación y
  controles de datos. La división final corresponde al equipo y no se decide en
  este informe.
- **Confianza:** Alta por el número de outcomes explícitos.
- **Bloqueador:** Sí para Ready si no puede estimarse/aceptarse de forma
  independiente; confirmar con el equipo.

#### F08 — Integraciones externas son hipótesis no confirmadas

- **Categoría:** dependencias/supuestos.
- **Fuente:** US-006 supone CDN/Cloud Storage; US-008 Redis, HTTP/2 y compresión;
  US-012 SMTP/SendGrid/Mailgun/AWS SES; US-018 certificado TLS de producción.
- **Observación:** son soluciones o servicios concretos, pero no hay decisión de
  proveedor, disponibilidad, credenciales de entorno, coste, fallback operativo
  ni contrato de error en las fuentes revisadas.
- **Impacto:** puede aparecer trabajo de infraestructura no estimado o una
  dependencia incompatible con la restricción de tecnologías acordadas.
- **Acción sugerida:** confirmar cada integración como requisito, restricción o
  simple candidato; documentar contrato, entorno y responsable antes de
  comprometerla.
- **Confianza:** Media, porque los textos lo expresan como supuesto.
- **Bloqueador:** No confirmado; se vuelve bloqueador si la historia depende de él
  para aceptación.

## 6. DoR matrix

**Clave de criterios reales del DoR:** A1 ID único; A2 formato Como/Quiero/Para;
A3 necesidad/objetivo; B1 ≥2 AC numerados; B2 regla y edge/error; B3 sin
ambigüedad; C1 prioridad + justificación; C2 estimación h-p; C3 incertidumbre;
C4 predecesores; C5 iteración; D1 RNF/restricciones; D2 supuestos; E1 WIP ≤2;
E2 validación explícita del PO. Estados: **MET**, **NOT_MET**,
**NOT_ASSESSABLE**, **NOT_APPLICABLE**.

| Historia | A1/A2/A3 | B1/B2/B3 | C1/C2/C3/C4/C5 | D1/D2 | E1/E2 | Evidencia/resumen |
|---|---|---|---|---|---|---|
| US-001 | MET/MET/MET | MET/MET/NOT_MET | MET/MET/MET/MET/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | Tiene ID, formato, 4 AC, reglas y casos límite, pero logout/JWT deja ambigüedad (F01). |
| US-003 | MET/MET/MET | MET/MET/NOT_MET | MET/MET/MET/MET/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | Tres AC y caso límite; falta resultado y validación del cambio de correo (F02). |
| US-006 | MET/MET/MET | MET/MET/NOT_MET | MET/MET/MET/NOT_APPLICABLE/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | Cuatro AC y caso 404; medición y cobertura de búsqueda requieren aclaración (F03/F06). |
| US-008 | MET/MET/MET | MET/MET/NOT_MET | MET/MET/MET/MET/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | Tres AC y fallback; criterios de entorno/medición no son reproducibles (F03). |
| US-009 | MET/MET/MET | MET/MET/NOT_MET | MET/MET/MET/NOT_ASSESSABLE/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | Cuatro AC y caso sin entradas; US-002 no localizado y faltan transiciones (F02/F05). |
| US-012 | MET/MET/MET | MET/MET/NOT_MET | MET/MET/MET/NOT_ASSESSABLE/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | Tres AC y agotamiento; US-011 no localizado y “campo ejecutable” es ambiguo (F05/F06). |
| US-018 | MET/MET/MET | MET/MET/NOT_MET | MET/MET/MET/MET/MET | MET/MET | NOT_ASSESSABLE/NOT_ASSESSABLE | Cuatro AC y caso HTTP; alcance RGPD/pago/cifrado debe decidirse y acotarse (F04). |

**Criterios deferred/no demostrables:** E1 y E2 se mantienen
**NOT_ASSESSABLE** para todas las historias porque no hay Team Charter, registro
de WIP ni aprobación del PO en las fuentes leídas. C4 es
**NOT_ASSESSABLE** donde el predecesor no fue localizado; no se ha supuesto que
esté completado. Las estimaciones y prioridades se registran como MET solo porque
cada historia contiene esos campos, no porque se haya verificado su acuerdo o
corrección.

## 7. Candidate omissions, stakeholder questions y OUT_OF_SCOPE

### Candidatos de omisión (no son defectos confirmados)

- **IN_SCOPE_CANDIDATE — Resultado de reserva/entrada digital:** G-01 y S-01
  hablan de confirmación simulada, mientras la misión promete “resultado tangible
  (la entrada digital)”. Pregunta: ¿el alcance exige generar/mostrar una entrada
  ficticia o solo confirmar una reserva?
- **IN_SCOPE_CANDIDATE — Flujo completo del comprador:** G-01 mide completar
  reserva, pero las historias revisadas no describen selección, confirmación,
  cancelación ni capacidad tras una reserva. Pregunta: ¿debe existir una historia
  específica de reserva simulada y control de concurrencia?
- **SCOPE_UNCLEAR — Recintos y aprobación:** S-02 exige crear evento y aforo;
  US-009 supone recinto registrado y aprobado. Pregunta: ¿la gestión/aprobación
  de recintos es parte del producto o una dependencia preparada?
- **SCOPE_UNCLEAR — Proveedores:** el mission declara como usuarios principales
  comprador y promotor, mientras EP-004 añade Proveedor. Pregunta: ¿EP-004 está
  dentro del incremento y qué objetivo G-01–G-03 cubre?
- **SCOPE_UNCLEAR — Roles:** EP-001 se titula roles, pero las historias revisadas
  describen visitante/cliente y US-009 organizador sin historia explícita de
  asignación o autorización de roles. Pregunta: ¿dónde se especifica el alta,
  asignación y revocación de roles?
- **IN_SCOPE_CANDIDATE — Errores operativos:** misión exige experiencia fiable y
  segura; deberían decidirse estados para fallo de persistencia, correo, mapa,
  almacenamiento y caché, sin inventar umbrales.

### Posible fuera de alcance (requiere decisión)

- **OUT_OF_SCOPE candidato — Pagos reales y datos de tarjeta:** EX-01 prohíbe
  pasarelas reales y goals exige datos ficticios; la parte de CVC/CVV2 de US-018
  puede ser innecesaria si no se procesan tarjetas. Pregunta: ¿se elimina esa
  superficie o se mantiene solo como control de no almacenamiento?
- **OUT_OF_SCOPE candidato — EP-004 de inventario de proveedores:** no se enlaza
  explícitamente con S-01–S-03. Pregunta: ¿se difiere el módulo de stock del
  incremento actual?

## 8. Dependencies, assumptions y traceability gaps

| Elemento | Tipo/estado | Evidencia y riesgo |
|---|---|---|
| US-002 → US-009 | Prerrequisito **UNCONFIRMED** | ID citado, no localizado en fuentes revisadas; impide validar Ready. |
| US-011 → US-012 | Prerrequisito **UNCONFIRMED** | Igual; falta contrato de producto, stock y proveedor. |
| US-001 → US-003/US-018 | Prerrequisito explícito | La autenticación se cita; falta evidencia de que esté planificada/completada. |
| Catálogo → reserva | Contrato de negocio **UNCONFIRMED** | US-006 ofrece selección de entradas, pero no existe historia de reserva en el material leído. |
| Recinto aprobado → US-009 | Prerrequisito de datos | Expresamente supuesto, sin historia/ID ni contrato de aprobación. |
| Redis/CDN/SMTP/TLS | Dependencias externas **UNCONFIRMED** | Enumeradas en supuestos; proveedor, entorno y fallback no decididos. |
| G-01/G-02/G-03 → historias | Brecha de trazabilidad | No hay enlaces por historia a objetivo/métrica; EP-004 y US-018 no tienen cobertura de objetivo explícita. |
| EX-01/EX-02/EX-03 → US-018/US-009 | Posible tensión | Datos de pago/“facturación” aparecen en historias pese a exclusiones; requiere autoridad de alcance. |

No se detectó un ciclo explícito en los predecesores declarados. La ausencia de
US-002/US-011 impide descartar ciclos o dependencias adicionales fuera del
material leído.

## 9. Questions for humans (prioridad)

1. **P0:** ¿Qué fuente y decisión controlan el alcance cuando US-018 menciona
   pagos/RGPD y `goals.md` excluye pagos reales y exige datos ficticios?
2. **P0:** ¿Dónde están US-002 y US-011, o deben corregirse/eliminarse esos
   predecesores? ¿Son prerrequisitos obligatorios o contratos compartidos?
3. **P0:** ¿Logout revoca tokens en servidor o solo elimina el token del cliente?
   ¿Qué respuesta observable se exige al reutilizarlo?
4. **P0:** ¿Se incluye la entrada digital y el flujo de reserva simulada completo,
   y qué historia cubre la selección iniciada desde US-006?
5. **P1:** ¿Qué estados y permisos son válidos para publicar, pausar, modificar y
   volver a publicar un evento?
6. **P1:** ¿Qué entorno, dispositivo, dataset, percentil y herramienta validan
   los límites de US-006/US-008?
7. **P1:** ¿EP-004 y el rol Proveedor están en el incremento actual y qué objetivo
   los justifica?
8. **P1:** ¿Se mantienen las historias grandes como están o se prefieren cortes
   verticales separados?
9. **P2:** ¿Qué servicios (Redis, SMTP, CDN/Cloud Storage) están aprobados y qué
   contrato se usa cuando fallan?
10. **P2:** ¿Dónde se registran aprobación del PO, WIP y estado de predecesores
    para poder completar el DoR?

## 10. RECHECK crosswalk

No aplica: revisión **INITIAL**; no se recibió informe previo, decisión log ni
fuentes revisadas posteriores.

## 11. Explicit closure

This is an advisory review. No source requirement, priority, estimate, plan or
human decision was changed. No baseline or gate was approved.
