# EP-005 — Administración Global, Seguridad y Analítica

## US-018 — Encriptación y ocultación de datos sensibles

* **Necesidad:** Proteger la privacidad de la información confidencial de los usuarios y garantizar el cumplimiento normativo de ciberseguridad y protección de datos (RGPD).
* **Objetivo:** Cifrar los datos sensibles en tránsito y en reposo, y enmascarar información privada en respuestas de la API y registros de servidor.
* **User Story:** Como usuario, quiero que mis datos sensibles (contraseñas, datos de pago, tokens) estén encriptados y protegidos, para evitar filtraciones y asegurar mi privacidad.
* **Priority:** Should
* **Estimate:** 12 h-p
* **Uncertainty:** Medium
* **Predecessors:** US-001
* **Initial plan:** IT-001 (Sprint 1)

### Acceptance criteria
* **US-018-AC-01:** Uso obligatorio del protocolo HTTPS / TLS 1.3 en todas las comunicaciones (redirección automática de HTTP a HTTPS).
* **US-018-AC-02:** Enmascaramiento de campos sensibles en los ficheros de log del servidor (contraseñas y tokens se registran como `***`).
* **US-018-AC-03:** Cifrado AES-256 para campos de datos personales altamente sensibles almacenados en la base de datos.
* **US-018-AC-04:** Exclusión estricta de hash de contraseñas y claves privadas en los JSON de respuesta de las APIs REST.

### Verification and constraints
* **Reglas de Negocio:** Ningún usuario, administrador o desarrollador tendrá acceso a las contraseñas en texto plano.
* **Restricciones:** Prohibición absoluta de almacenar el código CVC/CVV2 de las tarjetas de crédito en las bases de datos del sistema (cumplimiento PCI-DSS).
* **Requisitos No Funcionales (RNF):** Cumplimiento estricto del Reglamento General de Protección de Datos (RGPD) de la Unión Europea.
* **Ejemplos y Casos Límite:**
  * *Ejemplo:* Petición `GET /api/users/me`: devuelve la información del usuario en JSON omitiendo el campo `password_hash`.
  * *Caso Límite:* Intento de acceso inseguro mediante `http://`: el servidor devuelve un código de estado `301 Moved Permanently` hacia la versión `https://`.
* **Supuestos:** Se dispone de un certificado SSL/TLS válido instalado en el servidor de producción.
