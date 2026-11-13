/**
 * Router SPA - Gestiona navegación entre páginas sin recargar
 * Comunicación por HTTP con cookies automáticas
 */

globalThis.showSubsonicConfirm = function(message, options = {}) {
    const {
        title = 'Confirmar accion',
        confirmText = 'Confirmar',
        cancelText = 'Cancelar',
        danger = false
    } = options;

    return new Promise((resolve) => {
        const existing = document.getElementById('subsonicConfirmOverlay');
        if (existing) existing.remove();

        const overlay = document.createElement('div');
        overlay.id = 'subsonicConfirmOverlay';
        overlay.className = 'subsonic-confirm-overlay';

        overlay.innerHTML = `
            <div class="subsonic-confirm-modal" role="dialog" aria-modal="true" aria-labelledby="subsonicConfirmTitle">
                <h3 id="subsonicConfirmTitle">${title}</h3>
                <p>${message}</p>
                <div class="subsonic-confirm-actions">
                    <button type="button" class="subsonic-confirm-btn subsonic-confirm-cancel">${cancelText}</button>
                    <button type="button" class="subsonic-confirm-btn ${danger ? 'subsonic-confirm-danger' : 'subsonic-confirm-ok'}">${confirmText}</button>
                </div>
            </div>
        `;

        const close = (result) => {
            if (!overlay.isConnected) return;
            overlay.remove();
            resolve(result);
        };

        overlay.addEventListener('click', (event) => {
            if (event.target === overlay) close(false);
        });

        const cancelBtn = overlay.querySelector('.subsonic-confirm-cancel');
        const okBtn = overlay.querySelector('.subsonic-confirm-ok, .subsonic-confirm-danger');
        cancelBtn?.addEventListener('click', () => close(false));
        okBtn?.addEventListener('click', () => close(true));

        const onKeyDown = (event) => {
            if (event.key === 'Escape') {
                document.removeEventListener('keydown', onKeyDown);
                close(false);
            }
        };
        document.addEventListener('keydown', onKeyDown);

        document.body.appendChild(overlay);
        okBtn?.focus();
    });
};

globalThis.showSubsonicAlert = function(message, options = {}) {
    const {
        title = 'Información',
        buttonText = 'Aceptar',
        danger = false
    } = options;

    return new Promise((resolve) => {
        const existing = document.getElementById('subsonicAlertOverlay');
        if (existing) existing.remove();

        const overlay = document.createElement('div');
        overlay.id = 'subsonicAlertOverlay';
        overlay.className = 'subsonic-confirm-overlay';

        overlay.innerHTML = `
            <div class="subsonic-confirm-modal" role="dialog" aria-modal="true" aria-labelledby="subsonicAlertTitle">
                <h3 id="subsonicAlertTitle">${title}</h3>
                <p>${String(message ?? '')}</p>
                <div class="subsonic-confirm-actions">
                    <button type="button" class="subsonic-confirm-btn ${danger ? 'subsonic-confirm-danger' : 'subsonic-confirm-ok'}">${buttonText}</button>
                </div>
            </div>
        `;

        const close = () => {
            if (!overlay.isConnected) return;
            overlay.remove();
            resolve(true);
        };

        overlay.addEventListener('click', (event) => {
            if (event.target === overlay) close();
        });

        const okBtn = overlay.querySelector('.subsonic-confirm-ok, .subsonic-confirm-danger');
        okBtn?.addEventListener('click', close);

        const onKeyDown = (event) => {
            if (event.key === 'Escape' || event.key === 'Enter') {
                document.removeEventListener('keydown', onKeyDown);
                close();
            }
        };
        document.addEventListener('keydown', onKeyDown);

        document.body.appendChild(overlay);
        okBtn?.focus();
    });
};

