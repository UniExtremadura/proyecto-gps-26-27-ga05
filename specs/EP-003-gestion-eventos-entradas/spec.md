# EP-003 — Gestión de Eventos y Entradas

## US-009 — Publicación y gestión de eventos y entradas

* **Necesidad:** Permitir a las empresas promotoras y organizadoras de eventos crear, configurar y comercializar sus festivales y modalidades de entradas.
* **Objetivo:** Proporcionar un panel de gestión (*backoffice*) para Organizadores.
* **Historia de Usuario:** Como Organizador de eventos, quiero publicar y gestionar mis festivales definiendo fechas, recintos y tipos de entradas (General, VIP), para ponerlas a la venta en la plataforma.
* **Prioridad:** Must
* **Estimación:** 18 h-p
* **Incertidumbre:** Media
* **Predecesores:** US-002
* **Plan inicial:** IT-001 (Sprint 1)

### Criterios de aceptación
* **US-009-AC-01:** Asistente de creación (*wizard*) de eventos: Datos generales -> Cartelera -> Recinto -> Tipos de Entrada.
* **US-009-AC-02:** Configuración de modalidades de entrada especificando nombre, precio (€), aforo total asignado y límite de compra por usuario.
* **US-009-AC-03 (Máquina de estados y autorización):** Transiciones de estado del festival ("Borrador" -> "Publicado" -> "Pausado"). Solo el usuario organizador propietario del evento o un Administrador están autorizados a modificar el estado o contenido. Un festival en estado "Publicado" no puede revertirse a "Borrador" si ya registra entradas vendidas.
* **US-009-AC-04 (Control de aforo):** La suma del aforo asignado a las modalidades de entrada no puede superar la capacidad máxima autorizada del recinto ni ser igual a cero.
* **US-009-AC-05 (Manejo de errores de validación):** El sistema rechaza fechas inconsistentes (fecha de fin anterior a inicio, fechas pasadas) o duplicidad en los nombres de modalidades de entrada, devolviendo una respuesta HTTP `400 Bad Request` y detallando el error en el formulario.

### Verificación y restricciones
* **Reglas de Negocio:** Un organizador solo puede consultar y editar eventos de los que sea propietario.
* **Restricciones:** El precio mínimo por entrada es 0,00 € (entradas gratuitas) y el máximo 5.000,00 €.
* **Requisitos No Funcionales (RNF):** Garantizar transacciones ACID al guardar o modificar entradas para evitar problemas de sobreventa (*overbooking*).
* **Ejemplos y Casos Límite:**
  * *Ejemplo:* Alta de "Festiverano": 5.000 entradas Generales a 30 € y 500 VIP a 80 €. Se valida contra el aforo de 5.500 del recinto y se publica.
  * *Caso Límite:* Intento de publicar un festival sin haber añadido al menos un tipo de entrada: el sistema muestra "Debes configurar al menos una entrada antes de publicar".
  * *Caso Límite:* Intento de exceder la capacidad del recinto: el sistema bloquea el guardado advirtiendo "El aforo total de las entradas excede la capacidad máxima del recinto".
* **Supuestos:** Se asume que el recinto seleccionado ha sido previamente registrado y aprobado en el catálogo de espacios.