/** Listado público de artistas. */
(function () {
    let artists = [];

    function escapeHtml(value) {
        return String(value ?? '')
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#039;');
    }

    function render() {
        const grid = document.getElementById('artistsGrid');
        if (!grid) return;
        const query = String(document.getElementById('artistsSearch')?.value || '').toLowerCase().trim();
        const filtered = artists.filter((artist) => {
            const haystack = `${artist.name || ''} ${artist.genre || ''} ${artist.country || ''}`.toLowerCase();
            return !query || haystack.includes(query);
        });

        if (!filtered.length) {
            grid.innerHTML = '<p class="empty-state">No hay artistas que coincidan con la búsqueda.</p>';
            return;
        }

        grid.innerHTML = filtered.map((artist) => `
            <a class="artist-card" href="#artista?slug=${encodeURIComponent(artist.slug || artist.id || '')}" data-page="artista">
                <div class="artist-image">
                    ${artist.image ? `<img src="${escapeHtml(artist.image)}" alt="${escapeHtml(artist.name)}" loading="lazy">` : '<span>🎤</span>'}
                </div>
                <div class="artist-body">
                    <h3>${escapeHtml(artist.name || 'Artista')}</h3>
                    <p>${escapeHtml(artist.genre || 'Música')} · ${escapeHtml(artist.country || 'Internacional')}</p>
                </div>
            </a>
        `).join('');
    }

    async function load() {
        const grid = document.getElementById('artistsGrid');
        if (!grid) return;
        grid.innerHTML = '<p class="loading-state">Cargando artistas...</p>';
        try {
            const response = await globalThis.SubsonicAPI.getAllArtists();
            artists = Array.isArray(response?.data) ? response.data : [];
            render();
        } catch (error) {
            grid.innerHTML = `<p class="empty-state">No se pudieron cargar los artistas: ${escapeHtml(error.message)}</p>`;
        }
        const search = document.getElementById('artistsSearch');
        if (search && !search.dataset.bound) {
            search.dataset.bound = '1';
            search.addEventListener('input', render);
        }
    }

    globalThis.load_artistas = load;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', load);
    } else {
        load();
    }
})();
