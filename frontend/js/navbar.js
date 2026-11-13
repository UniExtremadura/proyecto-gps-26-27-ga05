/**
 * Navbar Management
 * Actualiza los links del navbar según autenticación y rol
 */

// Actualizar navbar cuando Auth cambia
function updateNavbarUI() {
    updateNavbarLinks();
    updateNavbarUser();
}

function buildAvatarFallback(name) {
    const safeName = String(name || 'U').trim() || 'U';
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(safeName)}&background=00d4ff&color=000000&bold=true&size=64`;
}

/**
 * Actualiza los links del navbar según el rol del usuario
 */
function updateNavbarLinks() {
    const navbarLinksContainer = document.querySelector('.navbar-links');
    if (!navbarLinksContainer) return;
    
    const user = AUTH.getUser();
    let links = [];
    
    if (!user) {
        // Visitante (no autenticado)
        links = [
            { text: 'EVENTOS', href: '#eventos' },
            { text: 'TIENDA', href: '#tienda' }
        ];
    } else if (user.role === 'proveedor') {
        // Proveedor
        links = [
            { text: 'EVENTOS', href: '#eventosProveedor' },
            { text: 'TIENDA', href: '#tiendaProveedor' },
            { text: 'RESERVAS', href: '#provider-bookings' },
            { text: 'CARRITO', href: '#carrito' }
        ];
    } else if (user.role === 'gestor') {
        // Gestor
        links = [
            { text: 'FESTIVALES', href: '#manager-events' },
            { text: 'ARTISTAS', href: '#manager-artists' },
            { text: 'TIENDA', href: '#manager-tienda' }
        ];
    } else if (user.role === 'admin') {
        // Administrador
        links = [
            { text: 'PANEL', href: '#admin-panel' },
            { text: 'ANALÍTICA', href: '#admin-analytics' },
            { text: 'FESTIVALES', href: '#manager-events' },
            { text: 'TIENDA', href: '#manager-tienda' }
        ];
    } else {
        // Cliente (autenticado )
        links = [
            { text: 'EVENTOS', href: '#eventos' },
            { text: 'TIENDA', href: '#tienda' },
            { text: 'CARRITO', href: '#carrito' }
        ];
    }
    
    // Generar HTML
    const linksHTML = links.map(link => 
        `<a href="${link.href}" data-page="${link.href.substr(1)}">${link.text}</a>`
    ).join('');
    
    navbarLinksContainer.innerHTML = linksHTML;
}

/**
 * Actualiza el saludo y avatar
 */
function updateNavbarUser() {
    const userGreeting = document.getElementById('user-greeting');
    const avatarLink = document.getElementById('user-avatar-link');
    const avatarImg = avatarLink?.querySelector('img');
    
    const user = AUTH.getUser();
    
    if (user && user.name) {
        // Usuario autenticado
        if (userGreeting) {
            userGreeting.textContent = `Hola, ${user.name}`;
        }

        if (avatarImg) {
            const avatarSrc = String(user.profile_image_url || '').trim() || buildAvatarFallback(user.name);
            avatarImg.src = avatarSrc;
            avatarImg.alt = `Avatar de ${user.name}`;
            avatarImg.onerror = () => {
                avatarImg.onerror = null;
                avatarImg.src = buildAvatarFallback(user.name);
            };
        }
        
        if (avatarLink) {
            // Navegar a perfil según rol
            let profilePage = 'client-profile';
            if (user.role === 'proveedor') {
                profilePage = 'provider-profile';
            } else if (user.role === 'gestor') {
                profilePage = 'manager-profile';
            } else if (user.role === 'admin') {
                profilePage = 'admin-panel';
            }
            avatarLink.setAttribute('href', `#${profilePage}`);
            avatarLink.setAttribute('data-page', profilePage);
        }
    } else {
        // No autenticado
        if (userGreeting) {
            userGreeting.textContent = 'Hola, Visitante';
        }

        if (avatarImg) {
            avatarImg.src = './assets/img/User.png';
            avatarImg.alt = 'User';
            avatarImg.onerror = null;
        }
        
        if (avatarLink) {
            avatarLink.setAttribute('href', '#login');
            avatarLink.setAttribute('data-page', 'login');
        }
    }
}

