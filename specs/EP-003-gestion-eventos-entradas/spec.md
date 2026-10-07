# EP-003 — Gestión de Eventos y Entradas

## US-009 — Publicación y gestión de eventos y entradas

* **Necesidad:** Permitir a las empresas promotoras y organizadoras de eventos crear, configurar y comercializar sus festivales y modalidades de entradas.
* **Objetivo:** Proporcionar un panel de gestión (*backoffice*) para Organizadores.
* **User Story:** Como Organizador de eventos, quiero publicar y gestionar mis festivales definiendo fechas, recintos y tipos de entradas (General, VIP), para ponerlas a la venta en la plataforma.
* **Priority:** Must
* **Estimate:** 18 h-p
* **Uncertainty:** Medium
* **Predecessors:** US-002
* **Initial plan:** IT-001 (Sprint 1)

### Acceptance criteria
* **US-009-AC-01:** Asistente de creación (*wizard*) de eventos: Datos generales -> Cartelera -> Recinto -> Tipos de Entrada.
* **US-009-AC-02:** Configuración de modalidades de entrada especificando nombre, precio (€), aforo total asignado y límite de compra por usuario.
* **US-009-AC-03:** Cambio de estado del festival de "Borrador" a "Publicado" o "Pausado".
* **US-009-AC-04:** Control de aforo: la suma de entradas creadas no puede superar la capacidad máxima autorizada del recinto seleccionado.

### Verification and constraints
* **Reglas de Negocio:** Un organizador solo puede consultar y editar eventos de los que sea propietario.
* **Restricciones:** El precio mínimo por entrada es 0.00 € (entradas gratuitas) y el máximo 5.000.00 €.
* **Requisitos No Funcionales (RNF):** Garantizar transacciones ACID al guardar o modificar entradas para evitar problemas de sobreventa (*overbooking*).
* **Ejemplos y Casos Límite:**
  * *Ejemplo:* Alta de "Festiverano": 5.000 entradas Generales a 30 € y 500 VIP a 80 €. Se valida contra el aforo de 5.500 del recinto y se publica.
  * *Caso Límite:* Intento de publicar un festival sin haber añadido al menos un tipo de entrada: el sistema muestra "Debes configurar al menos una entrada antes de publicar".
* **Supuestos:** Se asume que el recinto seleccionado ha sido previame registrado y aprobado en el catálogo de espacios.
