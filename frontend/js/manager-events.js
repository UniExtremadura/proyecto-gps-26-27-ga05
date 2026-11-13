// Manager Events Panel Logic (Firebase-backed)

const artists = [
    { id: 1, name: 'DJ Voltage', photo: '' },
    { id: 2, name: 'Neon Shadow', photo: '' },
    { id: 3, name: 'The Glitch', photo: '' }
];

globalThis.artists = artists;

let events = [];
globalThis.events = events;

/* ===== VARIABLES DE FILTRO (igual que eventos.js) ===== */
let allEvents = []; // Alias para usar la lógica de filtros de eventos.js
let searchNameFilter = ""; // Búsqueda por nombre desde navbar
let selectedCities = [];
let dateStart = null;
let dateEnd = null;

const recognizedCities = [
    "Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Málaga",
    "Zaragoza", "Córdoba", "Valladolid", "Alicante", "Toledo", "Granada",
    "Cuenca", "Salamanca", "Cádiz", "Oviedo", "Murcia", "Palma", "Ibiza",
    "París", "Londres", "Berlín", "Ámsterdam", "Milán", "Roma", "Venecia",
    "Estocolmo", "Copenhague", "Viena", "Praga", "Varsovia", "Bruselas",
    "Zúrich", "Ginebra", "Estambul", "Atenas", "Barcelona", "Lisboa",
    "Nueva York", "Los Ángeles", "Chicago", "Miami", "San Francisco", "Boston",
    "Tokio", "Osaka", "Kioto", "Bangkok", "Singapur", "Hong Kong",
    "Sydney", "Melbourne", "Sídney", "Dubái", "Abu Dabi", "Tel Aviv",
    "Estambul", "Bangkok", "Manila", "Kuala Lumpur", "Ciudad de México",
    "Toronto", "Vancouver", "Montréal", "São Paulo", "Río de Janeiro",
    "Buenos Aires", "Santiago", "Lima", "Bogotá", "Cartagena"
].sort();

function normalizeManagerEvent(ev) {
    return {
        id: String(ev.id || ''),
        name: ev.name || ev.title || ev.artist || 'Evento sin nombre',
        type: ev.type || 'Evento',
        status: ev.status || 'BORRADOR',
        location: ev.location || ev.loc || '',
        date: ev.date || '',
        capacity: Number(ev.capacity || ev.available_tickets || 0),
        attending: Number(ev.attending || 0),
        heroImg: ev.heroImg || ev.image || ev.image_url || '',
        cardImg: ev.cardImg || ev.image || ev.image_url || '',
        description: ev.description || '',
        isMultiDay: Boolean(ev.isMultiDay),
        prices: ev.prices || { general: Number(ev.ticket_price || 0), vip: 0, camping: 0 },
        lineup: Array.isArray(ev.lineup) ? ev.lineup : [],
        providerInfo: ev.providerInfo || '',
        map_config: ev.map_config || null,
        slots: Array.isArray(ev.slots) ? ev.slots : []
    };
}

async function loadManagerEvents() {
    try {
        const response = await SubsonicAPI.getAllEvents();
        const apiEvents = Array.isArray(response.data) ? response.data : [];
        events = apiEvents.map(normalizeManagerEvent);
    } catch (error) {
        console.error('No se pudieron cargar eventos para gestor:', error);
        events = [];
    }
    globalThis.events = events;
}

/* ===== FUNCIONES DE FILTRADO (copiadas de eventos.js) ===== */

function parseDate(dateStr) {
    if (!dateStr) return null;
    const [year, month, day] = dateStr.split('-');
    return new Date(year, month - 1, day);
}

function getEventDate(event) {
    if (event.date) {
        const parts = event.date.split('-');
        if (parts.length === 3) {
            return new Date(parts[2], parts[1] - 1, parts[0]);
        }
    }
    if (event.start_date) {
        return parseDate(event.start_date);
    }
    return null;
}

function filterManagerEvents() {
    return allEvents.filter(function (ev) {
        // Filtro de nombre (búsqueda desde navbar)
        let matchName = true;
        if (searchNameFilter.trim().length > 0) {
            const eventName = (ev.name || ev.title || ev.artist || "").toLowerCase();
            matchName = eventName.startsWith(searchNameFilter.toLowerCase());
        }

        let matchCity = selectedCities.length === 0;
        if (!matchCity) {
            const eventCity = (ev.location || ev.loc || "").toLowerCase();
            matchCity = selectedCities.some(city => eventCity.includes(city.toLowerCase()));
        }
        
        let matchDate = true;
        if (dateStart || dateEnd) {
            const eventDate = getEventDate(ev);
            if (eventDate) {
                if (dateStart) matchDate = matchDate && eventDate >= dateStart;
                if (dateEnd) matchDate = matchDate && eventDate <= dateEnd;
            } else {
                matchDate = false;
            }
        }
        
        return matchName && matchCity && matchDate;
    });
}

