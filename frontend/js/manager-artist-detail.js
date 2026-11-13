/** Detalle/edición de artista. */
(function () {
    function getParam(name) {
        const hash = String(globalThis.location.hash || '');
        const hashQuery = hash.includes('?') ? hash.split('?')[1] : '';
        return new URLSearchParams(hashQuery).get(name)
            || new URLSearchParams(globalThis.location.search).get(name)
            || '';
    }

    function setStatus(message, isError = false) {
        const node = document.getElementById('artistDetailStatus');
        if (!node) return;
        node.textContent = message || '';
        node.classList.toggle('error', isError);
        node.classList.toggle('success', !isError && Boolean(message));
    }

    async function load() {
        const form = document.getElementById('artistDetailForm');
        if (!form) return;
        const slug = getParam('slug') || getParam('id');
        const idField = document.getElementById('artistDetailId');
        if (idField) idField.value = slug;
        if (!slug) return;

        try {
            const response = await globalThis.SubsonicAPI.getArtist(slug);
            const artist = response?.data || {};
            const values = {
                artistDetailName: artist.name || '',
                artistDetailGenre: artist.genre || '',
                artistDetailCountry: artist.country || '',
                artistDetailImage: artist.image || '',
                artistDetailBio: artist.bio || ''
            };
            Object.entries(values).forEach(([id, value]) => {
                const field = document.getElementById(id);
                if (field) field.value = value;
            });
            const title = document.getElementById('artistDetailTitle');
            if (title) title.textContent = artist.name || 'Artista';
        } catch (error) {
            setStatus(error.message || 'No se pudo cargar el artista.', true);
        }
    }

    async function save(event) {
        event?.preventDefault?.();
        const slug = document.getElementById('artistDetailId')?.value.trim();
        const payload = {
            name: document.getElementById('artistDetailName')?.value.trim(),
            genre: document.getElementById('artistDetailGenre')?.value.trim(),
            country: document.getElementById('artistDetailCountry')?.value.trim(),
            image: document.getElementById('artistDetailImage')?.value.trim(),
            bio: document.getElementById('artistDetailBio')?.value.trim()
        };
        if (!payload.name) {
            setStatus('El nombre es obligatorio.', true);
            return;
        }
        try {
            setStatus('Guardando...');
            if (slug) await globalThis.SubsonicAPI.updateArtist(slug, payload);
            else await globalThis.SubsonicAPI.createArtist(payload);
            setStatus('Artista guardado.');
            globalThis.setTimeout(() => {
                globalThis.location.hash = '#manager-artists';
                globalThis.location.reload();
            }, 700);
        } catch (error) {
            setStatus(error.message || 'No se pudo guardar el artista.', true);
        }
    }

    async function remove() {
        const slug = document.getElementById('artistDetailId')?.value.trim();
        if (!slug) return;
        if (!await globalThis.showSubsonicConfirm('¿Eliminar este artista?', { danger: true, confirmText: 'Eliminar' })) return;
        try {
            await globalThis.SubsonicAPI.deleteArtist(slug);
            globalThis.location.hash = '#manager-artists';
            globalThis.location.reload();
        } catch (error) {
            setStatus(error.message || 'No se pudo eliminar el artista.', true);
        }
    }

    function bind() {
        if (!document.getElementById('artistDetailForm')) return;
        document.getElementById('artistDetailForm').addEventListener('submit', save);
        document.getElementById('artistDetailDelete')?.addEventListener('click', remove);
        load();
    }

    globalThis.load_manager_artist_detail = bind;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bind);
    } else {
        bind();
    }
})();
