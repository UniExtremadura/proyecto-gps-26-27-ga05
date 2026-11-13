// ventas.js - balance real del proveedor

let operations = [];
let summaryData = {
    total_balance: 0,
    sales_today: 0,
    units_sold: 0,
    top_product: 'Ninguno'
};

// función para formatear importe
function formatAmount(amount) {
    const sign = amount < 0 ? '-' : '+';
    const abs = Math.abs(amount);
    return `${sign}${abs.toFixed(2).replace('.', ',')}€`;
}

// renderizar tabla
function renderOperationsTable() {
    const tbody = document.getElementById('operations-tbody');
    if (!tbody) return;

    if (!operations.length) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" style="text-align:center;color:#94a3b8;padding:1.2rem;">Aún no hay ventas registradas para tus productos.</td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = operations.map((op) => {
        const amountClass = op.amount < 0 ? 'negative' : 'positive';
        const typeClass = 'venta';
        const statusRaw = String(op.status || 'pendiente').toLowerCase();
        const statusClass = (statusRaw === 'confirmado' || statusRaw === 'entregado')
            ? 'completed'
            : (statusRaw === 'cancelada' ? 'cancelled' : 'active');
        const statusText = op.status || 'pendiente';
        const typeLabel = 'Venta producto';

        return `
            <tr>
                <td class="op-id">${op.id}</td>
                <td class="op-concept">${op.item}</td>
                <td><span class="op-type ${typeClass}">${typeLabel}</span></td>
                <td class="op-date">${op.date}</td>
                <td class="op-amount ${amountClass}">${formatAmount(op.amount)}</td>
                <td class="op-status">
                    <div class="status-indicator">
                        <span class="status-dot ${statusClass}"></span>
                        <span class="status-text">${statusText}</span>
                    </div>
                </td>
                <td class="op-gestion">
                    <span class="finalized">Finalizado</span>
                </td>
            </tr>
        `;
    }).join('');
}

// actualizar resúmenes en la UI
function updateSummaries() {
    document.getElementById('current-balance').textContent = formatAmount(summaryData.total_balance || 0).replace('+', '');
    document.getElementById('slots-reservados').textContent = `${summaryData.units_sold || 0} uds`;
    document.getElementById('ventas-hoy').textContent = formatAmount(summaryData.sales_today || 0).replace('+', '');
    document.getElementById('proximo-evento').textContent = summaryData.top_product || 'Ninguno';
}

async function loadProviderSalesData() {
    const response = await SubsonicAPI.getProviderSales();
    const payload = response?.data || {};
    operations = Array.isArray(payload.operations) ? payload.operations : [];
    summaryData = {
        total_balance: Number(payload.summary?.total_balance || 0),
        sales_today: Number(payload.summary?.sales_today || 0),
        units_sold: Number(payload.summary?.units_sold || 0),
        top_product: payload.summary?.top_product || 'Ninguno'
    };
}

// evento principal
document.addEventListener('DOMContentLoaded', function() {
    const user = AUTH.getUser();
    if (!user || user.role !== 'proveedor') {
        globalThis.location.hash = 'login';
        return;
    }

    const userGreeting = document.querySelector('.user-greeting');
    if (userGreeting) userGreeting.textContent = `Hola, ${user.name}`;

    const userAvatarLink = document.querySelector('#user-avatar-link');
    if (userAvatarLink) {
        const initial = user.name.charAt(0).toUpperCase();
        const userImg = userAvatarLink.querySelector('img');
        if (userImg) {
            userImg.src = `https://ui-avatars.com/api/?name=${initial}&background=00d4ff&color=000&bold=true&size=40`;
        }
        userAvatarLink.href = 'provider-profile.html';
    }

    const backButton = document.getElementById('back-button');
    if (backButton) backButton.href = 'provider-profile.html';

    // Setup nueva reserva button listener
    const newReservaBtn = document.querySelector('.new-reserva-btn');
    if (newReservaBtn) {
        newReservaBtn.addEventListener('click', function() {
            globalThis.location.hash = 'eventosProveedor';
        });
    }

    // set company name
    document.getElementById('company-name').textContent = user.name.toUpperCase();

    loadProviderSalesData()
        .then(() => {
            renderOperationsTable();
            updateSummaries();
            loadSalesMetrics();
        })
        .catch((error) => {
            console.error('No se pudo cargar el balance del proveedor:', error);
            renderOperationsTable();
            updateSummaries();
        });
});



/* TK-013-2: métricas, gráficos y exportación */
function renderMetricsChart(days) {
    const chart = document.getElementById('metricsChart');
    if (!chart) return;
    if (!days.length) {
        chart.innerHTML = '<p class="metrics-empty">Sin datos para el periodo seleccionado.</p>';
        return;
    }
    const max = Math.max(...days.map((day) => Number(day.revenue) || 0), 1);
    chart.innerHTML = days.map((day) => {
        const height = Math.max(4, Math.round((Number(day.revenue) || 0) / max * 100));
        return `
            <div class="metrics-bar" title="${day.date}: ${Number(day.revenue).toFixed(2)} €">
                <div class="metrics-bar-fill" style="height:${height}%"></div>
                <span>${day.date.slice(5)}</span>
            </div>
        `;
    }).join('');
}

function renderMetricsTable(products) {
    const tbody = document.getElementById('metrics-productos');
    if (!tbody) return;
    tbody.innerHTML = products.length
        ? products.map((product) => `
            <tr>
                <td class="op-concept">${product.product}</td>
                <td>${product.units}</td>
                <td class="op-amount positive">${formatAmount(Number(product.revenue) || 0)}</td>
            </tr>
        `).join('')
        : '<tr><td colspan="3" style="text-align:center;color:#94a3b8;padding:1.2rem;">Todavía no hay ventas.</td></tr>';
}

async function loadSalesMetrics() {
    const days = Number(document.getElementById('metricsPeriod')?.value || 30);
    try {
        const response = await SubsonicAPI.request(`/metrics/sales?days=${days}`);
        const data = response?.data || {};
        const summary = data.summary || {};
        document.getElementById('metricsRevenue').textContent = formatAmount(Number(summary.revenue) || 0).replace('+', '');
        document.getElementById('metricsOrders').textContent = summary.orders ?? 0;
        document.getElementById('metricsUnits').textContent = summary.units ?? 0;
        document.getElementById('metricsTicket').textContent = formatAmount(Number(summary.average_ticket) || 0).replace('+', '');
        renderMetricsChart(data.by_day || []);
        renderMetricsTable(data.by_product || []);
    } catch (error) {
        console.error('No se pudieron cargar las métricas de ventas:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('metricsChart')) return;
    loadSalesMetrics();
    document.getElementById('metricsPeriod')?.addEventListener('change', loadSalesMetrics);
    document.getElementById('metricsExport')?.addEventListener('click', async () => {
        const days = Number(document.getElementById('metricsPeriod')?.value || 30);
        try {
            const token = localStorage.getItem('sessionToken');
            const response = await fetch(`${API_BASE_URL}/metrics/sales/export?days=${days}`, {
                headers: token ? { Authorization: `Bearer ${token}` } : {}
            });
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `ventas-${days}d.csv`;
            link.click();
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('No se pudo exportar el CSV:', error);
        }
    });
});