function updateActiveFiltersDisplay() {
    const container = document.getElementById('activeFiltersDisplay');
    if (!container) return;
    
    const filters = [];
    
    if (dateStart || dateEnd) {
        const startStr = dateStart ? dateStart.toLocaleDateString('es-ES') : '...';
        const endStr = dateEnd ? dateEnd.toLocaleDateString('es-ES') : '...';
        filters.push({
            text: `📅 ${startStr} → ${endStr}`,
            type: 'date'
        });
    }
    
    selectedCities.forEach(city => {
        filters.push({
            text: `🏙️ ${city}`,
            type: 'city',
            value: city
        });
    });

    // Agregar filtro de nombre si existe
    if (searchNameFilter.trim().length > 0) {
        filters.push({
            text: `📝 ${searchNameFilter}`,
            type: 'name'
        });
    }
    
    if (filters.length === 0) {
        container.innerHTML = '<span class="no-filters-text">Sin filtros aplicados</span>';
    } else {
        container.innerHTML = filters.map(f => {
            if (f.type === 'date') {
                return `<div class="filter-tag">${f.text} <span class="filter-tag-remove" onclick="clearDateFilter()">×</span></div>`;
            } else if (f.type === 'name') {
                return `<div class="filter-tag">${f.text} <span class="filter-tag-remove" onclick="clearNameFilter()">×</span></div>`;
            } else {
                return `<div class="filter-tag">${f.text} <span class="filter-tag-remove" onclick="removeCityFilter('${f.value}')">×</span></div>`;
            }
        }).join('');
    }
}

function clearDateFilter() {
    dateStart = null;
    dateEnd = null;
    document.getElementById('dateStart').value = '';
    document.getElementById('dateEnd').value = '';
    updateActiveFiltersDisplay();
    populateEvents();
}

function removeCityFilter(city) {
    selectedCities = selectedCities.filter(c => c !== city);
    renderSelectedCities();
    updateActiveFiltersDisplay();
    populateEvents();
}

function clearNameFilter() {
    searchNameFilter = "";
    updateActiveFiltersDisplay();
    populateEvents();
}

function renderSelectedCities() {
    const container = document.getElementById('selectedCities');
    if (!container) return;
    
    if (selectedCities.length === 0) {
        container.innerHTML = '';
    } else {
        container.innerHTML = selectedCities.map(city => 
            `<div class="city-chip">🏙️ ${city} <span class="city-chip-remove" onclick="removeCityFilter('${city}')">×</span></div>`
        ).join('');
    }
}

function updateCitySuggestions(query) {
    const container = document.getElementById('citySuggestions');
    if (!container) return;
    
    if (query.trim().length === 0) {
        container.style.display = 'none';
        return;
    }
    
    const qLower = query.toLowerCase();
    const filtered = recognizedCities.filter(city => 
        city.toLowerCase().includes(qLower) && !selectedCities.includes(city)
    );
    
    if (filtered.length === 0) {
        container.style.display = 'none';
    } else {
        container.innerHTML = filtered.map(city => 
            `<div class="city-suggestion-item" onclick="selectCity('${city}')">${city}</div>`
        ).join('');
        container.style.display = 'block';
    }
}

function selectCity(city) {
    if (!selectedCities.includes(city)) {
        selectedCities.push(city);
    }
    document.getElementById('citySearch').value = '';
    updateCitySuggestions('');
    renderSelectedCities();
    updateActiveFiltersDisplay();
    populateEvents();
}

