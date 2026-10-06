# EP-004 — Servicios y Productos para Proveedores

## US-012 — Alertas de stock bajo para Proveedores

* **Necesidad:** Evitar que los comerciantes y proveedores se queden sin inventario durante la venta en los festivales, previniendo la pérdida de ingresos.
* **Objetivo:** Notificar automáticamente al proveedor cuando el stock de un producto alcance su umbral mínimo configurado.
* **User Story:** Como Proveedor, quiero recibir avisos automáticos cuando el stock de mis artículos sea escaso, para reponer inventario antes de que se agote.
* **Priority:** Must
* **Estimate:** 12 h-p
* **Uncertainty:** Medium
* **Predecessors:** US-011
* **Initial plan:** IT-002 (Sprint 2)

### Acceptance criteria
* **US-012-AC-01:** Campo ejecutable "Umbral de Stock Mínimo" en la ficha de cada producto del proveedor (ej. umbral = 10 unidades).
* **US-012-AC-02:** Al procesarse una venta que deje el stock del artículo en un valor igual o inferior al umbral, se envía una alerta por correo electrónico al proveedor.
* **US-012-AC-03:** Visualización del indicador de color amarillo/rojo "Stock Crítico" en el panel de inventario del proveedor.

### Verification and constraints
* **Reglas de Negocio:** La alerta de correo electrónico solo se genera una vez por cada evento de bajada de umbral, hasta que el proveedor incremente el inventario.
* **Restricciones:** El servicio de mensajería debe reintentar la entrega del correo hasta 3 veces en caso de fallo temporal en la pasarela SMTP.
* **Requisitos No Funcionales (RNF):** Procesamiento asíncrono en segundo plano (vía cola de tareas) para no penalizar el tiempo de respuesta de la compra del cliente.
* **Ejemplos y Casos Límite:**
  * *Ejemplo:* Quedan 11 camisetas. Un cliente compra 2. Quedan 9 (por debajo del umbral de 10): se dispara el email de aviso en menos de 5 segundos.
  * *Caso Límite:* Compra masiva que agota el stock a 0 de golpe: se envían simultáneamente las alertas de "Stock Bajo" y "Producto Agotado".
* **Supuestos:** Se asume la disponibilidad de un servicio SMTP o pasarela de correo transaccional (SendGrid/Mailgun/AWS SES).