globalThis.showSubsonicPrompt = function(message, defaultValue = '', options = {}) {
    const {
        title = 'Introduce un valor',
        confirmText = 'Aceptar',
        cancelText = 'Cancelar'
    } = options;

    return new Promise((resolve) => {
        const existing = document.getElementById('subsonicPromptOverlay');
        if (existing) existing.remove();

        const overlay = document.createElement('div');
        overlay.id = 'subsonicPromptOverlay';
        overlay.className = 'subsonic-confirm-overlay';

        overlay.innerHTML = `
            <div class="subsonic-confirm-modal" role="dialog" aria-modal="true" aria-labelledby="subsonicPromptTitle">
                <h3 id="subsonicPromptTitle">${title}</h3>
                <p>${String(message ?? '')}</p>
                <input id="subsonicPromptInput" type="text" value="${String(defaultValue ?? '').replaceAll('"', '&quot;')}" style="width:100%;margin-top:8px;padding:10px 12px;border-radius:10px;border:1px solid rgba(148,163,184,.35);background:rgba(15,23,42,.7);color:#e2e8f0;outline:none;" />
                <div class="subsonic-confirm-actions" style="margin-top:14px;">
                    <button type="button" class="subsonic-confirm-btn subsonic-confirm-cancel">${cancelText}</button>
                    <button type="button" class="subsonic-confirm-btn subsonic-confirm-ok">${confirmText}</button>
                </div>
            </div>
        `;

        const input = () => overlay.querySelector('#subsonicPromptInput');

        const close = (result) => {
            if (!overlay.isConnected) return;
            overlay.remove();
            resolve(result);
        };

        overlay.addEventListener('click', (event) => {
            if (event.target === overlay) close(null);
        });

        const cancelBtn = overlay.querySelector('.subsonic-confirm-cancel');
        const okBtn = overlay.querySelector('.subsonic-confirm-ok');

        cancelBtn?.addEventListener('click', () => close(null));
        okBtn?.addEventListener('click', () => close(String(input()?.value ?? '')));

        const onKeyDown = (event) => {
            if (event.key === 'Escape') {
                document.removeEventListener('keydown', onKeyDown);
                close(null);
            }
            if (event.key === 'Enter') {
                document.removeEventListener('keydown', onKeyDown);
                close(String(input()?.value ?? ''));
            }
        };
        document.addEventListener('keydown', onKeyDown);

        document.body.appendChild(overlay);
        input()?.focus();
        input()?.select();
    });
};

globalThis.alert = function(message) {
    globalThis.showSubsonicAlert(String(message ?? ''));
};

const CART_STORAGE_KEY = 'subsonic_carrito';

globalThis.showAuthRequiredModal = function(options = {}) {
    const {
        title = 'Necesitas una cuenta para comprar',
        message = 'Regístrate o inicia sesión para añadir productos al carrito y completar tu compra.'
    } = options;

    const existing = document.getElementById('subsonicAuthOverlay');
    if (existing) existing.remove();

    const overlay = document.createElement('div');
    overlay.id = 'subsonicAuthOverlay';
    overlay.className = 'subsonic-confirm-overlay';

    overlay.innerHTML = `
        <div class="subsonic-confirm-modal subsonic-auth-modal" role="dialog" aria-modal="true" aria-labelledby="subsonicAuthTitle">
            <button type="button" class="subsonic-auth-close" aria-label="Cerrar">&times;</button>
            <h3 id="subsonicAuthTitle">${title}</h3>
            <p>${message}</p>
            <div class="subsonic-confirm-actions">
                <button type="button" class="subsonic-confirm-btn subsonic-confirm-cancel">Cerrar</button>
                <button type="button" class="subsonic-confirm-btn subsonic-confirm-ok subsonic-auth-register">Registrarme</button>
            </div>
        </div>
    `;

    const closeModal = () => {
        if (overlay.isConnected) overlay.remove();
    };

    overlay.addEventListener('click', (event) => {
        if (event.target === overlay) closeModal();
    });

    overlay.querySelector('.subsonic-auth-close')?.addEventListener('click', closeModal);
    overlay.querySelector('.subsonic-confirm-cancel')?.addEventListener('click', closeModal);
    overlay.querySelector('.subsonic-auth-register')?.addEventListener('click', () => {
        closeModal();
        globalThis.location.hash = 'register';
    });

    const onKeyDown = (event) => {
        if (event.key === 'Escape') {
            document.removeEventListener('keydown', onKeyDown);
            closeModal();
        }
    };
    document.addEventListener('keydown', onKeyDown);

    document.body.appendChild(overlay);
};

globalThis.ensureBuyerRole = function() {
    const role = AUTH.getRole();
    if (role === 'cliente' || role === 'proveedor') {
        return true;
    }
    globalThis.showAuthRequiredModal();
    return false;
};