function setupFilters() {
    const dateStartInput = document.getElementById('dateStart');
    const dateEndInput = document.getElementById('dateEnd');
    const citySearchInput = document.getElementById('citySearch');
    const clearAllBtn = document.getElementById('clearAllFilters');
    
    if (dateStartInput && !dateStartInput.dataset.bound) {
        dateStartInput.dataset.bound = '1';
        dateStartInput.addEventListener('change', function () {
            dateStart = this.value ? parseDate(this.value) : null;
            updateActiveFiltersDisplay();
            populateEvents();
        });
    }
    
    if (dateEndInput && !dateEndInput.dataset.bound) {
        dateEndInput.dataset.bound = '1';
        dateEndInput.addEventListener('change', function () {
            dateEnd = this.value ? parseDate(this.value) : null;
            updateActiveFiltersDisplay();
            populateEvents();
        });
    }
    
    if (citySearchInput && !citySearchInput.dataset.bound) {
        citySearchInput.dataset.bound = '1';
        citySearchInput.addEventListener('input', function () {
            updateCitySuggestions(this.value);
        });
        
        citySearchInput.addEventListener('blur', () => {
            setTimeout(() => {
                document.getElementById('citySuggestions').style.display = 'none';
            }, 200);
        });
    }
    
    if (clearAllBtn && !clearAllBtn.dataset.bound) {
        clearAllBtn.dataset.bound = '1';
        clearAllBtn.addEventListener('click', function () {
            selectedCities = [];
            dateStart = null;
            dateEnd = null;
            searchNameFilter = "";
            
            if (dateStartInput) dateStartInput.value = '';
            if (dateEndInput) dateEndInput.value = '';
            if (citySearchInput) citySearchInput.value = '';
            
            renderSelectedCities();
            updateActiveFiltersDisplay();
            populateEvents();
        });
    }
    
    updateActiveFiltersDisplay();
    renderSelectedCities();
}

document.addEventListener('DOMContentLoaded', async function () {
    const user = AUTH.getUser();
    if (user?.role !== 'gestor') {
        globalThis.location.hash = 'login';
        return;
    }

    // Aplicar búsqueda desde navbar si existe
    const savedSearch = sessionStorage.getItem('eventSearchQuery');
    if (savedSearch) {
        searchNameFilter = savedSearch;
        sessionStorage.removeItem('eventSearchQuery');
    }

    await loadManagerEvents();
    allEvents = events; // Sincronizar para usar lógica de filtros
    setupFilters(); // Configurar filtros
    populateEvents();

    const newEventBtn = document.querySelector('.btn-new-event');
    if (newEventBtn && !newEventBtn.dataset.bound) {
        newEventBtn.dataset.bound = '1';
        newEventBtn.addEventListener('click', createNewEvent);
    }
});

function populateEvents() {
    const grid = document.getElementById('eventsGrid');
    if (!grid) return;

    const filteredEvents = filterManagerEvents();

    if (!filteredEvents.length) {
        grid.innerHTML = '<p style="grid-column:1/-1;text-align:center;padding:2rem;color:#94a3b8;">No hay eventos que coincidan con los filtros.</p>';
        return;
    }

    grid.innerHTML = filteredEvents.map((eventItem) => {
        const encodedId = encodeURIComponent(String(eventItem.id));
        return `
        <div class="event-card" data-event-id="${encodedId}">
            <div class="event-image">
                ${eventItem.cardImg ? `<img src="${eventItem.cardImg}" alt="${eventItem.name}">` : 'Sin imagen'}
            </div>
            <div class="event-header">
                <span class="status-badge ${getStatusClass(eventItem.status)}">${eventItem.status}</span>
            </div>
            <div class="event-body">
                <h3 class="event-name">${eventItem.name}</h3>
                ${eventItem.lineup?.length ? `<p class="event-headliner">Artista: ${getArtistName(eventItem.lineup[0])}</p>` : ''}
                <div class="event-details">
                    <p class="event-location">📍 ${eventItem.location}</p>
                    <p class="event-date">📅 ${formatDate(eventItem.date)}</p>
                    <p class="event-capacity">👥 ${eventItem.attending}/${eventItem.capacity} asistentes</p>
                </div>
                <div class="event-actions">
                    <button class="btn-modify" data-action="modify" data-event-id="${encodedId}" type="button">MODIFICAR</button>
                    <button class="btn-delete" data-action="delete" data-event-id="${encodedId}" type="button">ELIMINAR</button>
                </div>
            </div>
        </div>
    `;
    }).join('');

    if (!grid.dataset.boundClicks) {
        grid.dataset.boundClicks = '1';
        grid.addEventListener('click', (domEvent) => {
            const actionButton = domEvent.target.closest('button[data-action]');
            if (actionButton && grid.contains(actionButton)) {
                domEvent.stopPropagation();
                const id = decodeURIComponent(actionButton.dataset.eventId || '');
                const action = actionButton.dataset.action;
                if (!id) return;

                if (action === 'modify') {
                    modifyEventById(id);
                    return;
                }
                if (action === 'delete') {
                    deleteEventById(id);
                }
                return;
            }

            const card = domEvent.target.closest('.event-card[data-event-id]');
            if (!card || !grid.contains(card)) return;
            const id = decodeURIComponent(card.dataset.eventId || '');
            if (!id) return;
            viewEventDetail(id);
        });
    }
}

