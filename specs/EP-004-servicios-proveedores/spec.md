# EP-004 — Servicios y Productos para Proveedores

## US-012 — Alertas de stock bajo para Proveedores

* **Necesidad:** Evitar que los comerciantes y proveedores se queden sin inventario durante la venta en los festivales, previniendo la pérdida de ingresos.
* **Objetivo:** Notificar automáticamente al proveedor cuando el stock de un producto alcance su umbral mínimo configurado.
* **Historia de Usuario:** Como Proveedor, quiero recibir avisos automáticos cuando el stock de mis artículos sea escaso, para reponer inventario antes de que se agote.
* **Prioridad:** Must
* **Estimación:** 12 h-p
* **Incertidumbre:** Media
* **Predecesores:** US-011
* **Plan inicial:** IT-002 (Sprint 2)

### Criterios de aceptación
* **US-012-AC-01 (Configuración de umbral):** Campo editable "Umbral de Stock Mínimo" en la ficha de gestión de cada producto del proveedor, permitiendo asignar únicamente valores enteros mayores o iguales a cero (ej. umbral = 10 unidades).
* **US-012-AC-02 (Notificación por email):** Al procesarse una venta que deje el stock del artículo en un valor igual o inferior al umbral configurado, se envía una alerta por correo electrónico al proveedor.
* **US-012-AC-03 (Indicador visual en panel):** Muestra de un distintivo visual codificado por colores ("Stock Crítico" en amarillo/rojo) en el panel de inventario del proveedor.
* **US-012-AC-04 (Control de reintentos y tolerancia a fallos):** La notificación por correo se dispara una sola vez por evento hasta que se registre una reposición de stock. Si el servicio de envío agota los 3 reintentos por fallo de la pasarela SMTP, el evento queda registrado en los logs del sistema sin bloquear la transacción de compra del cliente.

### Verificación y restricciones
* **Reglas de Negocio:** La alerta de correo electrónico solo se genera una vez por cada evento de bajada de umbral, hasta que el proveedor incremente el inventario.
* **Restricciones:** El servicio de mensajería debe reintentar la entrega del correo hasta 3 veces en caso de fallo temporal en la pasarela SMTP.
* **Requisitos No Funcionales (RNF):** Procesamiento asíncrono en segundo plano (vía cola de tareas) para no penalizar el tiempo de respuesta de la compra del cliente.
* **Ejemplos y Casos Límite:**
  * *Ejemplo:* Quedan 11 camisetas. Un cliente compra 2. Quedan 9 (por debajo del umbral de 10): se dispara el email de aviso en menos de 5 segundos.
  * *Caso Límite:* Compra masiva que agota el stock a 0 de golpe: se envían simultáneamente las alertas de "Stock Bajo" y "Producto Agotado".
  * *Caso Límite:* Intento de introducir un umbral negativo: el sistema bloquea el valor indicando el mensaje "El umbral de stock debe ser un número entero mayor o igual a 0".
* **Supuestos:** Se asume la disponibilidad de un servicio SMTP o pasarela de correo transaccional (SendGrid/Mailgun/AWS SES).