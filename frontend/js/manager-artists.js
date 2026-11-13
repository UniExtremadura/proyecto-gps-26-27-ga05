/** Panel de gestión de artistas para gestores/administradores. */
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

    function setStatus(message, isError = false) {
        const node = document.getElementById('artistManagerStatus');
        if (!node) return;
        node.textContent = message || '';
        node.classList.toggle('error', isError);
        node.classList.toggle('success', !isError && Boolean(message));
    }

    function render() {
        const grid = document.getElementById('managerArtistsGrid');
        if (!grid) return;
        if (!artists.length) {
            grid.innerHTML = '<p class="empty-state">Todavía no hay artistas registrados.</p>';
            return;
        }
        grid.innerHTML = artists.map((artist) => `
            <article class="manager-card">
                <div class="manager-card-image">
                    ${artist.image ? `<img src="${escapeHtml(artist.image)}" alt="${escapeHtml(artist.name)}">` : '<span>🎤</span>'}
                </div>
                <div class="manager-card-body">
                    <h3>${escapeHtml(artist.name || 'Artista')}</h3>
                    <p>${escapeHtml(artist.genre || 'Música')} · ${escapeHtml(artist.country || 'Internacional')}</p>
                    <p class="manager-card-bio">${escapeHtml(artist.bio || '')}</p>
                    <div class="manager-card-actions">
                        <button type="button" data-edit-artist="${escapeHtml(artist.slug || artist.id || '')}">EDITAR</button>
                        <button type="button" class="danger" data-delete-artist="${escapeHtml(artist.slug || artist.id || '')}">ELIMINAR</button>
                    </div>
                </div>
            </article>
        `).join('');

        grid.querySelectorAll('[data-edit-artist]').forEach((button) => {
            button.addEventListener('click', () => editArtist(button.dataset.editArtist));
        });
        grid.querySelectorAll('[data-delete-artist]').forEach((button) => {
            button.addEventListener('click', () => deleteArtist(button.dataset.deleteArtist));
        });
    }

    async function load() {
        const grid = document.getElementById('managerArtistsGrid');
        if (!grid) return;
        grid.innerHTML = '<p class="loading-state">Cargando artistas...</p>';
        try {
            const response = await globalThis.SubsonicAPI.getAllArtists();
            artists = Array.isArray(response?.data) ? response.data : [];
            render();
        } catch (error) {
            grid.innerHTML = `<p class="empty-state">No se pudieron cargar los artistas: ${escapeHtml(error.message)}</p>`;
        }
    }

    function editArtist(slug) {
        const artist = artists.find((item) => String(item.slug || item.id) === String(slug));
        if (!artist) return;
        document.getElementById('artistId').value = artist.slug || artist.id || '';
        document.getElementById('artistName').value = artist.name || '';
        document.getElementById('artistGenre').value = artist.genre || '';
        document.getElementById('artistCountry').value = artist.country || '';
        document.getElementById('artistImage').value = artist.image || '';
        document.getElementById('artistBio').value = artist.bio || '';
        setStatus(`Editando ${artist.name || slug}`);
    }

    async function removeArtist(slug) {
        if (!await globalThis.showSubsonicConfirm(`¿Eliminar el artista "${slug}"?`, { danger: true, confirmText: 'Eliminar' })) return;
        try {
            await globalThis.SubsonicAPI.deleteArtist(slug);
            artists = artists.filter((item) => String(item.slug || item.id) !== String(slug));
            render();
            setStatus('Artista eliminado.');
        } catch (error) {
            setStatus(error.message || 'No se pudo eliminar el artista.', true);
        }
    }

    async function save(event) {
        event?.preventDefault?.();
        const id = document.getElementById('artistId')?.value.trim();
        const payload = {
            name: document.getElementById('artistName')?.value.trim(),
            genre: document.getElementById('artistGenre')?.value.trim(),
            country: document.getElementById('artistCountry')?.value.trim(),
            image: document.getElementById('artistImage')?.value.trim(),
            bio: document.getElementById('artistBio')?.value.trim()
        };
        if (!payload.name) {
            setStatus('El nombre del artista es obligatorio.', true);
            return;
        }
        try {
            setStatus('Guardando...');
            if (id) await globalThis.SubsonicAPI.updateArtist(id, payload);
            else await globalThis.SubsonicAPI.createArtist(payload);
            document.getElementById('artistManagerForm')?.reset();
            document.getElementById('artistId').value = '';
            await load();
            setStatus(id ? 'Artista actualizado.' : 'Artista creado.');
        } catch (error) {
            setStatus(error.message || 'No se pudo guardar el artista.', true);
        }
    }

    function bind() {
        if (!document.getElementById('managerArtistsGrid')) return;
        document.getElementById('artistManagerForm')?.addEventListener('submit', save);
        load();
    }

    globalThis.load_manager_artists = bind;
    globalThis.deleteArtist = removeArtist;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bind);
    } else {
        bind();
    }
})();
