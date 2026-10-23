# EP-001 — Autenticación y Gestión de Usuarios y Roles

## US-001 — Registro e inicio de sesión de usuarios

- **Necesidad:** Identificar de forma única a los usuarios de la plataforma para permitirles realizar compras, publicar eventos o gestionar recintos con seguridad.
- **Objetivo:** Disponer de un subsistema de autenticación local mediante credenciales (correo electrónico y contraseña).
- **Historia de Usuario:** Como usuario, quiero registrarme e iniciar sesión con mi correo electrónico y contraseña, para acceder a las funcionalidades personalizadas del sistema.
- **Tipo:** Funcional
- **Prioridad:** Must (Punto de entrada obligatorio para la identificación de clientes, organizadores y proveedores).
- **Estimación:** 10 h-p
- **Incertidumbre:** Baja
- **Predecesores:** —
- **Plan inicial:** IT-001 (Sprint 1)
- **Coste Total Estimado:** 290,00 € (desglosado en tareas TK)
- **Desglose de tareas (IT-001):**
  - `TK-001-1`: Backend API Auth — Desarrollo de endpoints de registro y login (5 h-p | Predecesor: — | Responsable: Justo Cilleros | Tarifa: 25 €/h | Coste: 125,00 €).
  - `TK-001-2`: Frontend Auth form — Maquetación y conexión de formularios (3 h-p | Predecesor: `TK-001-1` | Responsable: Álvaro Martín | Tarifa: 35 €/h | Coste: 105,00 €).
  - `TK-001-3`: Testing Auth — Pruebas unitarias y de integración (2 h-p | Predecesor: `TK-001-2` | Responsable: Manuel Carvajal | Tarifa: 30 €/h | Coste: 60,00 €).

### Criterios de aceptación
- **US-001-AC-01:** Registro exitoso con email único, contraseña segura (mínimo 8 caracteres, 1 mayúscula, 1 número) y confirmación de contraseña.
- **US-001-AC-02:** Inicio de sesión que emite un token JWT con tiempo de expiración de 24 horas tras validar credenciales.
- **US-001-AC-03:** Mensaje de error genérico "Credenciales incorrectas" al fallar la autenticación, evitando revelar si el fallo es del correo o de la clave.
- **US-001-AC-04:** Cierre de sesión (*logout*) que destruye el token en el cliente y envía una petición a la API (`POST /api/auth/logout`) que añade el token a la lista de revocación (*blacklist*) en el servidor.
- **US-001-AC-05:** Cualquier petición posterior utilizando un token revocado o expirado debe ser rechazada con un código HTTP `401 Unauthorized`.

### Verificación y restricciones
- **Reglas de Negocio:** El correo electrónico se normalizará a minúsculas. No pueden coexistir dos cuentas activas con el mismo correo electrónico.
- **Restricciones:** Las contraseñas deben cifrarse obligatoriamente mediante Bcrypt (factor de coste ≥ 10). Uso exclusivo de datos ficticios.
- **Requisitos No Funcionales (RNF):** Tiempo de procesamiento del inicio de sesión < 500 ms.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Registro con `usuario@ejemplo.com` y clave `Festival2026!`: crea la cuenta e inicia sesión automáticamente.
  * *Caso Límite:* Intento de registro con un correo ya existente: devuelve error `409 Conflict` e indica "El correo electrónico ya está registrado".
- **Supuestos:** Se asume el uso de cuentas de correo simuladas para las pruebas del entorno local.

---

## US-002 — Gestión de roles y permisos diferidos

