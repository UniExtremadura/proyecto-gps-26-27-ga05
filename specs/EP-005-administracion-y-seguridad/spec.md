# EP-005 — Administración Global, Seguridad y Analítica

## US-014 — Gestión global de la plataforma por Administrador

- **Necesidad:** Dotar a Web Solutions SL de una herramienta centralizada de gobierno para supervisar usuarios, moderar festivales, gestionar recintos y resolver incidencias operativas.
- **Objetivo:** Construir un panel de administración global accesible exclusivamente para el rol `Admin`.
- **Historia de Usuario:** Como Administrador, quiero supervisar y gestionar usuarios, festivales, entradas y catálogo de productos, para garantizar el correcto funcionamiento de la plataforma.
- **Tipo:** Funcional
- **Prioridad:** Must (Soporte operacional indispensable para resolución de incidencias y moderación de contenidos).
- **Estimación:** 18 h-p
- **Incertidumbre:** Media
- **Predecesores:** US-002
- **Plan inicial:** IT-003 (Sprint 3)
- **Responsable:** Equipo (Justo Cilleros 9 h / Manuel Carvajal 9 h)
- **Tarifa Media / Coste Total:** 30 €/h | 540,00 €

### Criterios de aceptación
- **US-014-AC-01:** Panel `/admin` con vistas de listado y búsqueda para gestionar usuarios (activar/suspender cuentas y cambiar roles), festivales (publicar, pausar o cancelar cualquier evento), recintos y catálogo de merchandising.
- **US-014-AC-02:** Cuando un Administrador suspende una cuenta o pausa un festival por moderación, el cambio se aplica de inmediato e invalida las sesiones activas del usuario suspendido.
- **US-014-AC-03:** Toda acción administrativa de modificación de rol, suspensión de usuario o alteración de estado de un evento queda registrada en una tabla de auditoría (`audit_log`) con fecha, ID del administrador y motivo.

### Verificación y restricciones
- **Reglas de Negocio:** Un administrador no puede eliminar ni quitarse el rol `Admin` a su propia cuenta activa para evitar dejar el sistema sin administración (*lockout*).
- **Restricciones:** Acceso protegido mediante el middleware RBAC de `US-002` exclusivamente para el rol `Admin`.
- **Requisitos No Funcionales (RNF):** Todas las tablas del panel de administración cuentan con paginación y filtrado en servidor.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* El Admin asigna el rol `Organizador` a un usuario registrado y aprueba un nuevo recinto: la acción queda grabada en `audit_log`.
  * *Caso Límite:* Intento de un Administrador de desactivar su propia cuenta: el sistema rechaza la operación con HTTP `400 Bad Request` ("No puedes suspender tu propia cuenta de administrador").
- **Supuestos:** Existe al menos una cuenta `Admin` preconfigurada mediante el *seeder* inicial de la base de datos.

---

## US-015 — Dashboard de estadísticas y métricas globales

- **Necesidad:** Proporcionar a la dirección y administradores de la plataforma una vista consolidada del volumen de reservas, aforos ocupados e ingresos simulados de todos los festivales.
- **Objetivo:** Implementar un cuadro de mando analítico en el panel de administración con indicadores clave (KPIs) globales.
- **Historia de Usuario:** Como Administrador, quiero visualizar un panel con métricas agregadas de ventas e ingresos globales, para la toma de decisiones estratégicas.
- **Tipo:** Funcional
- **Prioridad:** Could (Aporta valor analítico a la dirección, pero la plataforma puede operar inicialmente sin este cuadro de mando).
- **Estimación:** 16 h-p
- **Incertidumbre:** Media
- **Predecesores:** US-014
- **Plan inicial:** IT-006 (Sprint 6)
- **Responsable:** Equipo (Javier García 8 h / Justo Cilleros 8 h)
- **Tarifa Media / Coste Total:** 30 €/h | 480,00 €

