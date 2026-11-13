/**
 * TK-009-2: interfaz de reserva de recintos para proveedores.
 */
async function loadBookingVenues() {
    const select = document.getElementById('bookingVenue');
    if (!select) return;
    const response = await SubsonicAPI.request('/venues');
    const venues = response?.data || [];
    select.innerHTML = venues.map((venue) => `<option value="${venue.id}">${venue.name} - ${venue.city}</option>`).join('');
    await refreshBookingSpaces();
}

async function refreshBookingSpaces() {
    const venueId = document.getElementById('bookingVenue')?.value;
    const date = document.getElementById('bookingDate')?.value;
    const spaceSelect = document.getElementById('bookingSpace');
    if (!venueId || !spaceSelect) return;
    if (!date) {
        spaceSelect.innerHTML = '<option value="">Selecciona una fecha</option>';
        return;
    }
    const response = await SubsonicAPI.request(`/venues/${encodeURIComponent(venueId)}/availability?date=${encodeURIComponent(date)}`);
    const spaces = response?.data?.spaces || [];
    spaceSelect.innerHTML = spaces.map((space) => `
        <option value="${space.id}" ${space.available ? '' : 'disabled'}>
            ${space.name} ${space.available ? `(${space.price} €)` : '- ocupado'}
        </option>
    `).join('');
}

async function loadMyBookings() {
    const container = document.getElementById('bookingList');
    if (!container) return;
    try {
        const response = await SubsonicAPI.request('/bookings');
        const bookings = response?.data || [];
        container.innerHTML = bookings.length
            ? bookings.map((booking) => `
                <article class="booking-item">
                    <strong>${booking.venue_id} / ${booking.space_id}</strong>
                    <span>${booking.date} · ${booking.start_time}-${booking.end_time}</span>
                    <span class="booking-status-pill">${booking.status}</span>
                </article>
            `).join('')
            : '<p class="empty-bookings">Todavía no tienes reservas.</p>';
    } catch (error) {
        container.innerHTML = '<p class="empty-bookings">No se pudieron cargar las reservas.</p>';
    }
}

async function submitBooking() {
    const status = document.getElementById('bookingStatus');
    const payload = {
        venue_id: document.getElementById('bookingVenue')?.value,
        space_id: document.getElementById('bookingSpace')?.value,
        date: document.getElementById('bookingDate')?.value,
        start_time: document.getElementById('bookingStart')?.value,
        end_time: document.getElementById('bookingEnd')?.value
    };
    if (!payload.venue_id || !payload.space_id || !payload.date) {
        if (status) status.textContent = 'Completa recinto, fecha y espacio.';
        return;
    }
    try {
        if (status) status.textContent = 'Enviando solicitud...';
        await SubsonicAPI.request('/bookings', 'POST', payload);
        if (status) status.textContent = 'Reserva confirmada.';
        await loadMyBookings();
        await refreshBookingSpaces();
    } catch (error) {
        if (status) status.textContent = error.message || 'No se pudo crear la reserva.';
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await loadBookingVenues();
    await loadMyBookings();
    document.getElementById('bookingDate')?.addEventListener('change', refreshBookingSpaces);
    document.getElementById('bookingVenue')?.addEventListener('change', refreshBookingSpaces);
    document.getElementById('bookingSubmit')?.addEventListener('click', submitBooking);
});


/* TK-012-2: historial de reservas pasadas */
async function loadBookingHistory() {
    const container = document.getElementById('bookingHistoryList');
    const summary = document.getElementById('bookingHistorySummary');
    if (!container) return;
    const status = document.getElementById('bookingHistoryFilter')?.value || '';
    try {
        const response = await SubsonicAPI.request(`/bookings/history?status=${encodeURIComponent(status)}`);
        const bookings = response?.data || [];
        const totals = response?.summary || {};
        if (summary) {
            summary.innerHTML = `
                <span>Total: <strong>${totals.total ?? 0}</strong></span>
                <span>Activas: <strong>${totals.active ?? 0}</strong></span>
                <span>Canceladas: <strong>${totals.cancelled ?? 0}</strong></span>
                <span>Gasto: <strong>${Number(totals.total_spent || 0).toFixed(2)} €</strong></span>
            `;
        }
        container.innerHTML = bookings.length
            ? `
                <table class="booking-history-table">
                    <thead><tr><th>Recinto</th><th>Espacio</th><th>Fecha</th><th>Horario</th><th>Importe</th><th>Estado</th></tr></thead>
                    <tbody>
                        ${bookings.map((booking) => `
                            <tr>
                                <td>${booking.venue_id}</td>
                                <td>${booking.space_id}</td>
                                <td>${booking.date}</td>
                                <td>${booking.start_time}-${booking.end_time}</td>
                                <td>${Number(booking.price || 0).toFixed(2)} €</td>
                                <td><span class="booking-status-pill">${booking.status}</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `
            : '<p class="empty-bookings">No hay reservas en el historial.</p>';
    } catch (error) {
        container.innerHTML = '<p class="empty-bookings">No se pudo cargar el historial.</p>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('bookingHistoryList')) return;
    loadBookingHistory();
    document.getElementById('bookingHistoryFilter')?.addEventListener('change', loadBookingHistory);
});