globalThis.SubsonicCart = {
    key: CART_STORAGE_KEY,

    getItems() {
        const raw = localStorage.getItem(this.key);
        if (!raw) return [];
        try {
            const parsed = JSON.parse(raw);
            if (!Array.isArray(parsed)) return [];
            return parsed.map((item) => this.normalizeItem(item)).filter(Boolean);
        } catch {
            return [];
        }
    },

    saveItems(items) {
        localStorage.setItem(this.key, JSON.stringify(Array.isArray(items) ? items : []));
    },

    addItem(item) {
        const normalized = this.normalizeItem(item);
        if (!normalized) return;

        const items = this.getItems();
        const sameIndex = items.findIndex((existing) => this.getIdentity(existing) === this.getIdentity(normalized));

        if (sameIndex >= 0) {
            items[sameIndex].qty += normalized.qty;
            items[sameIndex].quantity = items[sameIndex].qty;
            // Mantener/recuperar metadata visual si el item previo no la tenía.
            if (!items[sameIndex].image && normalized.image) {
                items[sameIndex].image = normalized.image;
            }
            if ((!Array.isArray(items[sameIndex].images) || items[sameIndex].images.length === 0) && Array.isArray(normalized.images) && normalized.images.length > 0) {
                items[sameIndex].images = normalized.images;
            }
        } else {
            items.push(normalized);
        }

        this.saveItems(items);
    },

    normalizeItem(item) {
        if (!item || typeof item !== 'object') return null;

        const parsedPrice = Number(item.price ?? item.unit_price ?? 0);
        const parsedQty = Number(item.qty ?? item.quantity ?? 1);
        const price = Number.isFinite(parsedPrice) ? parsedPrice : 0;
        const qty = Number.isFinite(parsedQty) && parsedQty > 0 ? parsedQty : 1;

        const name = String(item.name || item.title || item.id || 'Elemento').trim();
        const type = String(item.type || 'Merch').trim();
        const category = String(item.category || item.tipo || type).trim();
        const id = String(item.id || `${type}_${Date.now()}`).trim();
        let images = [];
        if (Array.isArray(item.images)) {
            images = item.images.filter((img) => typeof img === 'string' && img.trim());
        } else if (typeof item.images === 'string' && item.images.trim()) {
            images = [item.images.trim()];
        }
        const image = String(item.image || item.image_url || item.cardImg || item.heroImg || images[0] || '').trim();

        return {
            ...item,
            id,
            name,
            type,
            category,
            price,
            qty,
            quantity: qty,
            image,
            images
        };
    },

    getIdentity(item) {
        const color = item.color || '';
        const eventId = item.event_id || '';
        return `${item.type}|${item.id}|${color}|${eventId}`;
    }
};

