/** Panel de gestión de productos para gestores/administradores. */
(function () {
    let products = [];

    function escapeHtml(value) {
        return String(value ?? '')
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#039;');
    }

    function setStatus(message, isError = false) {
        const node = document.getElementById('productManagerStatus');
        if (!node) return;
        node.textContent = message || '';
        node.classList.toggle('error', isError);
        node.classList.toggle('success', !isError && Boolean(message));
    }

    function render() {
        const grid = document.getElementById('managerProductsGrid');
        if (!grid) return;
        if (!products.length) {
            grid.innerHTML = '<p class="empty-state">Todavía no hay productos registrados.</p>';
            return;
        }
        grid.innerHTML = products.map((product) => `
            <article class="manager-card">
                <div class="manager-card-image">
                    ${Array.isArray(product.images) && product.images.length ? `<img src="${escapeHtml(product.images[0])}" alt="${escapeHtml(product.name)}">` : '<span>🛍️</span>'}
                </div>
                <div class="manager-card-body">
                    <h3>${escapeHtml(product.name || 'Producto')}</h3>
                    <p>${escapeHtml(product.category || 'Merch')} · ${Number(product.price || 0).toFixed(2)} €</p>
                    <p>Stock: ${escapeHtml(product.stock ?? 0)} / mínimo ${escapeHtml(product.min_stock ?? 5)}</p>
                    <p>${escapeHtml(product.provider || '')}</p>
                    <div class="manager-card-actions">
                        <button type="button" data-edit-product="${escapeHtml(product.id || '')}">EDITAR</button>
                        <button type="button" class="danger" data-delete-product="${escapeHtml(product.id || '')}">ELIMINAR</button>
                    </div>
                </div>
            </article>
        `).join('');

        grid.querySelectorAll('[data-edit-product]').forEach((button) => {
            button.addEventListener('click', () => editProduct(button.dataset.editProduct));
        });
        grid.querySelectorAll('[data-delete-product]').forEach((button) => {
            button.addEventListener('click', () => removeProduct(button.dataset.deleteProduct));
        });
    }

    async function load() {
        const grid = document.getElementById('managerProductsGrid');
        if (!grid) return;
        grid.innerHTML = '<p class="loading-state">Cargando productos...</p>';
        try {
            const response = await globalThis.SubsonicAPI.getAllProducts();
            products = Array.isArray(response?.data) ? response.data : [];
            render();
        } catch (error) {
            grid.innerHTML = `<p class="empty-state">No se pudieron cargar los productos: ${escapeHtml(error.message)}</p>`;
        }
    }

    function editProduct(id) {
        const product = products.find((item) => String(item.id) === String(id));
        if (!product) return;
        document.getElementById('productId').value = product.id || '';
        document.getElementById('productName').value = product.name || '';
        document.getElementById('productCategory').value = product.category || '';
        document.getElementById('productPrice').value = product.price ?? '';
        document.getElementById('productStock').value = product.stock ?? 0;
        document.getElementById('productMinStock').value = product.min_stock ?? 5;
        document.getElementById('productImage').value = (Array.isArray(product.images) && product.images[0]) || product.image || '';
        document.getElementById('productDescription').value = product.description || '';
        setStatus(`Editando ${product.name || id}`);
    }

    async function removeProduct(id) {
        if (!await globalThis.showSubsonicConfirm(`¿Eliminar el producto "${id}"?`, { danger: true, confirmText: 'Eliminar' })) return;
        try {
            await globalThis.SubsonicAPI.deleteProduct(id);
            products = products.filter((item) => String(item.id) !== String(id));
            render();
            setStatus('Producto eliminado.');
        } catch (error) {
            setStatus(error.message || 'No se pudo eliminar el producto.', true);
        }
    }

    async function save(event) {
        event?.preventDefault?.();
        const id = document.getElementById('productId')?.value.trim();
        const image = document.getElementById('productImage')?.value.trim();
        const payload = {
            name: document.getElementById('productName')?.value.trim(),
            category: document.getElementById('productCategory')?.value.trim() || 'Varios',
            price: Number(document.getElementById('productPrice')?.value || 0),
            stock: Number(document.getElementById('productStock')?.value || 0),
            min_stock: Number(document.getElementById('productMinStock')?.value || 5),
            description: document.getElementById('productDescription')?.value.trim(),
            images: image ? [image] : []
        };
        if (!payload.name) {
            setStatus('El nombre del producto es obligatorio.', true);
            return;
        }
        try {
            setStatus('Guardando...');
            const response = id
                ? await globalThis.SubsonicAPI.updateProduct(id, payload)
                : await globalThis.SubsonicAPI.createProduct(payload);
            document.getElementById('productManagerForm')?.reset();
            document.getElementById('productId').value = '';
            await load();
            setStatus(id ? 'Producto actualizado.' : `Producto creado${response?.data?.id ? ` (${response.data.id})` : ''}.`);
        } catch (error) {
            setStatus(error.message || 'No se pudo guardar el producto.', true);
        }
    }

    function bind() {
        if (!document.getElementById('managerProductsGrid')) return;
        document.getElementById('productManagerForm')?.addEventListener('submit', save);
        load();
    }

    globalThis.load_manager_tienda = bind;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bind);
    } else {
        bind();
    }
})();
