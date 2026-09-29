# Constitution.md

## Principios generales (Core Principles)
1. **Especificación y trazabilidad:** Toda funcionalidad del sistema de gestión de aforos y compra de entradas debe estar especificada y justificada antes de escribirse el código. 
2. **Disciplina del MVP:** El equipo se centrará en desarrollar el flujo esencial de compra y validación de entradas. Cualquier funcionalidad extra será documentada y evaluada antes de añadirse.
3. **Calidad y comportamiento verificable:** Ninguna tarea se considerará terminada solo porque el código compile. Debe cumplir con la Definición de Terminado (DoD), incluir manejo de errores y pruebas.
4. **Seguridad y uso de datos sintéticos:** El sistema tratará exclusivamente con datos ficticios de clientes y eventos. Queda terminantemente prohibido el uso de tarjetas bancarias o datos personales reales.
5. **Usabilidad y Accesibilidad:** La experiencia de compra de entradas debe ser sencilla, intuitiva y rápida, garantizando que los mensajes de error sean claros para el comprador.

## Reglas de documentación
* Cada artefacto tiene una responsabilidad: `spec.md` (explica qué se necesita), `plan.md` (explica cómo se abordará técnicamente) y `tasks.md` (descompone el trabajo ejecutable).
* Toda decisión técnica relevante debe registrarse explícitamente.

## Control de calidad

Antes de aprobar cualquier modificación sobre el proyecto, se deben comprobar los siguientes aspectos para asegurar la calidad del mismo:

- Cumple con los principios de esta constitución.
- Respeta el alcance acordado para el producto.
- No contiene decisiones relevantes sin justificar.
- Mantiene un estándar de calidad: El código es comprobado y funcional.
- Respeta la trazabilidad del producto.

## Gobierno

La constitución tendrá prioridad sobre el resto de documentos de este proyecto. Cualquier modificación sobre el proyecto deberá:

- Tener causa justificada.
- Ser aprobada por (al menos) un miembro del equipo.
- Registrar la fecha de modificación y nueva versión.
- Indicar objetos afectados por la modificación.

Se permiten excepciones, pero para ello se pide que sean explícitas, justificadas debidamente. Además, deben ser aprobadas  y de carácter temporal en la medida de lo posible.