async function askConfirm(message, options) {
    ensureConfirmStyles();

    if (typeof globalThis.showSubsonicConfirm === 'function') {
        try {
            return await globalThis.showSubsonicConfirm(message, options);
        } catch (error) {
            console.warn('Modal global no disponible, usando modal local:', error);
        }
    }

    return new Promise((resolve) => {
        const {
            title = 'Confirmar accion',
            confirmText = 'Confirmar',
            cancelText = 'Cancelar',
            danger = false
        } = options || {};

        const existing = document.getElementById('subsonicConfirmOverlayLocal');
        if (existing) existing.remove();

        const overlay = document.createElement('div');
        overlay.id = 'subsonicConfirmOverlayLocal';
        overlay.className = 'subsonic-confirm-overlay';
        overlay.innerHTML = `
            <div class="subsonic-confirm-modal" role="dialog" aria-modal="true" aria-labelledby="subsonicConfirmLocalTitle">
                <h3 id="subsonicConfirmLocalTitle">${title}</h3>
                <p>${message}</p>
                <div class="subsonic-confirm-actions">
                    <button type="button" class="subsonic-confirm-btn subsonic-confirm-cancel">${cancelText}</button>
                    <button type="button" class="subsonic-confirm-btn ${danger ? 'subsonic-confirm-danger' : 'subsonic-confirm-ok'}">${confirmText}</button>
                </div>
            </div>
        `;

        const close = (result) => {
            if (!overlay.isConnected) return;
            document.removeEventListener('keydown', onKeyDown);
            overlay.remove();
            resolve(result);
        };

        const onKeyDown = (event) => {
            if (event.key === 'Escape') close(false);
        };

        overlay.addEventListener('click', (event) => {
            if (event.target === overlay) close(false);
        });

        const cancelBtn = overlay.querySelector('.subsonic-confirm-cancel');
        const okBtn = overlay.querySelector('.subsonic-confirm-ok, .subsonic-confirm-danger');
        cancelBtn?.addEventListener('click', () => close(false));
        okBtn?.addEventListener('click', () => close(true));

        document.addEventListener('keydown', onKeyDown);
        document.body.appendChild(overlay);
        okBtn?.focus();
    });
}

function ensureConfirmStyles() {
    if (document.getElementById('subsonicConfirmRuntimeStyles')) return;

    const style = document.createElement('style');
    style.id = 'subsonicConfirmRuntimeStyles';
    style.textContent = `
        .subsonic-confirm-overlay {
            position: fixed !important;
            inset: 0 !important;
            z-index: 99999 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 20px !important;
            background: rgba(1, 8, 20, 0.74) !important;
            backdrop-filter: blur(3px);
            animation: confirmFadeIn .18s ease-out;
        }
        .subsonic-confirm-modal {
            width: min(560px, 100%) !important;
            background: linear-gradient(155deg, #12182a 0%, #0a1020 100%) !important;
            border: 1px solid rgba(0, 212, 255, 0.35) !important;
            border-radius: 14px !important;
            padding: 24px !important;
            box-shadow: 0 22px 55px rgba(0, 0, 0, 0.55) !important;
            animation: confirmPop .2s ease-out;
        }
        .subsonic-confirm-modal h3 {
            margin: 0 0 10px !important;
            color: #64e8ff !important;
            font-size: 1.15rem !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            letter-spacing: .06em;
        }
        .subsonic-confirm-modal p {
            margin: 0 !important;
            color: #e2ecff !important;
            line-height: 1.5 !important;
            font-size: 1.02rem !important;
        }
        .subsonic-confirm-actions {
            margin-top: 18px !important;
            display: flex !important;
            justify-content: flex-end !important;
            gap: 10px !important;
        }
        .subsonic-confirm-btn {
            border-radius: 10px !important;
            border: 1px solid transparent !important;
            padding: 10px 16px !important;
            font-size: .92rem !important;
            font-weight: 700 !important;
            cursor: pointer !important;
        }
        .subsonic-confirm-cancel {
            background: rgba(148, 163, 184, 0.15) !important;
            border-color: rgba(148, 163, 184, 0.45) !important;
            color: #e2e8f0 !important;
        }
        .subsonic-confirm-ok {
            background: linear-gradient(135deg, #06b6d4, #0284c7) !important;
            color: #f8fafc !important;
        }
        .subsonic-confirm-danger {
            background: linear-gradient(135deg, #ef4444, #dc2626) !important;
            color: #fff !important;
        }
        @keyframes confirmFadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes confirmPop {
            from { opacity: 0; transform: translateY(10px) scale(.98); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
    `;
    document.head.appendChild(style);
}