### Criterios de aceptación
- **US-015-AC-01:** El dashboard `/admin/analytics` muestra tarjetas resumen con los KPIs globales: total de festivales activos, total de entradas reservadas, porcentaje de ocupación media de aforo, volumen total de ingresos simulados (€) de entradas y de merchandising, y número de usuarios registrados por rol.
- **US-015-AC-02:** Incluye desglose comparativo por festival y permite filtrar las métricas por rango de fechas.
- **US-015-AC-03:** Permite exportar el resumen estadístico visible en formato CSV para su análisis externo.

### Verificación y restricciones
- **Reglas de Negocio:** Las métricas globales agregan únicamente las reservas confirmadas (excluyendo reservas canceladas o eventos en estado `Borrador`).
- **Restricciones:** Acceso exclusivo para usuarios con rol `Admin`. Todos los datos financieros representados son simulados.
- **Requisitos No Funcionales (RNF):** Tiempo de carga de las consultas agregadas del dashboard < 1,0 segundo.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* El Administrador accede al dashboard y visualiza 3 festivales publicados, 1.250 entradas reservadas y un 68% de ocupación media.
  * *Caso Límite:* Filtro por un rango de fechas sin actividad: todos los indicadores numéricos muestran `0` o `0,00 €` sin producir errores de división por cero en el cálculo de porcentajes.
- **Supuestos:** Se alimenta de los datos sintéticos de eventos, entradas y merchandising generados en las épicas `EP-001` a `EP-004`.

---

## US-016 — Protección contra ataques, inyecciones y rate-limiting

- **Necesidad:** Blindar la plataforma frente a abusos automatizados, intentos de fuerza bruta en el login e inyecciones de código malicioso.
- **Objetivo:** Implementar limitación de tasa de peticiones (*rate-limiting*), cabeceras de seguridad HTTP y sanitización/validación estricta contra SQLi y XSS.
- **Historia de Usuario:** Como Administrador, quiero que el sistema incorpore limitación de peticiones (rate-limiting) y sanitización contra inyecciones SQL/XSS, para proteger la infraestructura frente a ciberataques.
- **Tipo:** Seguridad
- **Prioridad:** Must (Requisito no funcional crítico de ciberseguridad para evitar vulneraciones de datos y caídas de servicio).
- **Estimación:** 20 h-p
- **Incertidumbre:** Alta
- **Predecesores:** US-001
- **Plan inicial:** IT-005 (Sprint 5)
- **Responsable:** Equipo (Manuel Carvajal 10 h / Álvaro Martín 10 h)
- **Tarifa Media / Coste Total:** 30 €/h | 600,00 €

### Criterios de aceptación
- **US-016-AC-01 (Rate-limiting):** El middleware limita las peticiones por IP a un máximo de 10 intentos por minuto en los endpoints de autenticación (`/api/auth/*`) y 100 peticiones por minuto en el resto de la API, devolviendo HTTP `429 Too Many Requests` con cabecera `Retry-After` al superarse el umbral.
- **US-016-AC-02 (Prevención de SQLi y XSS):** Todas las consultas a base de datos utilizan sentencias parametrizadas/ORM y todas las entradas de texto de usuario se validan y escapan antes de persistirse o renderizarse, neutralizando payloads `<script>` o `' OR 1=1 --`.
- **US-016-AC-03 (Cabeceras de seguridad):** Las respuestas HTTP incluyen cabeceras de protección configuradas (`Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`).

