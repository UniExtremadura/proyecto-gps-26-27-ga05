# Definition of Done (DoD) — Web Solutions SL

## 1. Propósito
El **Definition of Done (DoD)** es el conjunto de criterios técnicos, de calidad y de proceso que debe satisfacer obligatoriamente cualquier Historia de Usuario (`US-XXX`) para considerarse **100% completada** y lista para ser integrada en la rama principal (`main`) de forma segura.

Garantiza que el entregable cumple con los estándares exigidos por **Web Solutions SL**, asegurando la estabilidad del sistema y el cumplimiento de los acuerdos del *Team Charter*.

---

## 2. Lista de Comprobación (Checklist de DoD)

Una Historia de Usuario solo se marcará como **Done / Finalizada** cuando cumpla el 100% de los siguientes puntos:

### A. Implementación y Estándares de Código
- [ ] **Desarrollo Completo:** La funcionalidad descrita en la Historia de Usuario se ha codificado por completo según las especificaciones técnicas.
- [ ] **Estándares de Limpieza:** El código sigue las convenciones de estilo del proyecto, está libre de código muerto, comentarios innecesarios o credenciales expuestas en texto plano.

### B. Criterios de Aceptación y Pruebas
- [ ] **Verificación de Criterios (AC):** Se han probado y validado exitosamente todos y cada uno de los criterios de aceptación (`US-XXX-AC-YY`).
- [ ] **Pruebas de Casos Límite:** Se han ejecutado pruebas manuales o unitarias verificando los casos de error, validaciones de formularios y límites de datos.

### C. Requisitos No Funcionales y Seguridad
- [ ] **Seguridad e Higiene:** Los datos sensibles (contraseñas, tokens) se manejan cifrados y no se muestran en logs ni respuestas insecure (cumplimiento de `US-018`).
- [ ] **Rendimiento:** El tiempo de respuesta de las vistas o endpoints desarrollados se mantiene dentro de los límites aceptables especificados (ej. < 2 segundos para la carga del catálogo).

### D. Control de Versiones e Integración (Git & GitHub)
- [ ] **Commits Limpios:** Los mensajes de commit son descriptivos y hacen referencia a la tarea correspondiente.
- [ ] **Sin Conflictos:** La rama de trabajo (`docs/hito2-requisitos` o equivalente) está sincronizada con `main` y no presenta conflictos de integración.
- [ ] **Pull Request (PR) Creada:** Se ha abierto una Pull Request formal hacia `main` en GitHub detallando los cambios introducidos.

### E. Revisión de Código y Calidad (Team Charter)
- [ ] **Peer Review Obligatoria:** La Pull Request ha sido revisada por un miembro del equipo ajeno al autor de los cambios.
- [ ] **Aprobación de Roles Clave:** Se cuenta con la aprobación explícita (*Approved*) en GitHub por parte del Tech Lead (Álvaro Martín) o del DevOps/QA (Manuel Carvajal).
- [ ] **Fusión a Main:** La PR se ha fusionado (*Merged*) correctamente en la rama `main` y la rama secundaria se ha eliminado/cerrado.

### F. Documentación
- [ ] **Actualización de Especificaciones:** Se ha actualizado el archivo `spec.md` correspondiente dentro de `specs/product/EP-XXX/` si durante el desarrollo surgieron ajustes o aclaraciones técnicas.

---

## 3. Flujo de Trabajo para Fusión y Cierre (Mermaid)

```mermaid
graph TD
    A[Desarrollo Completado en Rama] --> B[Ejecución y Verificación de Pruebas / ACs]
    B --> C[Apertura de Pull Request en GitHub]
    C --> D[Revisión por Peer / Tech Lead / QA]
    D -->|Requiere Cambios / Errores| A
    D -->|Aprobado por Revisores| E[Merge a la Rama Main]
    E --> F[Marcar Historia como Done]
