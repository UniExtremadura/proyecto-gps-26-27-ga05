/** Detalle/edición de producto para gestores y proveedores. */
(function () {
    function getParam(name) {
        const hash = String(globalThis.location.hash || '');
        const hashQuery = hash.includes('?') ? hash.split('?')[1] : '';
        return new URLSearchParams(hashQuery).get(name)
            || new URLSearchParams(globalThis.location.search).get(name)
            || '';
    }

    function setStatus(message, isError = false) {
        const node = document.getElementById('productDetailStatus');
        if (!node) return;
        node.textContent = message || '';
        node.classList.toggle('error', isError);
        node.classList.toggle('success', !isError && Boolean(message));
    }

    async function load() {
        const form = document.getElementById('productDetailForm');
        if (!form) return;
        const id = getParam('id');
        const idField = document.getElementById('productDetailId');
        if (idField) idField.value = id;
        if (!id) return;

        try {
            const response = await globalThis.SubsonicAPI.getProduct(id);
            const product = response?.data || {};
            const image = (Array.isArray(product.images) && product.images[0]) || product.image || '';
            const values = {
                productDetailName: product.name || '',
                productDetailCategory: product.category || '',
                productDetailPrice: product.price ?? 0,
                productDetailStock: product.stock ?? 0,
                productDetailMinStock: product.min_stock ?? 5,
                productDetailImage: image,
                productDetailDescription: product.description || ''
            };
            Object.entries(values).forEach(([fieldId, value]) => {
                const field = document.getElementById(fieldId);
                if (field) field.value = value;
            });
            const title = document.getElementById('productDetailTitle');
            if (title) title.textContent = product.name || 'Producto';
        } catch (error) {
            setStatus(error.message || 'No se pudo cargar el producto.', true);
        }
    }

    async function save(event) {
        event?.preventDefault?.();
        const id = document.getElementById('productDetailId')?.value.trim();
        const image = document.getElementById('productDetailImage')?.value.trim();
        const payload = {
            name: document.getElementById('productDetailName')?.value.trim(),
            category: document.getElementById('productDetailCategory')?.value.trim() || 'Varios',
            price: Number(document.getElementById('productDetailPrice')?.value || 0),
            stock: Number(document.getElementById('productDetailStock')?.value || 0),
            min_stock: Number(document.getElementById('productDetailMinStock')?.value || 5),
            description: document.getElementById('productDetailDescription')?.value.trim(),
            images: image ? [image] : []
        };
        if (!payload.name) {
            setStatus('El nombre es obligatorio.', true);
            return;
        }
        try {
            setStatus('Guardando...');
            if (id) await globalThis.SubsonicAPI.updateProduct(id, payload);
            else await globalThis.SubsonicAPI.createProduct(payload);
            setStatus('Producto guardado.');
            globalThis.setTimeout(() => {
                globalThis.location.hash = '#manager-tienda';
                globalThis.location.reload();
            }, 700);
        } catch (error) {
            setStatus(error.message || 'No se pudo guardar el producto.', true);
        }
    }

    async function remove() {
        const id = document.getElementById('productDetailId')?.value.trim();
        if (!id) return;
        if (!await globalThis.showSubsonicConfirm('¿Eliminar este producto?', { danger: true, confirmText: 'Eliminar' })) return;
        try {
            await globalThis.SubsonicAPI.deleteProduct(id);
            globalThis.location.hash = '#manager-tienda';
            globalThis.location.reload();
        } catch (error) {
            setStatus(error.message || 'No se pudo eliminar el producto.', true);
        }
    }

    function bind() {
        if (!document.getElementById('productDetailForm')) return;
        document.getElementById('productDetailForm').addEventListener('submit', save);
        document.getElementById('productDetailDelete')?.addEventListener('click', remove);
        load();
    }

    globalThis.load_manager_producto_detalle = bind;
    globalThis.load_producto_proveedor = bind;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bind);
    } else {
        bind();
    }
})();
