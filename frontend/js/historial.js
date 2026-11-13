/** Historial de pedidos del usuario autenticado. */
(function () {
    function escapeHtml(value) {
        return String(value ?? '')
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#039;');
    }

    function formatDate(value) {
        if (!value) return '-';
        const date = new Date(value);
        if (Number.isNaN(date.getTime())) return String(value);
        return date.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });
    }

    async function load() {
        const container = document.getElementById('ordersHistory');
        if (!container) return;
        if (!globalThis.AUTH?.isLoggedIn?.()) {
            globalThis.location.hash = '#login';
            globalThis.location.reload();
            return;
        }

        container.innerHTML = '<p class="loading-state">Cargando historial...</p>';
        try {
            const response = await globalThis.SubsonicAPI.getUserOrders();
            const orders = Array.isArray(response?.data) ? response.data : [];
            if (!orders.length) {
                container.innerHTML = '<p class="empty-state">Todavía no tienes pedidos.</p>';
                return;
            }

            container.innerHTML = `
                <table class="orders-table">
                    <thead><tr><th>Pedido</th><th>Fecha</th><th>Artículos</th><th>Total</th><th>Estado</th></tr></thead>
                    <tbody>
                        ${orders.map((order) => {
                            const items = Array.isArray(order.items) ? order.items : [];
                            const summary = items.map((item) => `${item.name || item.product_name || 'Artículo'} × ${item.quantity || item.qty || 1}`).join(', ');
                            return `
                                <tr>
                                    <td><strong>${escapeHtml(order.id || order.order_id || '-')}</strong></td>
                                    <td>${escapeHtml(formatDate(order.created_at))}</td>
                                    <td>${escapeHtml(summary || '-')}</td>
                                    <td>${Number(order.total || order.total_price || 0).toFixed(2)} €</td>
                                    <td><span class="order-status">${escapeHtml(order.status || 'pendiente')}</span></td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            `;
        } catch (error) {
            container.innerHTML = `<p class="empty-state">No se pudo cargar el historial: ${escapeHtml(error.message)}</p>`;
        }
    }

    globalThis.load_historial = load;
    globalThis.loadOrdersHistory = load;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', load);
    } else {
        load();
    }
})();
