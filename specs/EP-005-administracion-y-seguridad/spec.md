# EP-005 — Administración Global, Seguridad y Analítica

## US-018 — Encriptación y ocultación de datos sensibles

* **Necesidad:** Proteger la privacidad de la información confidencial de los usuarios y garantizar la seguridad de la plataforma.
* **Objetivo:** Cifrar los datos sensibles en tránsito y en reposo, y enmascarar información privada en respuestas de la API y registros de servidor.
* **Historia de Usuario:** Como usuario, quiero que mis datos sensibles (contraseñas, tokens de acceso y datos personales) estén cifrados y protegidos, para evitar filtraciones y asegurar mi privacidad.
* **Prioridad:** Should
* **Estimación:** 12 h-p
* **Incertidumbre:** Media
* **Predecesores:** US-001
* **Plan inicial:** IT-001 (Sprint 1)

### Criterios de aceptación
* **US-018-AC-01:** Uso obligatorio del protocolo HTTPS / TLS 1.3 en todas las comunicaciones (redirección automática de HTTP a HTTPS mediante respuesta HTTP `301`).
* **US-018-AC-02:** Enmascaramiento de campos sensibles en los ficheros de log del servidor (contraseñas, tokens y claves de acceso se registran siempre como `***`).
* **US-018-AC-03 (Datos simulados y alcance de pagos):** Operatividad exclusiva mediante entornos de prueba y datos simulados. Se excluye expresamente la integración de pasarelas de pago reales y el cumplimiento de la normativa PCI-DSS, quedando prohibido cualquier almacenamiento de datos bancarios reales.
* **US-018-AC-04:** Exclusión estricta de hashes de contraseñas, claves privadas y tokens en los objetos JSON devueltos por las respuestas de las APIs REST.

### Verificación y restricciones
* **Reglas de Negocio:** Ningún usuario, administrador o desarrollador tendrá acceso a las contraseñas en texto plano bajo ninguna circunstancia.
* **Restricciones:** El almacenamiento de credenciales de usuario se realiza exclusivamente mediante algoritmos de *hashing* seguro (Bcrypt con factor de coste ≥ 10). Los campos de datos personales sensibles en reposo se cifran con AES-256.
* **Requisitos No Funcionales (RNF):** Cumplimiento de las directrices de ciberseguridad del proyecto para entornos web seguros y transporte protegido de tokens de sesión.
* **Ejemplos y Casos Límite:**
  * *Ejemplo:* Petición `GET /api/users/me`: devuelve la información del perfil del usuario en JSON omitiendo por completo los campos `password_hash` y tokens sensibles.
  * *Caso Límite:* Intento de acceso inseguro mediante `http://`: el servidor devuelve un código de estado `301 Moved Permanently` redirigiendo inmediatamente hacia la versión `https://`.
  * *Caso Límite:* Registro de petición en logs: una solicitud con cuerpo `{"email": "a@a.com", "password": "Secret123!"}` se escribe en los registros del servidor como `{"email": "a@a.com", "password": "***"}`.
* **Supuestos:** Se dispone de un certificado SSL/TLS (o certificado simulado en desarrollo) configurado correctamente en el servidor web.