function getArtistName(lineupItem) {
    if (!lineupItem) return 'N/D';
    if (lineupItem.name) return lineupItem.name;
    if (lineupItem.role) return lineupItem.role;
    return 'N/D';
}

function getStatusClass(status) {
    switch (status) {
        case 'PUBLICADO':
            return 'status-published';
        case 'BORRADOR':
            return 'status-draft';
        case 'CANCELADO':
            return 'status-cancelled';
        default:
            return 'status-published';
    }
}

function formatDate(dateStr) {
    if (!dateStr) return 'Sin fecha';
    const date = new Date(`${dateStr}T00:00:00`);
    if (Number.isNaN(date.getTime())) return dateStr;
    return date.toLocaleDateString('es-ES', { year: 'numeric', month: '2-digit', day: '2-digit' });
}

function modifyEventById(id) {
    globalThis.location.hash = `manager-event-detail?id=${encodeURIComponent(id)}&mode=edit`;
}

async function deleteEvent(domEvent, id) {
    if (domEvent?.stopPropagation) domEvent.stopPropagation();
    const eventToDelete = events.find((ev) => ev.id === String(id));
    if (!eventToDelete) return;

    const firstConfirm = await askConfirm(
        `¿Estas seguro de que deseas eliminar el evento "${eventToDelete.name}"?`,
        { title: 'Eliminar evento', confirmText: 'Si, continuar', cancelText: 'Cancelar', danger: true }
    );
    if (!firstConfirm) {
        return;
    }

    const secondConfirm = await askConfirm(
        'Esta accion no se puede deshacer. ¿Confirmas eliminar definitivamente este evento?',
        { title: 'Confirmacion final', confirmText: 'Eliminar', cancelText: 'Volver', danger: true }
    );
    if (!secondConfirm) {
        return;
    }

    try {
        await SubsonicAPI.deleteEvent(id);
        events = events.filter((ev) => ev.id !== String(id));
        globalThis.events = events;
        populateEvents();
        alert('Evento eliminado exitosamente');
    } catch (error) {
        console.error('Error eliminando evento:', error);
        alert('No se pudo eliminar el evento.');
    }
}

function deleteEventById(id) {
    return deleteEvent(null, id);
}

function createNewEvent() {
    globalThis.location.hash = 'manager-event-detail?mode=add';
}

function viewEventDetail(id) {
    globalThis.location.hash = `manager-event-detail?id=${encodeURIComponent(id)}&mode=view`;
}


/* ================================================================
 * TK-008-2: panel rápido de gestión de eventos
 * ================================================================ */
async function saveQuickEvent() {
    const status = document.getElementById('quickEventStatus');
    const eventId = document.getElementById('quickEventId')?.value || '';
    const payload = {
        name: document.getElementById('quickEventName')?.value.trim(),
        date: document.getElementById('quickEventDate')?.value,
        location: document.getElementById('quickEventLocation')?.value.trim(),
        ticket_price: Number(document.getElementById('quickEventPrice')?.value || 0),
        available_tickets: Number(document.getElementById('quickEventTickets')?.value || 0)
    };

    if (!payload.name || !payload.date || !payload.location) {
        if (status) status.textContent = 'Nombre, fecha y ubicación son obligatorios.';
        return;
    }

    try {
        if (status) status.textContent = 'Guardando...';
        const endpoint = eventId ? `/admin/events/${encodeURIComponent(eventId)}` : '/admin/events';
        const method = eventId ? 'PUT' : 'POST';
        await SubsonicAPI.request(endpoint, method, payload);
        if (status) status.textContent = eventId ? 'Evento actualizado.' : 'Evento creado.';
        const list = await SubsonicAPI.request('/admin/events');
        events = Array.isArray(list?.data) ? list.data : events;
        globalThis.events = events;
        if (typeof populateEvents === 'function') populateEvents();
    } catch (error) {
        console.error('Error guardando evento:', error);
        if (status) status.textContent = error.message || 'No se pudo guardar el evento.';
    }
}

function bindQuickEventForm() {
    const button = document.getElementById('quickEventSave');
    if (!button || button.dataset.bound === '1') return;
    button.dataset.bound = '1';
    button.addEventListener('click', saveQuickEvent);
}

const originalCreateNewEvent = globalThis.createNewEvent;
globalThis.createNewEvent = function () {
    const idField = document.getElementById('quickEventId');
    if (idField) idField.value = '';
    bindQuickEventForm();
    if (originalCreateNewEvent) originalCreateNewEvent();
};

document.addEventListener('DOMContentLoaded', bindQuickEventForm);
