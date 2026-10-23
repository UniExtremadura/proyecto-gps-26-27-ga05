# EP-002 — Descubrimiento y Catálogo de Eventos

## US-006 — Catálogo, Búsqueda y Detalle de Festivales

- **Necesidad:** Permitir a los usuarios localizar eventos de su interés y consultar la información detallada de la cartelera, fechas y recintos para tomar la decisión de compra.
- **Objetivo:** Proveer una interfaz pública de catálogo con buscador en tiempo real y vista de detalle por evento.
- **Historia de Usuario:** Como usuario (Guest o Cliente), quiero ver, buscar festivales por nombre, fecha o artista y acceder a su ficha detallada, para informarme y comprar entradas.
- **Tipo:** Funcional
- **Prioridad:** Must (Core business de la plataforma; unifica la búsqueda general y el listado público. Sin catálogo no hay flujo comercial).
- **Estimación:** 14 h-p
- **Incertidumbre:** Baja
- **Predecesores:** —
- **Plan inicial:** IT-002 (Sprint 2)
- **Responsable:** Equipo (Justo Cilleros 7 h / Álvaro Martín 7 h)
- **Tarifa Media / Coste Total:** 30 €/h | 420,00 €

### Criterios de aceptación
- **US-006-AC-01:** El catálogo muestra una parrilla interactiva con los festivales activos, indicando cartelera, fechas y recinto.
- **US-006-AC-02:** El buscador permite filtrar la lista en tiempo real por texto (nombre de festival o artista) y por rango de fechas sin recargar la página.
- **US-006-AC-03:** Al hacer clic en un festival, el sistema muestra su ficha de detalle con la cartelera completa, ubicación, aforo disponible y botón de selección/reserva simulada de entradas.
- **US-006-AC-04:** Si no se encuentran resultados, el sistema muestra el mensaje "No se encontraron festivales que coincidan con la búsqueda" y un botón para limpiar filtros.

### Verificación y restricciones
- **Reglas de Negocio:** Solo se muestran públicamente aquellos festivales cuyo estado sea "Publicado" y tengan fecha de finalización igual o posterior a la fecha actual.
- **Restricciones:** Las imágenes de los carteles promocionales no deben superar los 2 MB de tamaño. Todos los eventos y artistas del catálogo son ficticios.
- **Requisitos No Funcionales (RNF):** Tiempo de filtrado < 100 ms (percentil p95) sobre un catálogo de hasta 500 eventos activos en entorno de pruebas local.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Búsqueda "Rock" o filtro por mes de julio: muestra "Subsonic RockFest 2026" y oculta los eventos que no coinciden.
  * *Caso Límite:* Acceso directo vía URL a un festival no publicado o inexistente: muestra una página de error `404` "Evento no disponible".
- **Supuestos:** Se asume que las imágenes están servidas desde almacenamiento local o estático simulado.

---

## US-007 — Rendimiento y carga veloz de la página principal

- **Necesidad:** Minimizar la tasa de rebote y garantizar una navegación fluida incluso durante picos de tráfico por lanzamiento de entradas.
- **Objetivo:** Optimizar el tiempo de carga de la página principal del catálogo para situarlo por debajo de los 2 segundos.
- **Historia de Usuario:** Como usuario, quiero que la página principal cargue en menos de 2 segundos, para disfrutar de una navegación fluida y sin retrasos.
- **Tipo:** Calidad
- **Prioridad:** Should (Mejora drásticamente la tasa de retención y conversión, previniendo el abandono de la web).
- **Estimación:** 16 h-p
- **Incertidumbre:** Media
- **Predecesores:** US-006
- **Plan inicial:** IT-006 (Sprint 6)
- **Responsable:** Equipo (Manuel Carvajal 8 h / Álvaro Martín 8 h)
- **Tarifa Media / Coste Total:** 30 €/h | 480,00 €

### Criterios de aceptación
- **US-007-AC-01:** La métrica *Largest Contentful Paint* (LCP) de la página de inicio es inferior a 2,0 segundos en perfil simulado Fast 4G, verificado mediante Chrome DevTools / Lighthouse CLI.
- **US-007-AC-02:** Aplicación de carga diferida (*lazy loading*) para las imágenes de los festivales situados fuera del *viewport* inicial.
- **US-007-AC-03:** Implementación de caché en memoria (Redis o caché en servidor) para el listado de festivales destacados con un TTL de 5 minutos e invalidación automática ante modificaciones en el catálogo.

### Verificación y restricciones
- **Reglas de Negocio:** La caché debe invalidarse inmediatamente cuando un organizador o administrador publique, edite o pause un festival.
- **Restricciones:** El peso total transferido en la primera carga de la página principal no debe exceder los 1,5 MB (comprimido).
- **Requisitos No Funcionales (RNF):** Puntuación de rendimiento (*Performance*) superior a 85/100 en Google Lighthouse sobre el entorno local/staging.
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Peticiones repetidas al listado principal: se sirven desde caché en menos de 300 ms sin realizar consultas redundantes a la base de datos.
  * *Caso Límite:* Caída o indisponibilidad del servicio de caché: el sistema realiza *fallback* transparente consultando la base de datos sin interrumpir el servicio.
- **Supuestos:** El servidor web soporta compresión HTTP (Gzip/Brotli).