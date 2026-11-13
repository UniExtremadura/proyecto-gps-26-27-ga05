/** Detalle público de artista. */
(function () {
    function escapeHtml(value) {
        return String(value ?? '')
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#039;');
    }

    function getSlug() {
        const hash = String(globalThis.location.hash || '');
        const hashQuery = hash.includes('?') ? hash.split('?')[1] : '';
        return new URLSearchParams(hashQuery).get('slug')
            || new URLSearchParams(globalThis.location.search).get('slug')
            || '';
    }

    async function load() {
        const container = document.getElementById('artistDetail');
        if (!container) return;
        const slug = getSlug();
        if (!slug) {
            container.innerHTML = '<p class="empty-state">No se ha indicado ningún artista.</p>';
            return;
        }
        container.innerHTML = '<p class="loading-state">Cargando artista...</p>';
        try {
            const response = await globalThis.SubsonicAPI.getArtist(slug);
            const artist = response?.data || {};
            container.innerHTML = `
                <div class="artist-detail-layout">
                    <div class="artist-detail-image">
                        ${artist.image ? `<img src="${escapeHtml(artist.image)}" alt="${escapeHtml(artist.name)}">` : '<span>🎤</span>'}
                    </div>
                    <div class="artist-detail-info">
                        <span class="artist-genre">${escapeHtml(artist.genre || 'Música')}</span>
                        <h1>${escapeHtml(artist.name || 'Artista')}</h1>
                        <p class="artist-country">${escapeHtml(artist.country || 'Internacional')}</p>
                        <p>${escapeHtml(artist.bio || 'Sin biografía disponible.')}</p>
                        <a href="#artistas" class="btn btn-outline" data-page="artistas">VOLVER A ARTISTAS</a>
                    </div>
                </div>
            `;
        } catch (error) {
            container.innerHTML = `<p class="empty-state">No se pudo cargar el artista: ${escapeHtml(error.message)}</p>`;
        }
    }

    globalThis.load_artista = load;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', load);
    } else {
        load();
    }
})();
