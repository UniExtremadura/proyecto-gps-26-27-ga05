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

async function loadAdminKpis() {
    try {
        const response = await SubsonicAPI.request('/admin/analytics?days=30');
        const summary = response?.data?.summary || {};
        const setText = (id, value) => {
            const node = document.getElementById(id);
            if (node) node.textContent = value;
        };
        setText('kpiUsers', summary.registered_users ?? 0);
        setText('kpiEvents', summary.active_festivals ?? 0);
        setText('kpiOrders', summary.orders ?? 0);
        setText('kpiRevenue', `${Number(summary.total_revenue || 0).toFixed(2)} €`);
    } catch (error) {
        console.warn('No se pudieron cargar los KPIs de administración:', error);
    }
}

function bindAdminExport() {
    document.getElementById('adminExportCsv')?.addEventListener('click', async () => {
        try {
            const token = localStorage.getItem('sessionToken');
            const response = await fetch(`${API_BASE_URL}/admin/analytics/export?days=30`, {
                headers: token ? { Authorization: `Bearer ${token}` } : {}
            });
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'metricas-globales.csv';
            link.click();
            URL.revokeObjectURL(url);
        } catch (error) {
            alert(error.message || 'No se pudo exportar el CSV');
        }
    });
}

async function initAdminPanel() {
    bindAdminActions();
    bindAdminExport();
    await loadAdminKpis();
    await loadAdminUsers();
    await loadAdminEvents();
    document.getElementById('adminRefresh')?.addEventListener('click', async () => {
        await loadAdminKpis();
        await loadAdminUsers();
        await loadAdminEvents();
    });
}

document.addEventListener('DOMContentLoaded', initAdminPanel);
globalThis.load_admin_panel = initAdminPanel;
