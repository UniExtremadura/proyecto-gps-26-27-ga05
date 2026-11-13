/** Carrito y creación de pedidos. */
(function () {
    function escapeHtml(value) {
        return String(value ?? '')
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#039;');
    }

    function getItems() {
        return globalThis.SubsonicCart?.getItems?.() || [];
    }

    function save(items) {
        globalThis.SubsonicCart?.saveItems?.(items);
    }

    function render() {
        const container = document.getElementById('cartItems');
        const empty = document.getElementById('cartEmpty');
        const totalNode = document.getElementById('cartTotal');
        if (!container) return;

        const items = getItems();
        if (!items.length) {
            container.innerHTML = '';
            if (empty) empty.classList.remove('hidden');
            if (totalNode) totalNode.textContent = '0.00 €';
            const checkout = document.getElementById('checkoutBtn');
            if (checkout) checkout.disabled = true;
            return;
        }

        if (empty) empty.classList.add('hidden');
        const checkout = document.getElementById('checkoutBtn');
        if (checkout) checkout.disabled = false;

        container.innerHTML = items.map((item, index) => `
            <article class="cart-item">
                <div class="cart-item-image">
                    ${item.image ? `<img src="${escapeHtml(item.image)}" alt="${escapeHtml(item.name)}">` : '<span>🎟️</span>'}
                </div>
                <div class="cart-item-info">
                    <h3>${escapeHtml(item.name)}</h3>
                    <p>${escapeHtml(item.category || item.type || 'Artículo')}${item.color ? ` · ${escapeHtml(item.color)}` : ''}</p>
                    <div class="cart-item-controls">
                        <button type="button" data-cart-action="decrease" data-index="${index}">−</button>
                        <span>${Number(item.qty || item.quantity || 1)}</span>
                        <button type="button" data-cart-action="increase" data-index="${index}">+</button>
                        <button type="button" class="cart-remove" data-cart-action="remove" data-index="${index}">Eliminar</button>
                    </div>
                </div>
                <div class="cart-item-price">${(Number(item.price || 0) * Number(item.qty || item.quantity || 1)).toFixed(2)} €</div>
            </article>
        `).join('');

        const total = items.reduce((sum, item) => sum + Number(item.price || 0) * Number(item.qty || item.quantity || 1), 0);
        if (totalNode) totalNode.textContent = `${total.toFixed(2)} €`;

        container.querySelectorAll('[data-cart-action]').forEach((button) => {
            button.addEventListener('click', () => {
                const index = Number(button.dataset.index);
                const action = button.dataset.cartAction;
                const next = getItems();
                if (!next[index]) return;
                if (action === 'increase') {
                    next[index].qty = Number(next[index].qty || next[index].quantity || 1) + 1;
                    next[index].quantity = next[index].qty;
                } else if (action === 'decrease') {
                    next[index].qty = Math.max(1, Number(next[index].qty || next[index].quantity || 1) - 1);
                    next[index].quantity = next[index].qty;
                } else if (action === 'remove') {
                    next.splice(index, 1);
                }
                save(next);
                render();
            });
        });
    }

    async function checkout() {
        const status = document.getElementById('checkoutStatus');
        const items = getItems();
        if (!items.length) return;

        if (!globalThis.AUTH?.isLoggedIn?.()) {
            if (status) status.textContent = 'Inicia sesión para completar la compra.';
            globalThis.location.hash = '#login';
            globalThis.location.reload();
            return;
        }

        const total = items.reduce((sum, item) => sum + Number(item.price || 0) * Number(item.qty || item.quantity || 1), 0);
        const payload = {
            items: items.map((item) => ({
                ...item,
                quantity: Number(item.qty || item.quantity || 1),
                qty: Number(item.qty || item.quantity || 1)
            })),
            total: Number(total.toFixed(2)),
            payment_method: document.getElementById('checkoutPayment')?.value || 'demo',
            delivery_address: document.getElementById('checkoutAddress')?.value.trim() || ''
        };

        const button = document.getElementById('checkoutBtn');
        if (button) button.disabled = true;
        if (status) status.textContent = 'Procesando pedido...';

        try {
            const response = await globalThis.SubsonicAPI.createOrder(payload);
            save([]);
            render();
            if (status) {
                status.textContent = `Pedido creado correctamente (${response?.data?.id || ''}).`;
                status.classList.add('success');
            }
            globalThis.setTimeout(() => {
                globalThis.location.hash = '#historial';
                globalThis.location.reload();
            }, 900);
        } catch (error) {
            if (status) {
                status.textContent = error.message || 'No se pudo completar el pedido.';
                status.classList.remove('success');
                status.classList.add('error');
            }
        } finally {
            if (button) button.disabled = false;
        }
    }

    function bind() {
        const container = document.getElementById('cartItems');
        if (!container) return;
        render();
        document.getElementById('checkoutBtn')?.addEventListener('click', checkout);
        globalThis.addEventListener?.('storage', (event) => {
            if (event.key === globalThis.SubsonicCart?.key) render();
        });
    }

    globalThis.load_carrito = bind;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bind);
    } else {
        bind();
    }
})();