- **Necesidad:** Garantizar que cada actor del sistema acceda únicamente a las vistas y operaciones autorizadas para su perfil.
- **Objetivo:** Implementar un control de acceso basado en roles (RBAC) en backend y frontend.
- **Historia de Usuario:** Como usuario del sistema, quiero tener un rol asignado (Guest, Cliente, Organizador, Proveedor, Admin) con interfaces y permisos específicos, para interactuar de forma segura según mi perfil.
- **Tipo:** Funcional
- **Prioridad:** Must (Arquitectura base del sistema necesaria para restringir el acceso a funcionalidades privadas).
- **Estimación:** 14 h-p
- **Incertidumbre:** Media
- **Predecesores:** US-001
- **Plan inicial:** IT-001 (Sprint 1)
- **Coste Total Estimado:** 410,00 € (desglosado en tareas TK)
- **Desglose de tareas (IT-001):**
  - `TK-002-1`: DB Roles Setup — Configuración de esquema de roles en BBDD (4 h-p | Predecesor: `US-001` | Responsable: Álvaro Martín | Tarifa: 35 €/h | Coste: 140,00 €).
  - `TK-002-2`: Middleware Auth — Lógica de validación de JWT y roles (6 h-p | Predecesor: `TK-002-1` | Responsable: Justo Cilleros | Tarifa: 25 €/h | Coste: 150,00 €).
  - `TK-002-3`: Test Roles — Verificación de accesos denegados/permitidos (4 h-p | Predecesor: `TK-002-2` | Responsable: Manuel Carvajal | Tarifa: 30 €/h | Coste: 120,00 €).

### Criterios de aceptación
- **US-002-AC-01:** El sistema soporta los roles `Guest`, `Cliente`, `Organizador`, `Proveedor` y `Admin` asociados al perfil de usuario y codificados en las reclamaciones (*claims*) del token JWT.
- **US-002-AC-02:** El middleware de autorización verifica el rol del usuario antes de ejecutar cualquier endpoint protegido, devolviendo `403 Forbidden` si el rol no tiene permisos suficientes.
- **US-002-AC-03:** La interfaz de usuario oculta las rutas y menús de administración, organización o proveedor a los usuarios que no posean dicho rol activo.

### Verificación y restricciones
- **Reglas de Negocio:** Todo usuario nuevo registrado por el flujo estándar adquiere por defecto el rol `Cliente`. Los roles `Organizador`, `Proveedor` y `Admin` solo pueden ser asignados por un `Admin`.
- **Restricciones:** La validación de permisos es obligatoria en el servidor (API REST) y no puede depender únicamente del ocultamiento en cliente.
- **Requisitos No Funcionales (RNF):** Sobrecarga de validación del middleware < 20 ms por petición.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Un usuario con rol `Cliente` intenta acceder a `POST /api/events`: recibe HTTP `403 Forbidden`.
  * *Caso Límite:* Un usuario sin sesión (`Guest`) intenta acceder a `/perfil`: es redirigido automáticamente a `/login` con estado `401 Unauthorized`.
- **Supuestos:** Se dispone de semillas de datos (*seeders*) con usuarios ficticios preconfigurados para cada uno de los 5 roles.

---

## US-003 — Consulta y modificación de perfil de Cliente

- **Necesidad:** Permitir al cliente gestionar sus datos personales y mantener actualizada la información de contacto para el envío de entradas.
- **Objetivo:** Disponer de un panel de perfil donde el usuario pueda consultar y actualizar sus datos.
- **Historia de Usuario:** Como Cliente, quiero consultar y actualizar mis datos personales (nombre, dirección, correo), para mantener mi información actualizada.
- **Tipo:** Funcional
- **Prioridad:** Should (Aporta valor al cliente para gestionar sus datos, aunque la compra básica puede operar con datos iniciales).
- **Estimación:** 6 h-p
- **Incertidumbre:** Baja
- **Predecesores:** US-001
- **Plan inicial:** IT-004 (Sprint 4)
- **Responsable:** Equipo (Justo Cilleros — 6 h)
- **Tarifa Media / Coste Total:** 30 €/h | 180,00 €

