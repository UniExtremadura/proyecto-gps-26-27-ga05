# EP-001 — Autenticación y Gestión de Usuarios y Roles

## US-001 — Registro e inicio de sesión de usuarios

* **Necesidad:** Identificar de forma única a los usuarios de la plataforma para permitirles realizar compras, publicar eventos o gestionar recintos con seguridad.
* **Objetivo:** Disponer de un subsistema de autenticación local mediante credenciales (correo electrónico y contraseña).
* **User Story:** Como usuario (visitante), quiero registrarme e iniciar sesión con mi correo electrónico y contraseña, para acceder a las funcionalidades personalizadas de mi cuenta.
* **Priority:** Must
* **Estimate:** 10 h-p
* **Uncertainty:** Low
* **Predecessors:** —
* **Initial plan:** IT-001 (Sprint 1)

### Acceptance criteria
* **US-001-AC-01:** Registro exitoso con email único, contraseña segura (mínimo 8 caracteres, 1 mayúscula, 1 número) y confirmación de contraseña.
* **US-001-AC-02:** Inicio de sesión que emite un token JWT con tiempo de expiración de 24 horas tras validar credenciales.
* **US-001-AC-03:** Mensaje de error genérico "Credenciales incorrectas" al fallar la autenticación, evitando revelar si el fallo es del correo o de la clave.
* **US-001-AC-04:** Cierre de sesión (*logout*) que invalida la sesión/token en el cliente.

### Verification and constraints
* **Reglas de Negocio:** El correo electrónico se normalizará a minúsculas. No pueden coexistir dos cuentas activas con el mismo correo electrónico.
* **Restricciones:** Las contraseñas deben cifrarse obligatoriamente mediante un algoritmo de *hashing* seguro (Bcrypt con factor de coste ≥ 10) antes de ser almacenadas en la base de datos.
* **Requisitos No Funcionales (RNF):** Tiempo de procesamiento del inicio de sesión < 500 ms.
* **Ejemplos y Casos Límite:**
  * *Ejemplo:* Registro con `usuario@ejemplo.com` y clave `Festival2026!`: crea la cuenta e inicia sesión automáticamente.
  * *Caso Límite:* Intento de registro con un correo ya existente: el sistema cancela el proceso y muestra "El correo electrónico ya está registrado".
  * *Caso Límite:* Inyección de espacios o scripts en el campo email: se sanitiza y valida según la sintaxis RFC 5322 antes de procesar.
* **Supuestos:** Se asume que el usuario tiene acceso a la cuenta de correo electrónico proporcionada.

---

## US-003 — Consulta y modificación de perfil de Cliente

* **Necesidad:** Permitir al cliente gestionar sus datos personales y mantener actualizada la información de contacto para la facturación y el envío de entradas.
* **Objetivo:** Disponer de un panel de perfil donde el usuario pueda consultar y actualizar sus datos.
* **User Story:** Como Cliente, quiero consultar y modificar los datos de mi perfil personal (nombre, dirección, teléfono, correo), para mantener mi información actualizada.
* **Priority:** Should
* **Estimate:** 6 h-p
* **Uncertainty:** Low
* **Predecessors:** US-001
* **Initial plan:** IT-002 (Sprint 2)

### Acceptance criteria
* **US-003-AC-01:** Visualización organizada de los datos actuales del usuario al acceder a la vista `/perfil`.
* **US-003-AC-02:** Formulario de edición que permite modificar nombre, teléfono y dirección con guardado inmediato.
* **US-003-AC-03:** Si se solicita cambiar la dirección de correo electrónico, el sistema requiere introducir la contraseña actual por motivos de seguridad.

### Verification and constraints
* **Reglas de Negocio:** Solo los usuarios con rol "Cliente" pueden editar su perfil de cliente. Todas las modificaciones se registran con marca temporal de actualización.
* **Restricciones:** Los campos obligatorios (Nombre y Apellidos) no pueden quedarse vacíos ni contener solo espacios en blanco.
* **Requisitos No Funcionales (RNF):** Formulario accesible (cumplimiento WCAG 2.1 AA) y adaptable (*responsive*) a dispositivos móviles.
* **Ejemplos y Casos Límite:**
  * *Ejemplo:* Cambio de teléfono de "600000000" a "611111111": se guarda en la BD y muestra la notificación "Perfil actualizado correctamente".
  * *Caso Límite:* Intento de cambiar el correo a uno que ya pertenece a otro usuario registrado: el sistema deniega el cambio y notifica el conflicto.
* **Supuestos:** Se asume que la modificación de la dirección de contacto no altera los datos de facturación de entradas o pedidos emitidos con anterioridad.