const App = {
    BASE_URL: 'http://subsonic-backend-pi.asatfyfmapbdgdfk.polandcentral.azurecontainer.io:8000',
    API_URL: 'http://subsonic-backend-pi.asatfyfmapbdgdfk.polandcentral.azurecontainer.io:8000/api',
    APP_CONTAINER: null, // Se inicializa en init()
    CURRENT_PAGE: null,
    DYNAMIC_SCRIPT_TAG: null,
    LOADED_SCRIPTS: new Set(),
    INDEX_TEMPLATE_HTML: '',
    NAVIGATION_SEQ: 0,
    ROLE_ALLOWED_PAGES: {
        visitante: new Set(['index', 'login', 'register', 'oauth-callback', 'eventos', 'tienda', 'producto', 'artistas', 'artista']),
        cliente: new Set(['index', 'eventos', 'tienda', 'carrito', 'client-profile', 'historial', 'producto', 'artistas', 'artista']),
        proveedor: new Set(['index', 'eventosProveedor', 'tiendaProveedor', 'carrito', 'historial', 'provider-profile', 'productoProveedor', 'ventas', 'provider-bookings', 'provider-history', 'artistas', 'artista']),
        gestor: new Set(['index', 'manager-profile', 'manager-events', 'manager-artists', 'manager-tienda', 'manager-event-detail', 'manager-artist-detail', 'manager-producto-detalle', 'gestor-eventos', 'artista'])
    },

    /**
     * Inicializar la aplicación
     */
    init: function() {
        console.log('Subsonic Festival - SPA iniciado');
        
        // Asegurar que el contenedor de la app existe
        this.APP_CONTAINER = document.getElementById('main-content');
        if (!this.APP_CONTAINER) {
            console.error('ERROR: No se encontró #main-content');
            return;
        }
        console.log('✓ APP_CONTAINER encontrado:', this.APP_CONTAINER);

        // Guardar el HTML inicial para poder restaurar correctamente #index
        this.INDEX_TEMPLATE_HTML = this.APP_CONTAINER.innerHTML;

        // Verificar autenticación al cargar
        this.checkAuth();

        // Configurar event listeners para navegación
        this.setupNavigation();

        // Cargar página inicial
        const initialPage = globalThis.location.hash.slice(1) || 'index';
        console.log('Página inicial:', initialPage);
        this.navigate(initialPage);

        // Escuchar cambios de hash: recargar por defecto (para back/forward),
        // pero suprimir la recarga si la navegación la inició nuestro handler (flag en sessionStorage)
        globalThis.addEventListener('hashchange', () => {
            const page = globalThis.location.hash.slice(1) || 'index';
            console.log('Hash cambió a:', page);
            try {
                const suppress = sessionStorage.getItem('suppressHashReload');
                if (suppress) {
                    // Navegación iniciada por nuestro click handler: eliminar flag y no recargar aquí
                    sessionStorage.removeItem('suppressHashReload');
                    console.log('Suppressing hashchange reload (programmatic navigation)');
                    return;
                }

                // Para navegación por historial (back/forward), forzar recarga completa
                globalThis.location.reload();
            } catch (err) {
                console.error('Error handling hashchange reload:', err);
            }
        });
    },

    /**
     * Navegar a una página
     * @param {string} page - Nombre de la página (puede incluir subcarpeta: "artistas/adam")
     */
    navigate: function(page) {
        const parsed = this.parsePage(page);
        const normalizedPage = this.normalizePage(parsed.page);
        const normalizedRoute = parsed.query ? `${normalizedPage}?${parsed.query}` : normalizedPage;

        if (normalizedPage !== 'index' && typeof globalThis.destroyFestivalGlobe === 'function') {
            globalThis.destroyFestivalGlobe();
        }

        const access = this.getAccessDecision(normalizedPage);
        if (!access.allowed) {
            console.warn(`Acceso denegado a '${normalizedPage}' para rol '${access.role}'. Redirigiendo a '${access.redirectPage}'.`);
            if (access.redirectPage && access.redirectPage !== normalizedPage) {
                this.NAVIGATION_SEQ += 1;
                this.CURRENT_PAGE = access.redirectPage;
                this.syncUrlQuery(access.redirectPage, '');
                return this.navigate(access.redirectPage);
            }
            return;
        }

        console.log(`Navegando a: ${page} (normalizada: ${normalizedRoute})`);
        this.NAVIGATION_SEQ += 1;
        this.CURRENT_PAGE = normalizedPage;
        this.syncUrlQuery(normalizedPage, parsed.query);

        // Si es index, solo ejecutar script y actualizar navbar
        if (normalizedPage === 'index') {
            console.log('✓ Página index - mostrando contenido por defecto');
            if (this.APP_CONTAINER && this.INDEX_TEMPLATE_HTML) {
                this.APP_CONTAINER.innerHTML = this.INDEX_TEMPLATE_HTML;
            }
            this.loadPageStyles(normalizedPage);
            this.loadPageScript(normalizedPage, this.NAVIGATION_SEQ);
            this.updateNavbarActive(normalizedPage);
            globalThis.scrollTo(0, 0);
            return;
        }

        // Para otras páginas, cargar desde ./paginas/.
        // Algunas rutas mantienen nombre interno distinto al archivo HTML físico.
        const htmlTemplateMap = {
            ventas: 'HistorialVentasProveedor'
        };
        const htmlPageName = htmlTemplateMap[normalizedPage] || normalizedPage;
        const filePath = `./paginas/${htmlPageName}.html`;
        const fetchPath = `${filePath}?_=${Date.now()}`;
        console.log(`Fetching: ${filePath}`);

        // Cargar el contenido
        fetch(fetchPath)
            .then(response => {
                console.log(`Response status: ${response.status}`);
                if (!response.ok) {
                    throw new Error(`Página ${page} no encontrada (${response.status})`);
                }
                return response.text();
            })
            .then(html => {
                console.log(`Contenido cargado, tamaño: ${html.length} bytes`);
                // IMPORTANTE: Extraer solo el contenido del <body> para evitar duplicar navbar
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                
                // Para otras páginas, extraer solo divs principales (sin navbar, sin scripts)
                // Excluir nav, header, canvas, script
                const navs = doc.querySelectorAll('nav');
                navs.forEach(nav => nav.remove());
                
                const scripts = doc.querySelectorAll('script');
                scripts.forEach(script => script.remove());
                
                const canvases = doc.querySelectorAll('canvas');
                canvases.forEach((canvasEl) => {
                    if (canvasEl.id !== 'neural-glow-canvas') {
                        canvasEl.remove();
                    }
                });
                
                const contentToInsert = doc.body.innerHTML;

                // Reemplazar contenido
                if (this.APP_CONTAINER) {
                    this.APP_CONTAINER.innerHTML = contentToInsert;
                    console.log('✓ Contenido insertado en APP_CONTAINER');
                    globalThis.scrollTo(0, 0);
                } else {
                    console.warn('#main-content no encontrado');
                }

                // Cargar CSS específico de la página si existe
                this.loadPageStyles(normalizedPage);
                
                // Reajustar paths de imágenes y recursos
                this.fixResourcePaths(this.APP_CONTAINER);

                // Ejecutar script de la página si existe
                this.loadPageScript(normalizedPage, this.NAVIGATION_SEQ);

                if (typeof globalThis.initNeuralGlow === 'function') {
                    globalThis.initNeuralGlow();
                }

                // Actualizar navbar activo
                this.updateNavbarActive(normalizedPage);
            })
            .catch(error => {
                console.error('Error cargando página:', error);
                if (this.APP_CONTAINER) {
                    this.APP_CONTAINER.innerHTML = `
                        <div class="error-page" style="padding: 40px; text-align: center;">
                            <h1>Página no encontrada</h1>
                            <p>${error.message}</p>
                            <p><small>Intenta navegar a: eventos, tienda, carrito, login, etc.</small></p>
                            <a href="#index" style="color: #00d4ff; text-decoration: underline; font-weight: bold;">← Volver al inicio</a>
                        </div>
                    `;
                }
            });
    },

    /**
     * Cargar CSS específico de la página si existe
     * @param {string} page - Nombre de la página
     */
    loadPageStyles: function(page) {
        if (page === 'index') return;

        const cssMap = {
            artista: './css/artist.css',
            'manager-producto-detalle': './css/productoProveedor.css'
        };

        let cssPath = cssMap[page] || `./css/${page}.css`;
        if (page.startsWith('artistas/')) {
            cssPath = './css/artist.css';
        }
        
        // Verificar si ya está cargado
        const existing = document.querySelector(`link[href="${cssPath}"]`);
        if (existing) return;
        
        // Intentar cargar el CSS
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = cssPath;
        link.onerror = () => {
            console.log(`CSS no encontrado para página: ${page}`);
        };
        document.head.appendChild(link);
    },

    /**
     * Arreglar paths de recursos (imágenes, etc.) en el contenido cargado
     * @param {Element} container - Contenedor con el contenido
     */
    fixResourcePaths: function(container) {
        // Arreglar src de imágenes
        container.querySelectorAll('img').forEach(img => {
            if (img.src && !img.src.startsWith('http')) {
                // Si comienza con /assets/, arreglarlo a ./assets/
                if (img.src.includes('/assets/')) {
                    img.src = img.src.replace(/^.*\/assets\//, './assets/');
                }
            }
        });
        
        // Arreglar href en links
        container.querySelectorAll('a[href]').forEach(a => {
            const href = a.getAttribute('href');
            if (!href) return;
            
            // Si empieza con paginas/, convertir a #
            if (href.includes('paginas/')) {
                const page = href.replace(/.*paginas\//, '').replace('.html', '');
                a.setAttribute('href', `#${page}`);
                a.dataset.page = page;
            }
        });
    },

    /**
     * Cargar y ejecutar el script de la página
     * @param {string} page - Nombre de la página
     */
    loadPageScript: function(page, navSeq) {
        const scriptPath = this.resolveScriptPath(page);
        if (!scriptPath) {
            console.log(`No hay script asociado para la página: ${page}`);
            return;
        }

        if (this.LOADED_SCRIPTS.has(scriptPath)) {
            // Evita redeclaraciones globales (const/let) al volver a entrar en la misma página.
            this.executePageLoaderWithRetry(page, navSeq);
            return;
        }

        const originalAddEventListener = document.addEventListener.bind(document);
        document.addEventListener = function(type, listener, options) {
            if (type === 'DOMContentLoaded') {
                try {
                    listener.call(document, new Event('DOMContentLoaded'));
                } catch (error) {
                    console.error('Error ejecutando listener DOMContentLoaded:', error);
                }
                return;
            }
            return originalAddEventListener(type, listener, options);
        };

        const script = document.createElement('script');
        script.src = scriptPath;
        script.onload = () => {
            document.addEventListener = originalAddEventListener;
            this.LOADED_SCRIPTS.add(scriptPath);
            this.executePageLoaderWithRetry(page, navSeq);
        };
        script.onerror = () => {
            document.addEventListener = originalAddEventListener;
            console.warn(`Script no encontrado para página: ${page} (${scriptPath})`);
            this.executePageLoaderWithRetry(page, navSeq);
        };

        document.body.appendChild(script);
        this.DYNAMIC_SCRIPT_TAG = script;
    },

    normalizePage: function(page) {
        if (!page || page === '') return 'index';
        if (page.startsWith('#')) {
            return this.normalizePage(page.slice(1));
        }
        if (page.includes('/paginas/')) {
            const onlyPage = page.split('/paginas/')[1] || page;
            return this.normalizePage(onlyPage);
        }
        if (page.endsWith('.html')) {
            return this.normalizePage(page.replace('.html', ''));
        }
        if (page.startsWith('artistas-')) {
            return 'artista';
        }
        return page;
    },

    parsePage: function(rawPage) {
        const pageStr = (rawPage || '').trim();
        if (!pageStr) {
            return { page: 'index', query: '' };
        }

        if (pageStr.startsWith('artistas/')) {
            const slug = pageStr.split('/').slice(1).join('/');
            return { page: 'artista', query: `slug=${encodeURIComponent(slug)}` };
        }

        if (pageStr.startsWith('artistas-')) {
            const slug = pageStr.replace('artistas-', '');
            return { page: 'artista', query: `slug=${encodeURIComponent(slug)}` };
        }

        const separatorIndex = pageStr.indexOf('?');
        if (separatorIndex === -1) {
            return { page: pageStr, query: '' };
        }

        return {
            page: pageStr.slice(0, separatorIndex),
            query: pageStr.slice(separatorIndex + 1)
        };
    },

    syncUrlQuery: function(page, query) {
        const cleanQuery = query ? `?${query}` : '';
        const hash = `#${page}${cleanQuery}`;
        const nextUrl = `${globalThis.location.pathname}${cleanQuery}${hash}`;
        globalThis.history.replaceState(null, '', nextUrl);
    },

    getRoleHomePage: function(role) {
        return 'index';
    },

    getAccessDecision: function(page) {
        const user = AUTH.getUser();
        const role = user?.role || 'visitante';
        const rolePages = this.ROLE_ALLOWED_PAGES[role] || this.ROLE_ALLOWED_PAGES.visitante;

        // Compatibilidad con rutas antiguas de artistas
        if (page.startsWith('artistas/')) {
            return { allowed: true, role, redirectPage: null };
        }

        // Si está logeado, bloquear login/register
        if (user && (page === 'login' || page === 'register')) {
            return { allowed: false, role, redirectPage: this.getRoleHomePage(role) };
        }

        if (rolePages.has(page)) {
            return { allowed: true, role, redirectPage: null };
        }

        return { allowed: false, role, redirectPage: this.getRoleHomePage(role) };
    },

    resolveScriptPath: function(page) {
        const scriptMap = {
            index: './js/main.js',
            login: './js/login.js',
            register: './js/register.js',
            eventos: './js/eventos.js',
            eventosProveedor: './js/eventosProveedor.js',
            tienda: './js/tienda.js',
            tiendaProveedor: './js/tiendaProveedor.js',
            carrito: './js/carrito.js',
            'client-profile': './js/client-profile.js',
            'provider-profile': './js/provider-profile.js',
            'manager-profile': './js/manager-profile.js',
            historial: './js/historial.js',
            'gestor-eventos': './js/gestor-eventos.js',
            'manager-events': './js/manager-events.js',
            'manager-artists': './js/manager-artists.js',
            'manager-event-detail': './js/manager-event-detail.js',
            'manager-artist-detail': './js/manager-artist-detail.js',
            'manager-tienda': './js/manager-tienda.js',
            'manager-producto-detalle': './js/manager-producto-detalle.js',
            producto: './js/producto.js',
            productoProveedor: './js/productoProveedor.js',
            ventas: './js/ventas.js',
            'provider-bookings': './js/provider-bookings.js',
            artista: './js/artista.js'
        };

        return scriptMap[page] || null;
    },

    executePageLoader: function(page) {
        const functionName = `load_${page.replaceAll('/', '_').replaceAll('-', '_')}`;
        if (globalThis[functionName] && typeof globalThis[functionName] === 'function') {
            console.log(`Ejecutando: ${functionName}()`);
            try {
                globalThis[functionName]();
                return true;
            } catch (error) {
                console.error(`Error ejecutando ${functionName}:`, error);
            }
        }
        return false;
    },

    executePageLoaderWithRetry: function(page, navSeq, retries = 6) {
        if (navSeq !== this.NAVIGATION_SEQ) return;

        const executed = this.executePageLoader(page);
        if (executed || retries <= 0) return;

        globalThis.setTimeout(() => {
            this.executePageLoaderWithRetry(page, navSeq, retries - 1);
        }, 60);
    },

    /**
     * Configurar listeners de navegación
     */
    setupNavigation: function() {
        document.addEventListener('click', (e) => {
            // Detectar clicks también cuando se pulsa un hijo interno (img/span)
            const navTarget = e.target.closest('[data-page]');
            if (navTarget) {
                e.preventDefault();
                const page = navTarget.dataset.page;
                const currentRoute = (globalThis.location.hash || '').slice(1) || this.CURRENT_PAGE || 'index';
                if (typeof page === 'string' && page.startsWith('artista')) {
                    try {
                        if (currentRoute && !currentRoute.startsWith('artista')) {
                            sessionStorage.setItem('artistBackTarget', currentRoute);
                        }
                    } catch (error) {
                        console.warn('No se pudo guardar artistBackTarget:', error);
                    }
                }
                // Actualizar hash y forzar recarga completa para garantizar estado limpio
                try {
                    // Marcar para suprimir la recarga en el listener de hashchange
                    sessionStorage.setItem('suppressHashReload', '1');
                    const targetHash = `#${page}`;
                    if (globalThis.location.hash !== targetHash) {
                        globalThis.location.hash = page;
                    }
                    // Forzamos recarga inmediata para que el navegador cargue la página con el nuevo hash
                    globalThis.location.reload();
                    return;
                } catch (err) {
                    console.error('Error forzando recarga en navegación:', err);
                    // Fallback: navegar sin recarga
                    globalThis.location.hash = page;
                }
            }
        });
    },

    /**
     * Actualizar el navbar para marcar la página activa
     * @param {string} page - Página actual
     */
    updateNavbarActive: function(page) {
        const navLinks = document.querySelectorAll('.navbar-links [data-page]');
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.dataset.page === page) {
                link.classList.add('active');
            }
        });
    },

    /**
     * Verificar si el usuario está autenticado
     */
    checkAuth: function() {
        const user = AUTH.getUser();
        if (user) {
            console.log(`Usuario autenticado: ${user.name}`);
            this.updateUserUI(user);
        } else {
            console.log('Usuario no autenticado');
        }
    },

    /**
     * Actualizar UI con datos del usuario
     * @param {object} user - Datos del usuario
     */
    updateUserUI: function(user) {
        const userGreeting = document.getElementById('user-greeting');
        if (userGreeting) {
            userGreeting.textContent = `Hola, ${user.name}`;
        }
    },

    /**
     * Cerrar sesión
     */
    logout: function() {
        AUTH.logoutAndReloadToLogin();
    }
};

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});
