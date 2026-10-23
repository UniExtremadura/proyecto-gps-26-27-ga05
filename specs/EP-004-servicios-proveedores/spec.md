# EP-004 — Servicios y Productos para Proveedores

## US-009 — Consulta y reserva de recintos por Proveedores

- **Necesidad:** Permitir a los proveedores de servicios (hostelería, sonido, stands) consultar qué espacios o zonas están disponibles en los festivales y solicitar su reserva.
- **Objetivo:** Dotar a los usuarios con rol Proveedor de un buscador y sistema de reserva de espacios/recintos asociados a los festivales.
- **Historia de Usuario:** Como Proveedor, quiero consultar la disponibilidad de recintos/espacios y reservarlos, para prestar mis servicios durante los festivales.
- **Tipo:** Funcional
- **Prioridad:** Must (Permite la operatividad B2B del ecosistema de proveedores dentro de las instalaciones del evento).
- **Estimación:** 16 h-p
- **Incertidumbre:** Media
- **Predecesores:** US-002
- **Plan inicial:** IT-003 (Sprint 3)
- **Responsable:** Equipo (Justo Cilleros 8 h / Álvaro Martín 8 h)
- **Tarifa Media / Coste Total:** 30 €/h | 480,00 €

### Criterios de aceptación
- **US-009-AC-01:** El proveedor autenticado visualiza el listado de festivales activos con sus espacios/zonas para proveedores indicando estado (`Disponible`, `Reservado`), dimensiones y tarifa simulada.
- **US-009-AC-02:** El proveedor puede seleccionar un espacio `Disponible` y confirmar su reserva ficticia, cambiando inmediatamente el estado del espacio a `Reservado` y asociándolo a su cuenta.
- **US-009-AC-03:** Si dos proveedores intentan reservar el mismo espacio simultáneamente, el sistema procesa únicamente la primera transacción y devuelve HTTP `409 Conflict` al segundo indicando "El espacio seleccionado ya no está disponible".

### Verificación y restricciones
- **Reglas de Negocio:** Solo usuarios con rol `Proveedor` o `Admin` pueden realizar o gestionar reservas de espacios B2B. Un proveedor puede cancelar su reserva mientras falten más de 7 días para el inicio del festival.
- **Restricciones:** Las reservas de espacios son 100% simuladas y no conllevan cobros bancarios ni facturación fiscal real.
- **Requisitos No Funcionales (RNF):** Bloqueo pesimista u optimista en base de datos para impedir dobles reservas del mismo espacio.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Proveedor reserva el "Stand Zona Gastro A-01" para el festival "Subsonic 2026": recibe confirmación en pantalla y el espacio pasa a `Reservado`.
  * *Caso Límite:* Intento de reservar un espacio en un festival ya finalizado o pausado: devuelve HTTP `400 Bad Request`.
- **Supuestos:** Los festivales disponen de zonas/espacios de proveedor predefinidos en los datos semilla del sistema.

---

## US-010 — Venta y gestión de catálogo de merchandising

- **Necesidad:** Ofrecer a los proveedores un canal digital integrado para publicar y gestionar los artículos de merchandising asociados a los festivales.
- **Objetivo:** Implementar un módulo CRUD de catálogo e inventario de productos de merchandising para el rol Proveedor.
- **Historia de Usuario:** Como Proveedor, quiero publicar y gestionar mis artículos de merchandising, para venderlos a los asistentes del festival a través de la web.
- **Tipo:** Funcional
- **Prioridad:** Must (Vía secundaria clave de ingresos para la plataforma y los proveedores asociados).
- **Estimación:** 14 h-p
- **Incertidumbre:** Baja
- **Predecesores:** US-002
- **Plan inicial:** IT-004 (Sprint 4)
- **Responsable:** Equipo (Justo Cilleros 7 h / Manuel Carvajal 7 h)
- **Tarifa Media / Coste Total:** 30 €/h | 420,00 €

### Criterios de aceptación
- **US-010-AC-01:** El proveedor dispone de un panel para dar de alta, editar y dar de baja artículos de merchandising indicando nombre, descripción, precio simulado (€), festival asociado y stock disponible.
- **US-010-AC-02:** Los artículos publicados con stock mayor a 0 se muestran en la vista pública del festival para que los clientes puedan añadirlos a su reserva simulada, descontando automáticamente las unidades del inventario.
- **US-010-AC-03:** El sistema impide guardar artículos con precio negativo o stock menor que cero, devolviendo HTTP `400 Bad Request` con mensajes de validación claros.

