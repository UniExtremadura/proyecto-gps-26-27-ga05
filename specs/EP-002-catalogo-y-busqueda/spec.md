# EP-002 — Descubrimiento y Catálogo de Eventos

## US-006 — Catálogo, Búsqueda y Detalle de Festivales

* **Necesidad:** Permitir a los usuarios localizar eventos de su interés y consultar la información detallada de la cartelera, fechas y recintos para tomar la decisión de compra.
* **Objetivo:** Proveer una interfaz pública de catálogo con buscador en tiempo real y vista de detalle por evento.
* **Historia de Usuario:** Como usuario (Guest o Cliente), quiero buscar festivales por nombre, fecha o artista y consultar su ficha detallada, para informarme sobre el evento y seleccionar entradas.
* **Prioridad:** Must
* **Estimación:** 14 h-p
* **Incertidumbre:** Baja
* **Predecesores:** —
* **Plan inicial:** IT-001 (Sprint 1)

### Criterios de aceptación
* **US-006-AC-01:** El catálogo muestra una parrilla interactiva con los festivales activos, indicando cartelera, fechas y recinto.
* **US-006-AC-02:** El cuadro de búsqueda filtra la lista en tiempo real por texto (nombre de festival o artista) sin recargar la página.
* **US-006-AC-03:** Al hacer clic en un festival, el sistema muestra su ficha de detalle con la cartelera completa, ubicación en mapa y botón de selección de entradas.
* **US-006-AC-04:** Si no se encuentran resultados, el sistema muestra el mensaje "No se encontraron festivales que coincidan con la búsqueda" y un botón para limpiar filtros.

### Verificación y restricciones
* **Reglas de Negocio:** Solo se muestran públicamente aquellos festivales cuyo estado sea "Publicado" y tengan fecha de finalización posterior a la fecha actual.
* **Restricciones:** Las imágenes de los carteles promocionales no deben superar los 2 MB de tamaño.
* **Requisitos No Funcionales (RNF):** Tiempo de filtrado en cliente < 100 ms (percentil p95) sobre un catálogo de hasta 500 eventos activos, verificado mediante pruebas automatizadas con k6 / Postman CLI en un entorno de pruebas local.
* **Ejemplos y Casos Límite:**
  * *Ejemplo:* Búsqueda "Rock": muestra "RockFest 2026" y oculta eventos de otros géneros.
  * *Caso Límite:* Acceso directo vía URL a un festival no publicado o cancelado: muestra una página de error 404 "Evento no disponible".
* **Supuestos:** Se asume que las imágenes están almacenadas y optimizadas a través de un servicio de almacenamiento de objetos (CDN/Cloud Storage).

---

## US-008 — Rendimiento y carga veloz de la página principal

* **Necesidad:** Minimizar la tasa de rebote y garantizar una navegación fluida incluso durante picos masivos de tráfico por lanzamiento de entradas.
* **Objetivo:** Optimizar el tiempo de carga de la página principal del catálogo para situarlo por debajo de los 2 segundos.
* **Historia de Usuario:** Como usuario, quiero que la página principal del catálogo cargue en menos de 2 segundos bajo condiciones normales, para navegar sin interrupciones ni esperas.
* **Prioridad:** Should
* **Estimación:** 16 h-p
* **Incertidumbre:** Media
* **Predecesores:** US-006
* **Plan inicial:** IT-003 (Sprint 3)

### Criterios de aceptación
* **US-008-AC-01:** La métrica *Largest Contentful Paint* (LCP) de la página de inicio es inferior a 2,0 segundos en conexiones simuladas Fast 4G, verificado mediante la herramienta Chrome DevTools / Lighthouse CLI.
* **US-008-AC-02:** Aplicación de carga diferida (*lazy loading*) para las imágenes de los festivales situados fuera del *viewport* inicial.
* **US-008-AC-03:** Implementación de caché en memoria (Redis) para el listado de festivales destacados con un tiempo de vida (TTL) de 5 minutos e invalidación automática ante cualquier modificación en el catálogo.

### Verificación y restricciones
* **Reglas de Negocio:** La caché debe invalidarse de forma inmediata si un organizador o administrador modifica un festival publicado.
* **Restricciones:** El peso total transferido en la primera carga de la página principal no debe exceder los 1.5 MB (comprimido).
* **Requisitos No Funcionales (RNF):** Obtener una puntuación de rendimiento superior a 85/100 en Google Lighthouse en entorno de pruebas local/staging.
* **Ejemplos y Casos Límite:**
  * *Ejemplo:* Entrada masiva de 100 usuarios simultáneos: la home se sirve desde caché en menos de 300 ms sin sobrecargar la base de datos.
  * *Caso Límite:* Caída del servidor de caché: el sistema realiza un *fallback* transparente consultando directamente a la base de datos sin interrumpir el servicio.
* **Supuestos:** Se asume que el servidor web soporta compresión HTTP (Gzip/Brotli) y protocolo HTTP/2.