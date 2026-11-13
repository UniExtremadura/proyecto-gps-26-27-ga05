/* merchandise page logic */

let products = [];
let searchText = '';
let categoryFilter = 'Todos';

function filterProducts() {
    return products.filter(p => {
        let matchesSearch = (p.name && p.name.toLowerCase().includes(searchText.toLowerCase())) || 
                           (p.provider && p.provider.toLowerCase().includes(searchText.toLowerCase()));
        let matchesCat = categoryFilter === 'Todos' || p.category === categoryFilter;
        return matchesSearch && matchesCat;
    });
}

function renderProducts() {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;
    grid.innerHTML = '';
    const list = filterProducts();
    
    if (list.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #888;">No hay productos disponibles</div>';
        return;
    }
    
    list.forEach(p => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML =
            `<div class="product-header">
                ${p.images && p.images.length > 0 && p.images[0] ? `<img src="${p.images[0]}" style="width: 100%; height: 100%; object-fit: cover;" alt="${p.name}">` : '<div class="no-image-placeholder">Sin imagen</div>'}
             </div>
             <div class="product-body">
                <div class="product-category">${escapeHtml(p.category || 'N/A')}</div>
                <h3 class="product-name">${escapeHtml(p.name || 'Sin nombre')}</h3>
                <div class="product-provider" style="font-size: 0.80rem; color: #888; margin: 0.25rem 0;">Empresa: ${escapeHtml(p.provider || 'Desconocida')}</div>
                <div class="product-price">${(p.price || 0).toFixed(2)}€</div>
                <div class="product-actions">
                    <button class="btn btn-primary add-cart" data-id="${p.id}">Añadir al carrito</button>
                    <button class="btn btn-success buy-now" data-id="${p.id}">Comprar Ahora</button>
                    <button class="btn btn-outline more-info" data-id="${p.id}">Más información</button>
                </div>
             </div>`;
        grid.appendChild(card);
        
        // Listener para "Más información"
        const moreInfoBtn = card.querySelector('.more-info');
        if (moreInfoBtn) {
            moreInfoBtn.addEventListener('click', (e) => {
                e.preventDefault();
                globalThis.location.hash = `producto?id=${p.id}`;
            });
        }

        // Listener para "Comprar Ahora"
        const buyNowBtn = card.querySelector('.buy-now');
        if (buyNowBtn) {
            buyNowBtn.addEventListener('click', (e) => {
                e.preventDefault();
                buyProductNow(p);
            });
        }

        // Listener para "Añadir al carrito"
        const addCartBtn = card.querySelector('.add-cart');
        if (addCartBtn) {
            addCartBtn.addEventListener('click', (e) => {
                e.preventDefault();
                addToCart(p);
            });
        }
    });
}

function setupSearchAndFilters() {
    const searchInput = document.getElementById('merchSearch');
    const catContainer = document.getElementById('categoryFilters');
    if (searchInput && !searchInput.dataset.bound) {
        searchInput.dataset.bound = '1';
        searchInput.addEventListener('input', e => {
            searchText = e.target.value;
            renderProducts();
        });
    }
    if (catContainer && !catContainer.dataset.bound) {
        catContainer.dataset.bound = '1';
        catContainer.addEventListener('click', e => {
            if (e.target.tagName === 'BUTTON') {
                const btn = e.target;
                categoryFilter = btn.dataset.category;
                // toggle active class
                catContainer.querySelectorAll('button').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderProducts();
            }
        });
    }
}

async function loadProducts() {
    try {
        const response = await SubsonicAPI.getAllProducts();
        if (response && response.data) {
            products = response.data;
            renderProducts();
        } else {
            throw new Error('Respuesta inválida del servidor');
        }
    } catch (error) {
        console.error('Error loading products:', error);
        const grid = document.getElementById('productsGrid');
        if (grid) {
            grid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 40px;">
                    <p style="color: #888; margin-bottom: 20px;">No hay productos disponibles en este momento.</p>
                    <small style="color: #666;">Por favor, intenta recargar la página o contáctanos si el problema persiste.</small>
                </div>
            `;
        }
    }
}

// Función para añadir al carrito
function addToCart(product) {
    if (!globalThis.ensureBuyerRole()) {
        return;
    }

    const color = product.colors && product.colors.length > 0 ? product.colors[0] : 'Sin especificar';

    globalThis.SubsonicCart.addItem({
        id: product.id,
        name: product.name,
        type: 'Merch',
        category: product.category || 'Merch',
        price: product.price,
        image: product.image || product.image_url || product.cardImg || product.heroImg || (Array.isArray(product.images) ? product.images[0] : ''),
        images: Array.isArray(product.images) ? product.images : [],
        qty: 1,
        color: color,
        timestamp: Date.now()
    });

    alert(`"${product.name}" añadido al carrito`);
}

// Función para comprar directamente
function buyProductNow(product) {
    if (!globalThis.ensureBuyerRole()) {
        return;
    }

    const color = product.colors && product.colors.length > 0 ? product.colors[0] : 'Sin especificar';

    globalThis.SubsonicCart.addItem({
        id: product.id,
        name: product.name,
        type: 'Merch',
        category: product.category || 'Merch',
        price: product.price,
        image: product.image || product.image_url || product.cardImg || product.heroImg || (Array.isArray(product.images) ? product.images[0] : ''),
        images: Array.isArray(product.images) ? product.images : [],
        qty: 1,
        color: color,
        timestamp: Date.now()
    });
    
    // Redirigir directamente al carrito
    globalThis.location.hash = 'carrito';
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function initMerch() {
    if (!document.getElementById('productsGrid')) return;
    loadProducts();
    setupSearchAndFilters();
}

globalThis.load_tienda = function () {
    initMerch();
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', globalThis.load_tienda);
} else {
    globalThis.load_tienda();
}

function bootTiendaWhenReady(retries = 20) {
    if (document.getElementById('productsGrid')) {
        globalThis.load_tienda();
        return;
    }
    if (retries <= 0) return;
    globalThis.setTimeout(() => bootTiendaWhenReady(retries - 1), 50);
}

bootTiendaWhenReady();



/* TK-010-2: indicadores de stock en el catálogo público */
async function decorateProductStock() {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;
    try {
        const response = await SubsonicAPI.request('/stock');
        const stockItems = response?.data || [];
        const byId = Object.fromEntries(stockItems.map((item) => [String(item.product_id), item]));
        grid.querySelectorAll('[data-product-id]').forEach((card) => {
            const item = byId[String(card.dataset.productId)];
            if (!item) return;
            let badge = card.querySelector('.stock-badge');
            if (!badge) {
                badge = document.createElement('span');
                badge.className = 'stock-badge';
                card.appendChild(badge);
            }
            badge.textContent = item.stock > 0 ? `${item.stock} disponibles` : 'Agotado';
            badge.classList.toggle('stock-low', item.low_stock);
            badge.classList.toggle('stock-out', item.stock <= 0);
        });
        const summary = document.getElementById('merchStockSummary');
        if (summary) {
            summary.textContent = `${stockItems.filter((item) => item.low_stock).length} productos con stock bajo`;
        }
    } catch (error) {
        console.warn('No se pudo consultar el stock:', error);
    }
}

const productGridObserver = new MutationObserver(() => decorateProductStock());
document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('productsGrid');
    if (grid) productGridObserver.observe(grid, { childList: true });
    decorateProductStock();
});
