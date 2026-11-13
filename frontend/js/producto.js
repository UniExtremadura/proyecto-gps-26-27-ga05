/** Detalle de producto de merchandising. */
(function () {
    function escapeHtml(value) {
        return String(value ?? '')
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#039;');
    }

    function getQueryParam(name) {
        const hash = String(globalThis.location.hash || '');
        const hashQuery = hash.includes('?') ? hash.split('?')[1] : '';
        return new URLSearchParams(hashQuery).get(name)
            || new URLSearchParams(globalThis.location.search).get(name)
            || '';
    }

    function imageOf(product) {
        if (Array.isArray(product.images) && product.images.length) return product.images[0];
        return product.image || product.image_url || '';
    }

    function addToCart(product) {
        if (typeof globalThis.ensureBuyerRole === 'function' && !globalThis.ensureBuyerRole()) return;
        globalThis.SubsonicCart.addItem({
            id: product.id,
            name: product.name,
            type: 'Merch',
            category: product.category || 'Merch',
            price: Number(product.price || 0),
            color: Array.isArray(product.colors) && product.colors.length ? product.colors[0] : '',
            image: imageOf(product),
            images: Array.isArray(product.images) ? product.images : [],
            qty: 1
        });
        globalThis.alert(`"${product.name}" añadido al carrito.`);
    }

    async function load() {
        const container = document.getElementById('productDetail');
        if (!container) return;
        const productId = getQueryParam('id');
        if (!productId) {
            container.innerHTML = '<p class="empty-state">No se ha indicado ningún producto.</p>';
            return;
        }

        container.innerHTML = '<p class="loading-state">Cargando producto...</p>';
        try {
            const response = await globalThis.SubsonicAPI.getProduct(productId);
            const product = response?.data || {};
            const image = imageOf(product);
            container.innerHTML = `
                <div class="product-detail-layout">
                    <div class="product-detail-media">
                        ${image ? `<img src="${escapeHtml(image)}" alt="${escapeHtml(product.name)}">` : '<span class="product-placeholder">🛍️</span>'}
                    </div>
                    <div class="product-detail-info">
                        <span class="product-category">${escapeHtml(product.category || 'Merch')}</span>
                        <h1>${escapeHtml(product.name || 'Producto')}</h1>
                        <p class="product-provider">Empresa: ${escapeHtml(product.provider || 'Subsonic Merch')}</p>
                        <p class="product-detail-price">${Number(product.price || 0).toFixed(2)} €</p>
                        <p>${escapeHtml(product.description || '')}</p>
                        <ul class="product-meta">
                            ${product.material ? `<li><strong>Material:</strong> ${escapeHtml(product.material)}</li>` : ''}
                            ${product.shipping ? `<li><strong>Envío:</strong> ${escapeHtml(product.shipping)}</li>` : ''}
                            ${product.stock !== undefined ? `<li><strong>Stock:</strong> ${escapeHtml(product.stock)} unidades</li>` : ''}
                        </ul>
                        <button id="productAddToCart" class="btn btn-primary" type="button">AÑADIR AL CARRITO</button>
                        <a href="#tienda" class="btn btn-outline" data-page="tienda">VOLVER A LA TIENDA</a>
                    </div>
                </div>
            `;
            document.getElementById('productAddToCart')?.addEventListener('click', () => addToCart(product));
        } catch (error) {
            container.innerHTML = `<p class="empty-state">No se pudo cargar el producto: ${escapeHtml(error.message)}</p>`;
        }
    }

    globalThis.load_producto = load;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', load);
    } else {
        load();
    }
})();
