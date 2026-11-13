/**
 * TK-014-2: panel de administración (moderación + métricas).
 */
async function loadAdminUsers() {
    const container = document.getElementById('adminUsersTable');
    if (!container) return;
    try {
        const response = await SubsonicAPI.request('/admin/users');
        const users = response?.data || [];
        container.innerHTML = `
            <table class="admin-table">
                <thead><tr><th>Nombre</th><th>Email</th><th>Rol</th><th>Estado</th><th></th></tr></thead>
                <tbody>
                    ${users.map((user) => `
                        <tr>
                            <td>${user.name || '-'}</td>
                            <td>${user.email || '-'}</td>
                            <td>${user.role || '-'}</td>
                            <td>${user.suspended ? 'Suspendida' : 'Activa'}</td>
                            <td>
                                <button data-admin-action="${user.suspended ? 'reactivate' : 'suspend'}" data-uid="${user.uid}">
                                    ${user.suspended ? 'Reactivar' : 'Suspender'}
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>`;
    } catch (error) {
        container.innerHTML = '<p class="admin-empty">No se pudieron cargar las cuentas.</p>';
    }
}

async function loadAdminEvents() {
    const container = document.getElementById('adminEventsTable');
    if (!container) return;
    try {
        const response = await SubsonicAPI.request('/admin/events');
        const events = response?.data || [];
        container.innerHTML = `
            <table class="admin-table">
                <thead><tr><th>Evento</th><th>Fecha</th><th>Estado</th><th></th></tr></thead>
                <tbody>
                    ${events.map((event) => `
                        <tr>
                            <td>${event.name || event.title || '-'}</td>
                            <td>${event.date || '-'}</td>
                            <td>${event.status || 'borrador'}</td>
                            <td>
                                <button data-event-action="aprobado" data-event-id="${event.id}">Aprobar</button>
                                <button data-event-action="rechazado" data-event-id="${event.id}">Rechazar</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>`;
    } catch (error) {
        container.innerHTML = '<p class="admin-empty">No se pudieron cargar los eventos.</p>';
    }
}

function bindAdminActions() {
    document.getElementById('adminUsersTable')?.addEventListener('click', async (event) => {
        const button = event.target.closest('button[data-admin-action]');
        if (!button) return;
        const uid = button.dataset.uid;
        const action = button.dataset.adminAction;
        try {
            await SubsonicAPI.request(`/admin/users/${encodeURIComponent(uid)}/${action}`, 'POST', {});
            await loadAdminUsers();
        } catch (error) {
            alert(error.message || 'No se pudo moderar la cuenta');
        }
    });

    document.getElementById('adminEventsTable')?.addEventListener('click', async (event) => {
        const button = event.target.closest('button[data-event-action]');
        if (!button) return;
        try {
            await SubsonicAPI.request(`/admin/events/${encodeURIComponent(button.dataset.eventId)}/moderate`, 'POST', {
                decision: button.dataset.eventAction
            });
            await loadAdminEvents();
        } catch (error) {
            alert(error.message || 'No se pudo moderar el evento');
        }
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    bindAdminActions();
    await loadAdminUsers();
    await loadAdminEvents();
    document.getElementById('adminRefresh')?.addEventListener('click', async () => {
        await loadAdminUsers();
        await loadAdminEvents();
    });
});