### Criterios de aceptación
- **US-003-AC-01:** Visualización organizada de los datos actuales del usuario al acceder a la vista `/perfil`.
- **US-003-AC-02:** Formulario de edición que permite modificar nombre, teléfono y dirección con guardado inmediato y respuesta HTTP `200 OK`.
- **US-003-AC-03:** Si se solicita cambiar la dirección de correo electrónico, el sistema requiere introducir la contraseña actual por motivos de seguridad y envía un email de verificación a la nueva dirección antes de hacer efectivo el cambio.
- **US-003-AC-04:** Si la contraseña actual es incorrecta o los datos no cumplen el formato (email inválido o teléfono con letras), el sistema muestra un mensaje de error específico y devuelve un código HTTP `400 Bad Request`.

### Verificación y restricciones
- **Reglas de Negocio:** Solo los usuarios autenticados pueden editar su propio perfil. Todas las modificaciones se registran con marca temporal de actualización.
- **Restricciones:** Los campos obligatorios (Nombre y Correo) no pueden quedarse vacíos ni contener solo espacios en blanco. Uso exclusivo de datos sintéticos.
- **Requisitos No Funcionales (RNF):** Formulario accesible (cumplimiento WCAG 2.1 AA) y adaptable (*responsive*) a dispositivos móviles.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Cambio de teléfono de `600000000` a `611111111`: se guarda en la BD y muestra la notificación "Perfil actualizado correctamente".
  * *Caso Límite:* Intento de cambiar el correo a uno que ya pertenece a otro usuario registrado: el sistema deniega el cambio y notifica el conflicto (`409 Conflict`).
- **Supuestos:** Se asume que la modificación de los datos de contacto no altera las reservas emitidas con anterioridad.

---

## US-004 — Autenticación mediante OAuth 2.0

- **Necesidad:** Agilizar el registro e inicio de sesión mediante cuentas externas de confianza sin obligar al usuario a recordar nuevas contraseñas.
- **Objetivo:** Integrar el flujo de autenticación delegada mediante el estándar OAuth 2.0 (Google / Apple simulado en desarrollo).
- **Historia de Usuario:** Como usuario, quiero iniciar sesión mediante proveedores externos (Google, Apple) con OAuth 2.0, para agilizar el proceso de acceso sin crear contraseñas adicionales.
- **Tipo:** Técnico
- **Prioridad:** Must (Requisito técnico clave para reducir la fricción en el registro e incrementar la conversión de ventas).
- **Estimación:** 16 h-p
- **Incertidumbre:** Media
- **Predecesores:** US-001
- **Plan inicial:** IT-001 (Sprint 1)
- **Coste Total Estimado:** 470,00 € (desglosado en tareas TK)
- **Desglose de tareas (IT-001):**
  - `TK-004-1`: Config OAuth Providers — Alta y configuración de credenciales en Google/Apple (3 h-p | Predecesor: `US-001` | Responsable: Javier García | Tarifa: 35 €/h | Coste: 105,00 €).
  - `TK-004-2`: Backend OAuth logic — Callbacks y validación de tokens externos (5 h-p | Predecesor: `TK-004-1` | Responsable: Justo Cilleros | Tarifa: 25 €/h | Coste: 125,00 €).
  - `TK-004-3`: Frontend OAuth flow — Botones sociales y redirección (5 h-p | Predecesor: `TK-004-1` | Responsable: Manuel Carvajal | Tarifa: 30 €/h | Coste: 150,00 €).
  - `TK-004-4`: Documentación OAuth — Documentar variables de entorno y arquitectura (3 h-p | Predecesor: `TK-004-3` | Responsable: Jaime Arias | Tarifa: 30 €/h | Coste: 90,00 €).

### Criterios de aceptación
- **US-004-AC-01:** La pantalla de acceso incluye botones de inicio de sesión con Google y Apple que redirigen al flujo de autorización OAuth 2.0.
- **US-004-AC-02:** Al recibir un *callback* válido del proveedor con el código de autorización, el backend valida el token, crea o vincula la cuenta con rol `Cliente` y emite el JWT propio de la plataforma.
- **US-004-AC-03:** Si el usuario cancela la autorización en la ventana externa o el token es inválido, el sistema retorna a `/login` mostrando el aviso "Autenticación externa cancelada o no válida".