### Verificación y restricciones
- **Reglas de Negocio:** Cada proveedor solo puede editar o eliminar los artículos de merchandising que pertenecen a su propio catálogo. Cuando el stock llega a 0, el artículo se muestra como "Agotado" y no permite nuevas reservas.
- **Restricciones:** Todas las transacciones de compra de merchandising son simuladas con datos sintéticos.
- **Requisitos No Funcionales (RNF):** Actualización atómica del contador de inventario en cada reserva simulada.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Alta de "Camiseta Oficial Subsonic" a 20 € con 50 unidades de stock: aparece publicada en la ficha del festival.
  * *Caso Límite:* Un cliente intenta reservar 5 unidades cuando solo quedan 2 en stock: el sistema bloquea la operación e informa "Solo quedan 2 unidades disponibles".
- **Supuestos:** Las imágenes de productos utilizan recursos locales o URLs ficticias de prueba.

---

## US-011 — Alertas de stock bajo para Proveedores

- **Necesidad:** Evitar que los comerciantes y proveedores se queden sin inventario durante la venta en los festivales, previniendo la pérdida de ingresos.
- **Objetivo:** Notificar automáticamente al proveedor cuando el stock de un producto alcance su umbral mínimo configurado.
- **Historia de Usuario:** Como Proveedor, quiero recibir avisos automáticos cuando las unidades de un producto sean escasas, para reponer inventario a tiempo.
- **Tipo:** Técnico
- **Prioridad:** Must (Evita roturas de stock y pérdidas de ventas durante los picos de demanda en los festivales).
- **Estimación:** 12 h-p
- **Incertidumbre:** Media
- **Predecesores:** US-010
- **Plan inicial:** IT-004 (Sprint 4)
- **Responsable:** Equipo (Justo Cilleros 6 h / Álvaro Martín 6 h)
- **Tarifa Media / Coste Total:** 30 €/h | 360,00 €

### Criterios de aceptación
- **US-011-AC-01 (Configuración de umbral):** Campo editable "Umbral de Stock Mínimo" en la ficha de gestión de cada producto del proveedor, permitiendo asignar únicamente valores enteros mayores o iguales a cero (ej. umbral = 10 unidades).
- **US-011-AC-02 (Notificación por email en cruce de umbral):** Cuando una reserva reduce el stock de un valor superior al umbral a un valor igual o inferior al umbral configurado (y mayor que 0), se envía una única alerta de "Stock Bajo" por correo electrónico al proveedor. Si el stock llega a 0, se emite la alerta de "Producto Agotado".
- **US-011-AC-03 (Indicador visual en panel):** Muestra de un distintivo visual codificado por colores ("Stock Bajo" en amarillo cuando `0 < stock <= umbral` y "Agotado" en rojo cuando `stock == 0`) en el panel de inventario del proveedor.
- **US-011-AC-04 (Rearme y tolerancia a fallos):** La alerta se rearma únicamente cuando el proveedor repone stock situándolo por encima del umbral configurado. Si el servicio SMTP falla tras 3 reintentos, el evento queda registrado en los logs del sistema sin bloquear la reserva del cliente.

### Verificación y restricciones
- **Reglas de Negocio:** No se envían correos duplicados de "Stock Bajo" en ventas sucesivas mientras el artículo permanezca por debajo del umbral sin haber sido repuesto por encima de dicho umbral.
- **Restricciones:** El servicio de mensajería reintenta la entrega del correo hasta 3 veces en caso de fallo temporal en la pasarela SMTP simulada.
- **Requisitos No Funcionales (RNF):** Procesamiento asíncrono o no bloqueante para no penalizar el tiempo de respuesta de la reserva del cliente.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Quedan 11 camisetas (umbral 10). Un cliente reserva 2 y quedan 9: se dispara el email de aviso en menos de 5 segundos.
  * *Caso Límite:* Intento de introducir un umbral negativo: el sistema bloquea el valor indicando el mensaje "El umbral de stock debe ser un número entero mayor o igual a 0".
- **Supuestos:** Se dispone de un servicio SMTP simulado en el entorno local de desarrollo.

---

## US-013 — Historial y reporte de ventas de mercancía

