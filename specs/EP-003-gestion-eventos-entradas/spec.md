# EP-003 — Gestión de Eventos y Entradas

## US-008 — Publicación y gestión de eventos y entradas

- **Necesidad:** Permitir a las empresas promotoras y organizadoras de eventos crear, configurar y comercializar sus festivales y modalidades de entradas sin intermediarios.
- **Objetivo:** Proporcionar un panel de gestión (*backoffice*) para Organizadores donde gestionar eventos, tipos de entrada y aforos.
- **Historia de Usuario:** Como Organizador, quiero dar de alta, editar y publicar festivales con sus diferentes tipos de entradas, para ponerlos a la venta en la plataforma.
- **Tipo:** Funcional
- **Prioridad:** Must (Funcionalidad primaria de generación de oferta de eventos. Bloquea la comercialización).
- **Estimación:** 8 h-p
- **Incertidumbre:** Media
- **Predecesores:** US-002
- **Plan inicial:** IT-002 (Sprint 2)
- **Coste Total Estimado:** 240,00 € (desglosado en tareas TK)
- **Desglose de tareas (IT-002):**
  - `TK-008-1`: Event Mgmt API — CRUD de eventos y tipos de entradas (4 h-p | Predecesor: MGT IT 2. Sprint planning, `TK-004-2` | Responsable: Jaime Arias | Tarifa: 30 €/h | Coste: 120,00 €).
  - `TK-008-2`: Event Dashboard UI — Panel de gestión para el organizador (4 h-p | Predecesor: MGT IT 2. Sprint planning | Responsable: Manuel Carvajal | Tarifa: 30 €/h | Coste: 120,00 €).

### Criterios de aceptación
- **US-008-AC-01:** Asistente de creación (*wizard*) y edición de eventos: Datos generales -> Cartelera -> Recinto -> Tipos de Entrada (General, VIP).
- **US-008-AC-02:** Configuración de modalidades de entrada especificando nombre, precio ficticio (€), aforo asignado y límite de reserva por usuario, mostrando en el panel las entradas vendidas/reservadas y disponibles.
- **US-008-AC-03 (Máquina de estados y autorización):** Transiciones de estado del festival: `Borrador` -> `Publicado` <-> `Pausado`, y desde `Publicado` o `Pausado` -> `Cancelado` (estado terminal: el festival deja de mostrarse en el catálogo y no admite nuevas reservas). Un festival `Publicado` o `Pausado` cuya fecha de fin ha vencido se considera `Finalizado` (estado derivado, de solo lectura, que tampoco admite reservas). Un festival `Publicado` o `Pausado` solo puede volver a `Borrador` si no registra reservas. Solo el usuario `Organizador` propietario del evento o un `Admin` están autorizados a modificar el estado o contenido.
- **US-008-AC-04 (Control de aforo):** La suma del aforo asignado a las modalidades de entrada no puede superar la capacidad máxima autorizada del recinto ni ser menor o igual a cero.
- **US-008-AC-05 (Manejo de errores de validación):** El sistema rechaza fechas inconsistentes (fecha de fin anterior a inicio, fechas pasadas) o nombres de entrada duplicados en el mismo festival, devolviendo HTTP `400 Bad Request` y detallando el error en el formulario.

### Verificación y restricciones
- **Reglas de Negocio:** Un organizador solo puede consultar y editar eventos de los que sea propietario.
- **Restricciones:** El precio mínimo por entrada es 0,00 € (entradas gratuitas) y el máximo 5.000,00 €. No se integran pasarelas de pago reales (reservas 100% simuladas).
- **Requisitos No Funcionales (RNF):** Garantizar transacciones atómicas (ACID) al guardar entradas y registrar reservas para evitar sobreventa (*overbooking*).
- **Ejemplos y Casos Límite:**
  * *Ejemplo:* Alta de "Festiverano": 5.000 entradas Generales a 30 € y 500 VIP a 80 €. Se valida contra el aforo de 5.500 del recinto y pasa a estado `Publicado`.
  * *Caso Límite:* Intento de publicar un festival sin haber añadido al menos un tipo de entrada: el sistema bloquea la transición e indica "Debes configurar al menos una modalidad de entrada antes de publicar".
  * *Caso Límite:* Intento de superar la capacidad del recinto: el sistema bloquea el guardado advirtiendo "El aforo total de las entradas excede la capacidad máxima del recinto".
- **Supuestos:** Se dispone de un catálogo base de recintos ficticios precargados en la base de datos.