### Verificación y restricciones
- **Reglas de Negocio:** Si el correo devuelto por el proveedor OAuth 2.0 ya existe en la base de datos local, se vincula la identidad federada a la cuenta existente sin duplicar el usuario.
- **Restricciones:** Las claves `CLIENT_ID` y `CLIENT_SECRET` se inyectan mediante variables de entorno (`.env`) y nunca se suben al repositorio Git.
- **Requisitos No Funcionales (RNF):** Protección obligatoria mediante parámetro `state` contra ataques CSRF durante la redirección OAuth 2.0.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Usuario pulsa "Continuar con Google", acepta permisos de prueba y accede directamente al catálogo con sesión iniciada.
  * *Caso Límite:* Respuesta OAuth con parámetro `state` alterado o caducado: el backend aborta la sesión y devuelve HTTP `400 Bad Request`.
- **Supuestos:** En entorno local de evaluación se emplean credenciales de *sandbox*/desarrollo o un proveedor OAuth simulado (*mock*) para no requerir cuentas personales reales.

---

## US-005 — Restablecimiento de contraseña por correo

- **Necesidad:** Ofrecer un mecanismo autónomo para que los usuarios recuperen el acceso a su cuenta en caso de olvido de contraseña.
- **Objetivo:** Implementar un flujo de generación y validación de enlaces temporales de recuperación por correo electrónico.
- **Historia de Usuario:** Como usuario registrado, quiero solicitar un enlace de restablecimiento de contraseña por email, para recuperar el acceso a mi cuenta si me olvido de las credenciales.
- **Tipo:** Seguridad
- **Prioridad:** Should (Funcionalidad esencial de usabilidad y autoservicio para reducir llamadas a soporte).
- **Estimación:** 8 h-p
- **Incertidumbre:** Baja
- **Predecesores:** US-001
- **Plan inicial:** IT-005 (Sprint 5)
- **Responsable:** Equipo (Justo Cilleros 4 h / Manuel Carvajal 4 h)
- **Tarifa Media / Coste Total:** 30 €/h | 240,00 €

### Criterios de aceptación
- **US-005-AC-01:** Al introducir un correo en `/recuperar-password`, el sistema devuelve siempre el mismo mensaje de confirmación ("Si el correo está registrado, recibirás un enlace de recuperación") para evitar la enumeración de usuarios.
- **US-005-AC-02:** Si el correo existe, se genera un token criptográfico de un solo uso con caducidad de 15 minutos y se envía el enlace de restablecimiento mediante el servicio SMTP simulado.
- **US-005-AC-03:** Al enviar la nueva contraseña válida junto con el token vigente, el sistema actualiza el hash Bcrypt de la clave, invalida el token de recuperación y revoca las sesiones anteriores.

### Verificación y restricciones
- **Reglas de Negocio:** Cada token de recuperación solo puede utilizarse una única vez. Solicitar un nuevo enlace invalida cualquier token previo pendiente para ese usuario.
- **Restricciones:** La nueva contraseña debe cumplir las mismas reglas de complejidad definidas en `US-001`.
- **Requisitos No Funcionales (RNF):** Los tokens de restablecimiento deben almacenarse hasheados en la base de datos.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Usuario solicita recuperación, abre el enlace antes de 15 minutos, introduce su nueva clave y accede con éxito en `/login`.
  * *Caso Límite:* Intento de usar un enlace transcurridos más de 15 minutos o ya utilizado: devuelve HTTP `400 Bad Request` con el mensaje "El enlace de recuperación ha expirado o no es válido".
- **Supuestos:** En el entorno de desarrollo se utiliza un buzón SMTP local simulado (ej. Mailpit/Mailtrap) para inspeccionar los correos enviados.