- **Necesidad:** Facilitar a los proveedores el seguimiento de las reservas y ventas simuladas de sus productos para evaluar su rendimiento comercial.
- **Objetivo:** Proporcionar un listado filtrable y métricas agregadas de las ventas de merchandising de cada proveedor.
- **Historia de Usuario:** Como Proveedor, quiero ver el listado y métricas de mis ventas de artículos recientes, para analizar el rendimiento de mis productos.
- **Tipo:** Funcional
- **Prioridad:** Must (Indispensable para el cuadre contable y liquidación financiera simulada de los comerciantes).
- **Estimación:** 10 h-p
- **Incertidumbre:** Baja
- **Predecesores:** US-010
- **Plan inicial:** IT-004 (Sprint 4)
- **Responsable:** Equipo (Justo Cilleros 5 h / Manuel Carvajal 5 h)
- **Tarifa Media / Coste Total:** 30 €/h | 300,00 €

### Criterios de aceptación
- **US-013-AC-01:** El panel del proveedor muestra el listado cronológico de operaciones de venta simuladas de sus artículos con fecha, producto, unidades, importe total (€) y festival asociado.
- **US-013-AC-02:** Incluye un resumen superior con el total de unidades vendidas, ingresos brutos simulados (€) y el artículo más vendido del proveedor.
- **US-013-AC-03:** Permite filtrar el reporte por festival y por rango de fechas, mostrando un estado vacío informativo si no existen registros en ese periodo.

### Verificación y restricciones
- **Reglas de Negocio:** Un proveedor únicamente puede visualizar las métricas y operaciones correspondientes a sus propios artículos.
- **Restricciones:** Los importes mostrados tienen carácter informativo y simulado, sin validez tributaria (exclusión `EX-02`).
- **Requisitos No Funcionales (RNF):** Tiempo de generación de la consulta del reporte < 500 ms para historiales de hasta 5.000 registros.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* El proveedor filtra por "Subsonic RockFest": visualiza 45 camisetas vendidas y un total acumulado de 900,00 € simulados.
  * *Caso Límite:* Proveedor recién registrado sin ventas realizadas: los contadores muestran `0` y el mensaje "Aún no se registran ventas para tus artículos".
- **Supuestos:** Los datos de ventas provienen de las reservas simuladas generadas sobre el catálogo de `US-010`.

---

## US-012 — Panel e historial de participación en festivales

- **Necesidad:** Permitir a los proveedores consultar el registro histórico de los festivales y recintos en los que han participado o reservado espacios.
- **Objetivo:** Implementar una vista de historial de participaciones y reservas de recintos para el rol Proveedor.
- **Historia de Usuario:** Como Proveedor, quiero consultar el historial de festivales en los que he participado con mis recintos, para llevar un control de mi actividad histórica.
- **Tipo:** Funcional
- **Prioridad:** Could (Funcionalidad de consulta complementaria que no bloquea las operaciones de venta activa).
- **Estimación:** 8 h-p
- **Incertidumbre:** Baja
- **Predecesores:** US-009
- **Plan inicial:** IT-006 (Sprint 6)
- **Responsable:** Equipo (Justo Cilleros 4 h / Álvaro Martín 4 h)
- **Tarifa Media / Coste Total:** 30 €/h | 240,00 €

### Criterios de aceptación
- **US-012-AC-01:** El proveedor dispone de una sección "Mis Participaciones" que lista todos los festivales (pasados y activos) donde tiene o ha tenido espacios reservados, indicando fechas, recinto, ubicación del espacio y estado (`Finalizado`, `Activo`, `Cancelado`).
- **US-012-AC-02:** Permite filtrar el historial por año y por estado de la participación.
- **US-012-AC-03:** Al seleccionar una participación, muestra el detalle del espacio asignado y el resumen de actividad vinculada a ese festival.

### Verificación y restricciones
- **Reglas de Negocio:** Las participaciones en festivales cuya fecha de finalización ya ha vencido se marcan automáticamente como `Finalizado` en modo de solo lectura.
- **Restricciones:** Acceso restringido exclusivamente al proveedor titular de las reservas o a un usuario `Admin`.
- **Requisitos No Funcionales (RNF):** Paginación de resultados de 20 elementos por página.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Consulta de participaciones del año 2026: lista los 3 festivales donde el proveedor reservó stand mediante `US-009`.
  * *Caso Límite:* Proveedor sin reservas históricas ni activas: muestra el mensaje "Todavía no tienes participaciones registradas en festivales" y un enlace al buscador de recintos (`US-009`).
- **Supuestos:** Se apoya en el modelo de datos de reservas de espacios creado en `US-009`.