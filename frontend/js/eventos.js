/** Catálogo público de festivales y compra de entradas. */
(function () {
    let events = [];

    function escapeHtml(value) {
        return String(value ?? '')
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#039;');
    }

    function formatDate(value) {
        if (!value) return 'Fecha por confirmar';
        const date = new Date(`${value}T00:00:00`);
        if (Number.isNaN(date.getTime())) return value;
        return date.toLocaleDateString('es-ES', { day: '2-digit', month: 'long', year: 'numeric' });
    }

    function getTicketPrice(event) {
        const price = event.ticket_price ?? event.price ?? event.prices?.general ?? 0;
        return Number(price) || 0;
    }

    function getImage(event) {
        return event.image || event.cardImg || event.heroImg || event.image_url || '';
    }

    function render() {
        const grid = document.getElementById('eventsGrid');
        if (!grid) return;

        const search = String(document.getElementById('eventsSearch')?.value || '').toLowerCase().trim();
        const genre = String(document.getElementById('eventsGenre')?.value || '').toLowerCase().trim();

        const filtered = events.filter((event) => {
            const haystack = [
                event.name, event.title, event.location, event.loc, event.description, event.genre
            ].join(' ').toLowerCase();
            const matchSearch = !search || haystack.includes(search);
            const matchGenre = !genre || String(event.genre || '').toLowerCase().includes(genre);
            return matchSearch && matchGenre;
        });

        if (!filtered.length) {
            grid.innerHTML = '<p class="empty-state">No hay festivales que coincidan con la búsqueda.</p>';
            return;
        }

        grid.innerHTML = filtered.map((event) => {
            const id = String(event.id || '');
            const name = event.name || event.title || 'Festival';
            const image = getImage(event);
            const price = getTicketPrice(event);
            const soldOut = Number(event.available_tickets ?? 1) <= 0;
            return `
                <article class="event-card">
                    <div class="event-image">
                        ${image ? `<img src="${escapeHtml(image)}" alt="${escapeHtml(name)}" loading="lazy">` : '<span class="event-image-fallback">🎪</span>'}
                    </div>
                    <div class="event-body">
                        <span class="event-genre">${escapeHtml(event.genre || 'Festival')}</span>
                        <h3 class="event-name">${escapeHtml(name)}</h3>
                        <p class="event-location">📍 ${escapeHtml(event.location || event.loc || 'Ubicación por confirmar')}</p>
                        <p class="event-date">📅 ${escapeHtml(formatDate(event.date))}</p>
                        <p class="event-description">${escapeHtml(event.description || '')}</p>
                        <div class="event-footer">
                            <span class="event-price">${price.toFixed(2)} €</span>
                            <button class="btn btn-primary event-buy" type="button" data-event-id="${escapeHtml(id)}" ${soldOut ? 'disabled' : ''}>
                                ${soldOut ? 'AGOTADO' : 'COMPRAR ENTRADA'}
                            </button>
                        </div>
                    </div>
                </article>
            `;
        }).join('');

        grid.querySelectorAll('.event-buy').forEach((button) => {
            button.addEventListener('click', () => addTicket(button.dataset.eventId));
        });
    }

    function addTicket(eventId) {
        const event = events.find((item) => String(item.id) === String(eventId));
        if (!event) return;

        if (typeof globalThis.ensureBuyerRole === 'function' && !globalThis.ensureBuyerRole()) {
            return;
        }

        globalThis.SubsonicCart.addItem({
            id: event.id,
            name: `Entrada: ${event.name || event.title || 'Festival'}`,
            type: 'Entrada',
            category: 'Entradas',
            price: getTicketPrice(event),
            event_id: event.id,
            event_name: event.name || event.title || '',
            image: getImage(event),
            images: getImage(event) ? [getImage(event)] : [],
            qty: 1
        });

        globalThis.alert(`Entrada para "${event.name || event.title}" añadida al carrito.`);
    }

    async function load() {
        const grid = document.getElementById('eventsGrid');
        if (!grid) return;
        grid.innerHTML = '<p class="loading-state">Cargando festivales...</p>';
        try {
            const response = await globalThis.SubsonicAPI.getAllEvents();
            events = Array.isArray(response?.data) ? response.data : [];
            render();
        } catch (error) {
            grid.innerHTML = `<p class="empty-state">No se pudieron cargar los festivales: ${escapeHtml(error.message)}</p>`;
        }

        const search = document.getElementById('eventsSearch');
        const genre = document.getElementById('eventsGenre');
        if (search && !search.dataset.bound) {
            search.dataset.bound = '1';
            search.addEventListener('input', render);
        }
        if (genre && !genre.dataset.bound) {
            genre.dataset.bound = '1';
            genre.addEventListener('change', render);
        }
    }

    globalThis.load_eventos = load;
    globalThis.load_eventosProveedor = load;
    globalThis.loadEventosPage = load;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', load);
    } else {
        load();
    }
})();