/**
 * Setup para búsqueda de festivales con dropdown predictivo
 * Funciona como el selector de artistas: muestra todos al hacer click y filtra conforme escribes
 */
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (!searchInput || !searchResults) return;
    
    let allEvents = []; // Cache de todos los eventos
    let searchTimeout;
    
    // Función para obtener todos los eventos
    async function loadAllEvents() {
        try {
            const response = await fetch('http://subsonic-backend-pi.asatfyfmapbdgdfk.polandcentral.azurecontainer.io:8000/api/events');
            if (!response.ok) return [];
            const result = await response.json();
            return result.data || [];
        } catch (error) {
            console.error('Error cargando eventos:', error);
            return [];
        }
    }
    
    // Función para filtrar y renderizar eventos
    function filterAndRenderEvents(query = '') {
        let filtered = allEvents;
        
        if (query.trim().length > 0) {
            const qLower = query.toLowerCase();
            filtered = allEvents.filter(event => {
                const name = (event.name || event.title || event.artist || '').toLowerCase();
                const location = (event.location || event.loc || '').toLowerCase();
                const description = (event.description || '').toLowerCase();
                return name.includes(qLower) || location.includes(qLower) || description.includes(qLower);
            });
        }
        
        if (filtered.length === 0) {
            searchResults.innerHTML = '<div class="search-no-results-navbar">No hay festivales disponibles</div>';
        } else {
            // Ordenar por relevancia si hay query
            if (query.trim().length > 0) {
                const qLower = query.toLowerCase();
                filtered.sort((a, b) => {
                    const aName = (a.name || a.title || a.artist || '').toLowerCase();
                    const bName = (b.name || b.title || b.artist || '').toLowerCase();
                    const aStarts = aName.startsWith(qLower) ? 0 : 1;
                    const bStarts = bName.startsWith(qLower) ? 0 : 1;
                    return aStarts - bStarts;
                });
            }
            
            const html = filtered.map(event => {
                const eventName = event.name || event.title || event.artist || 'Sin nombre';
                const eventLocation = event.location || event.loc || 'Ubicación no disponible';
                const eventDate = event.date || event.start_date || 'Fecha no disponible';
                const eventImage = event.cardImg || event.heroImg || event.image || '';
                const eventId = event.id;
                
                return `
                    <div class="search-result-event" onclick="navigateToEventDetail('${eventId}')">
                        <div class="search-result-event-image" style="background-image: url('${sanitizeHtml(eventImage)}'); background-size: cover; background-position: center;"></div>
                        <div class="search-result-event-info">
                            <div class="search-result-event-title">${sanitizeHtml(eventName)}</div>
                            <div class="search-result-event-location">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                                    <circle cx="12" cy="10" r="3"></circle>
                                </svg>
                                ${sanitizeHtml(eventLocation)}
                            </div>
                            <div class="search-result-event-date">${eventDate}</div>
                        </div>
                    </div>
                `;
            }).join('');
            
            searchResults.innerHTML = html;
        }
        
        searchResults.style.display = 'block';
    }
    
    // Focus/Click: cargar todos los eventos
    searchInput.addEventListener('focus', async () => {
        if (allEvents.length === 0) {
            allEvents = await loadAllEvents();
        }
        filterAndRenderEvents();
    });
    
    // Input: filtrar conforme escribe
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value;
        
        clearTimeout(searchTimeout);
        searchTimeout = globalThis.setTimeout(() => {
            filterAndRenderEvents(query);
        }, 100);
    });
    
    // Enter: aplicar filtro y navegar a festivales
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const query = searchInput.value.trim();
            if (query) {
                performEventSearch(query);
                searchInput.value = '';
                searchResults.style.display = 'none';
            }
        }
    });
    
    // Cerrar dropdown al hacer click fuera
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.navbar-search')) {
            searchResults.style.display = 'none';
        }
    });
    
    // Limpiar al perder foco
    searchInput.addEventListener('blur', () => {
        globalThis.setTimeout(() => {
            searchResults.style.display = 'none';
        }, 200);
    });
}

/**
 * Navega directamente al detalle del evento seleccionado
 */
function navigateToEventDetail(eventId) {
    const user = AUTH.getUser();
    let targetPage = 'eventos';
    
    if (user && user.role === 'gestor') {
        targetPage = 'manager-event-detail';
    } else if (user && user.role === 'proveedor') {
        targetPage = 'eventosProveedor';
    }
    
    // Navegar a detalle del evento
    globalThis.location.hash = `#${targetPage}?id=${eventId}`;
    
    // Limpiar búsqueda
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    if (searchInput) searchInput.value = '';
    if (searchResults) searchResults.style.display = 'none';
}

/**
 * Realiza búsqueda de eventos y redirija a festivales con filtro
 */
function performEventSearch(query) {
    if (!query || query.trim().length === 0) {
        globalThis.location.hash = '#eventos';
        return;
    }
    
    // Guardar término de búsqueda en sessionStorage
    sessionStorage.setItem('eventSearchQuery', query.trim());
    
    // Determinar página según rol
    const user = AUTH.getUser();
    let targetPage = '#eventos';
    
    if (user && user.role === 'gestor') {
        targetPage = '#manager-events';
    } else if (user && user.role === 'proveedor') {
        targetPage = '#eventosProveedor';
    }
    
    globalThis.location.hash = targetPage;
}

/**
 * Sanitiza HTML para evitar inyecciones
 */
function sanitizeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Inicializar navbar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    updateNavbarUI();
    setupSearch();
});
