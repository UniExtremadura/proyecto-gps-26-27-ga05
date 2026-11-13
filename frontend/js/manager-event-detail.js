/** Crear/editar/ver un evento desde el panel de gestor. */
(function () {
    function escapeHtml(value) {
        return String(value ?? '')
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#039;');
    }

    function getParam(name) {
        const hash = String(globalThis.location.hash || '');
        const hashQuery = hash.includes('?') ? hash.split('?')[1] : '';
        return new URLSearchParams(hashQuery).get(name)
            || new URLSearchParams(globalThis.location.search).get(name)
            || '';
    }

    function setStatus(message, isError = false) {
        const node = document.getElementById('eventDetailStatus');
        if (!node) return;
        node.textContent = message || '';
        node.classList.toggle('error', isError);
        node.classList.toggle('success', !isError && Boolean(message));
    }

    function fill(event) {
        const mapping = {
            eventDetailName: event.name || event.title || '',
            eventDetailDate: event.date || '',
            eventDetailLocation: event.location || event.loc || '',
            eventDetailPrice: event.ticket_price ?? event.price ?? 0,
            eventDetailTickets: event.available_tickets ?? event.capacity ?? 0,
            eventDetailDescription: event.description || '',
            eventDetailGenre: event.genre || ''
        };
        Object.entries(mapping).forEach(([id, value]) => {
            const field = document.getElementById(id);
            if (field) field.value = value;
        });
        const title = document.getElementById('eventDetailTitle');
        if (title) title.textContent = event.name || event.title || 'Evento';
    }

    async function load() {
        const form = document.getElementById('eventDetailForm');
        if (!form) return;
        const id = getParam('id');
        const mode = getParam('mode') || (id ? 'view' : 'add');
        const idField = document.getElementById('eventDetailId');
        if (idField) idField.value = id;
        const deleteButton = document.getElementById('eventDetailDelete');
        if (deleteButton) deleteButton.classList.toggle('hidden', !id);
        const submitButton = document.getElementById('eventDetailSubmit');
        if (submitButton) submitButton.textContent = id ? 'GUARDAR CAMBIOS' : 'CREAR EVENTO';

        if (!id) return;
        try {
            const response = await globalThis.SubsonicAPI.getEvent(id);
            fill(response?.data || {});
            if (mode === 'view') {
                form.querySelectorAll('input, textarea, select').forEach((field) => { field.disabled = true; });
                if (submitButton) submitButton.classList.add('hidden');
            }
        } catch (error) {
            setStatus(error.message || 'No se pudo cargar el evento.', true);
        }
    }

    async function save(event) {
        event?.preventDefault?.();
        const id = document.getElementById('eventDetailId')?.value.trim();
        const payload = {
            name: document.getElementById('eventDetailName')?.value.trim(),
            date: document.getElementById('eventDetailDate')?.value,
            location: document.getElementById('eventDetailLocation')?.value.trim(),
            genre: document.getElementById('eventDetailGenre')?.value.trim(),
            ticket_price: Number(document.getElementById('eventDetailPrice')?.value || 0),
            available_tickets: Number(document.getElementById('eventDetailTickets')?.value || 0),
            description: document.getElementById('eventDetailDescription')?.value.trim()
        };
        if (!payload.name || !payload.date || !payload.location) {
            setStatus('Nombre, fecha y ubicación son obligatorios.', true);
            return;
        }
        try {
            setStatus('Guardando...');
            if (id) await globalThis.SubsonicAPI.updateEvent(id, payload);
            else await globalThis.SubsonicAPI.createEvent(payload);
            setStatus(id ? 'Evento actualizado.' : 'Evento creado.');
            globalThis.setTimeout(() => {
                globalThis.location.hash = '#manager-events';
                globalThis.location.reload();
            }, 700);
        } catch (error) {
            setStatus(error.message || 'No se pudo guardar el evento.', true);
        }
    }

    async function remove() {
        const id = document.getElementById('eventDetailId')?.value.trim();
        if (!id) return;
        if (!await globalThis.showSubsonicConfirm('¿Eliminar este evento?', { danger: true, confirmText: 'Eliminar' })) return;
        try {
            await globalThis.SubsonicAPI.deleteEvent(id);
            globalThis.location.hash = '#manager-events';
            globalThis.location.reload();
        } catch (error) {
            setStatus(error.message || 'No se pudo eliminar el evento.', true);
        }
    }

    function bind() {
        if (!document.getElementById('eventDetailForm')) return;
        document.getElementById('eventDetailForm').addEventListener('submit', save);
        document.getElementById('eventDetailDelete')?.addEventListener('click', remove);
        load();
    }

    globalThis.load_manager_event_detail = bind;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bind);
    } else {
        bind();
    }
})();
