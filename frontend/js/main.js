/** Contenido dinámico de la portada (line-up y festivales). */
(function () {
    const FALLBACK_ARTISTS = [
        { name: 'DJ Voltage', genre: 'Electrónica', country: 'España' },
        { name: 'Neon Shadow', genre: 'Synthwave', country: 'Portugal' },
        { name: 'The Glitch', genre: 'Indie', country: 'Francia' }
    ];

    function escapeHtml(value) {
        return String(value ?? '')
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#039;');
    }

    function renderLineup(artists) {
        const grid = document.getElementById('lineup-grid');
        if (!grid) return;
        const list = artists.length ? artists : FALLBACK_ARTISTS;
        grid.innerHTML = list.slice(0, 8).map((artist) => `
            <article class="lineup-card">
                <h3>${escapeHtml(artist.name || 'Artista')}</h3>
                <p>${escapeHtml(artist.genre || 'Música')} · ${escapeHtml(artist.country || 'Internacional')}</p>
            </article>
        `).join('');
    }

    function renderFestivals(events) {
        const globe = document.getElementById('festivals-globe');
        if (!globe) return;
        if (!events.length) {
            globe.innerHTML = '<span class="globe-festival-pill">Próximamente nuevos festivales</span>';
            return;
        }
        globe.innerHTML = events.slice(0, 10).map((event) => `
            <a class="globe-festival-pill" href="#eventos" data-page="eventos">
                ${escapeHtml(event.name || event.title || 'Festival')}
            </a>
        `).join('');
    }

    async function loadIndex() {
        if (!document.getElementById('lineup-grid') && !document.getElementById('festivals-globe')) return;

        let artists = [];
        let events = [];
        try {
            if (globalThis.SubsonicAPI?.getAllArtists) {
                const response = await globalThis.SubsonicAPI.getAllArtists();
                artists = Array.isArray(response?.data) ? response.data : [];
            }
        } catch (error) {
            console.warn('No se pudieron cargar los artistas de la portada:', error);
        }
        try {
            if (globalThis.SubsonicAPI?.getAllEvents) {
                const response = await globalThis.SubsonicAPI.getAllEvents();
                events = Array.isArray(response?.data) ? response.data : [];
            }
        } catch (error) {
            console.warn('No se pudieron cargar los festivales de la portada:', error);
        }

        renderLineup(artists);
        renderFestivals(events);

        if (typeof globalThis.initNeuralGlow === 'function') {
            globalThis.initNeuralGlow();
        }
    }

    globalThis.load_index = loadIndex;
    globalThis.destroyFestivalGlobe = function () {};

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadIndex);
    } else {
        loadIndex();
    }
})();
