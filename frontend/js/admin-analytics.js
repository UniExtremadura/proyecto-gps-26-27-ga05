/**
 * TK-015-2: vista de estadísticas globales y exportación CSV.
 */
function renderRoleBreakdown(byRole) {
    const container = document.getElementById('analyticsRoles');
    if (!container) return;
    const entries = Object.entries(byRole || {});
    container.innerHTML = entries.length
        ? entries.map(([role, count]) => `
            <div class="analytics-role-row">
                <span>${role}</span>
                <strong>${count}</strong>
            </div>
        `).join('')
        : '<p class="analytics-empty">Sin usuarios registrados.</p>';
}

function renderFestivalBreakdown(byFestival) {
    const container = document.getElementById('analyticsFestivals');
    if (!container) return;
    const entries = Object.entries(byFestival || {});
    container.innerHTML = entries.length
        ? `
            <table class="analytics-table">
                <thead><tr><th>Festival</th><th>Aforo</th><th>Entradas</th><th>Ocupación</th><th>Ingresos</th></tr></thead>
                <tbody>
                    ${entries.map(([name, item]) => `
                        <tr>
                            <td>${name}</td>
                            <td>${item.capacity}</td>
                            <td>${item.tickets_sold}</td>
                            <td>${item.occupancy}%</td>
                            <td>${Number(item.revenue || 0).toFixed(2)} €</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `
        : '<p class="analytics-empty">Sin festivales en el periodo.</p>';
}

async function loadGlobalAnalytics() {
    const days = Number(document.getElementById('analyticsPeriod')?.value || 30);
    try {
        const response = await SubsonicAPI.request(`/admin/analytics?days=${days}`);
        const data = response?.data || {};
        const summary = data.summary || {};
        document.getElementById('kpiFestivals').textContent = summary.active_festivals ?? 0;
        document.getElementById('kpiUsers').textContent = summary.registered_users ?? 0;
        document.getElementById('kpiOrders').textContent = summary.orders ?? 0;
        document.getElementById('kpiRevenue').textContent = `${Number(summary.total_revenue || 0).toFixed(2)} €`;
        document.getElementById('kpiOccupancy').textContent = `${summary.average_occupancy ?? 0}%`;
        renderFestivalBreakdown(data.by_festival);
        renderRoleBreakdown(data.by_role);
    } catch (error) {
        console.error('No se pudieron cargar las métricas globales:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('analyticsKpis')) return;
    loadGlobalAnalytics();
    document.getElementById('analyticsPeriod')?.addEventListener('change', loadGlobalAnalytics);
    document.getElementById('analyticsExport')?.addEventListener('click', async () => {
        const days = Number(document.getElementById('analyticsPeriod')?.value || 30);
        try {
            const token = localStorage.getItem('sessionToken');
            const response = await fetch(`${API_BASE_URL}/admin/analytics/export?days=${days}`, {
                headers: token ? { Authorization: `Bearer ${token}` } : {}
            });
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `metricas-globales-${days}d.csv`;
            link.click();
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('No se pudo exportar el CSV:', error);
        }
    });
});