### Verificación y restricciones
- **Reglas de Negocio:** Los bloqueos por *rate-limiting* son temporales (ventana deslizante de 60 segundos) y se registran en los logs de seguridad cuando una IP supera el umbral reiteradamente.
- **Restricciones:** Prohibido concatenar cadenas de texto directamente en consultas SQL nativas en todo el código fuente.
- **Requisitos No Funcionales (RNF):** Superar una batería de pruebas automatizadas de inyección SQL/XSS y ráfagas de peticiones sin caída del servicio ni ejecución de scripts.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Un script automatizado lanza 15 peticiones de login seguidas en 10 segundos: las primeras 10 reciben respuesta normal y de la 11 a la 15 reciben HTTP `429 Too Many Requests`.
  * *Caso Límite:* Intento de crear un festival con título `<script>alert(1)</script>`: el sistema sanitiza o rechaza la entrada impidiendo la ejecución de código en el navegador.
- **Supuestos:** El control de *rate-limiting* opera en memoria del servidor o sobre la instancia local de Redis.

---

## US-017 — Encriptación y ocultación de datos sensibles

- **Necesidad:** Proteger la privacidad de la información confidencial de los usuarios y garantizar la seguridad de la plataforma.
- **Objetivo:** Cifrar los datos sensibles en tránsito y en reposo, y enmascarar información privada en respuestas de la API y registros de servidor.
- **Historia de Usuario:** Como usuario, quiero que mis datos sensibles (contraseñas, tokens) no viajen en texto plano en las peticiones HTTP, para asegurar la privacidad de mi información.
- **Tipo:** Seguridad
- **Prioridad:** Should (Garantiza el cumplimiento normativo de protección de datos RGPD y buenas prácticas de cifrado).
- **Estimación:** 12 h-p
- **Incertidumbre:** Media
- **Predecesores:** US-001
- **Plan inicial:** IT-005 (Sprint 5)
- **Responsable:** Equipo (Justo Cilleros 6 h / Álvaro Martín 6 h)
- **Tarifa Media / Coste Total:** 30 €/h | 360,00 €

### Criterios de aceptación
- **US-017-AC-01:** Uso obligatorio del protocolo HTTPS / TLS 1.3 en todas las comunicaciones (redirección automática de HTTP a HTTPS mediante respuesta HTTP `301`).
- **US-017-AC-02:** Enmascaramiento de campos sensibles en los ficheros de log del servidor (`password`, `token`, `authorization` y `secret` se registran siempre como `***`).
- **US-017-AC-03 (Datos simulados y alcance de cifrado en reposo):** Operatividad exclusiva con datos sintéticos (excluyendo pasarelas de pago reales y PCI-DSS). Los campos ficticios de contacto sensible (`telefono` y `direccion` del perfil de usuario) se almacenan cifrados en reposo con AES-256, mientras que las contraseñas utilizan hash irreversible Bcrypt (coste ≥ 10).
- **US-017-AC-04:** Exclusión estricta de hashes de contraseñas, claves privadas y tokens internos en los objetos JSON devueltos por las respuestas de las APIs REST.

### Verificación y restricciones
- **Reglas de Negocio:** Ningún usuario, administrador o desarrollador tendrá acceso a las contraseñas en texto plano bajo ninguna circunstancia.
- **Restricciones:** Prohibido almacenar datos personales o bancarios reales. La clave de cifrado AES-256 se gestiona exclusivamente por variable de entorno.
- **Requisitos No Funcionales (RNF):** Cumplimiento de las directrices de ciberseguridad del proyecto para entornos web seguros y transporte protegido de tokens de sesión.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Petición `GET /api/users/me`: devuelve la información del perfil del usuario en JSON omitiendo por completo los campos `password_hash` y tokens internos.
  * *Caso Límite:* Intento de acceso inseguro mediante `http://`: el servidor devuelve un código de estado `301 Moved Permanently` redirigiendo inmediatamente hacia la versión `https://`.
  * *Caso Límite:* Registro de petición en logs: una solicitud con cuerpo `{"email": "a@a.com", "password": "Secret123!"}` se escribe en los registros del servidor como `{"email": "a@a.com", "password": "***"}`.
- **Supuestos:** Se dispone de un certificado SSL/TLS autofirmado o simulado configurado en el entorno local de desarrollo.