/**
 * Cliente HTTP común para el frontend.
 *
 * Detecta automáticamente el backend local. Si la web se sirve desde el mismo
 * FastAPI (puerto 8000) usa rutas relativas; si se sirve con Live Server u otro
 * puerto apunta a http://<host>:8000/api.
 */
(function () {
    const host = globalThis.location.hostname || 'localhost';
    const port = globalThis.location.port;
    const servedByBackend = port === '8000' || port === '';
    const defaultBase = servedByBackend ? `${globalThis.location.origin}/api` : `http://${host}:8000/api`;

    const API_BASE_URL = globalThis.SUBSONIC_API_BASE || defaultBase;
    globalThis.API_BASE_URL = API_BASE_URL;

    function getToken() {
        if (globalThis.AUTH && typeof globalThis.AUTH.getToken === 'function') {
            return globalThis.AUTH.getToken();
        }
        return localStorage.getItem('subsonic_token') || localStorage.getItem('sessionToken') || '';
    }

    function buildUrl(path) {
        if (/^https?:\/\//i.test(path)) return path;
        const clean = String(path || '').startsWith('/') ? path : `/${path}`;
        return `${API_BASE_URL}${clean}`;
    }

    async function parseResponse(response) {
        const text = await response.text();
        let payload = null;
        if (text) {
            try {
                payload = JSON.parse(text);
            } catch (_error) {
                payload = { status: response.ok ? 'success' : 'error', detail: text };
            }
        }
        if (!response.ok) {
            const detail = payload?.detail || payload?.message || `Error HTTP ${response.status}`;
            const error = new Error(Array.isArray(detail) ? detail.map((item) => item.msg || item).join(', ') : String(detail));
            error.status = response.status;
            error.payload = payload;
            throw error;
        }
        return payload;
    }

    async function request(path, method = 'GET', body = null, options = {}) {
        const headers = { Accept: 'application/json', ...(options.headers || {}) };
        const token = getToken();
        if (token) headers.Authorization = `Bearer ${token}`;

        const config = {
            method: method.toUpperCase(),
            headers,
            credentials: 'include'
        };

        if (body !== null && body !== undefined) {
            if (body instanceof FormData) {
                config.body = body;
            } else {
                headers['Content-Type'] = 'application/json';
                config.body = JSON.stringify(body);
            }
        }

        const response = await fetch(buildUrl(path), config);
        return parseResponse(response);
    }

    const endpoints = {
        // Autenticación
        login: (email, password) => request('/auth/login', 'POST', { email, password }),
        register: (data) => request('/auth/register', 'POST', data),
        logout: () => request('/auth/logout', 'POST', {}),
        me: () => request('/auth/me'),
        checkEmail: (email) => request(`/auth/check_email?email=${encodeURIComponent(email)}`),
        oauthDemo: (data) => request('/auth/google-register', 'POST', data),

        // Productos
        getAllProducts: () => request('/products'),
        getProduct: (id) => request(`/products/${encodeURIComponent(id)}`),
        createProduct: (data) => request('/products', 'POST', data),
        updateProduct: (id, data) => request(`/products/${encodeURIComponent(id)}`, 'PUT', data),
        deleteProduct: (id) => request(`/products/${encodeURIComponent(id)}`, 'DELETE'),

        // Eventos
        getAllEvents: () => request('/events'),
        getEvent: (id) => request(`/events/${encodeURIComponent(id)}`),
        searchEvents: (query) => request(`/events/search?q=${encodeURIComponent(query || '')}`),
        createEvent: (data) => request('/events', 'POST', data),
        updateEvent: (id, data) => request(`/events/${encodeURIComponent(id)}`, 'PUT', data),
        deleteEvent: (id) => request(`/events/${encodeURIComponent(id)}`, 'DELETE'),

        // Artistas
        getAllArtists: () => request('/artists'),
        getArtist: (slug) => request(`/artists/${encodeURIComponent(slug)}`),
        searchArtists: (query, genre) => request(`/artists/search?q=${encodeURIComponent(query || '')}&genre=${encodeURIComponent(genre || '')}`),
        createArtist: (data) => request('/artists', 'POST', data),
        updateArtist: (id, data) => request(`/artists/${encodeURIComponent(id)}`, 'PUT', data),
        deleteArtist: (id) => request(`/artists/${encodeURIComponent(id)}`, 'DELETE'),

        // Perfil y pedidos
        getUserProfile: () => request('/profile'),
        updateUserProfile: (data) => request('/profile', 'PUT', data),
        getUserOrders: () => request('/orders'),
        getOrder: (id) => request(`/orders/${encodeURIComponent(id)}`),
        createOrder: (data) => request('/orders', 'POST', data),
        updateOrder: (id, data) => request(`/orders/${encodeURIComponent(id)}`, 'PUT', data),

        // Paneles
        getProviderSales: () => request('/provider/sales'),
        getManagerDashboard: () => request('/manager/dashboard'),

        // Stock
        getStock: () => request('/stock'),
        updateStock: (productId, stock, minStock) => request(`/stock/${encodeURIComponent(productId)}`, 'PUT', { stock, min_stock: minStock }),
        lowStockAlerts: () => request('/stock/alerts'),

        // Reservas
        getVenues: () => request('/venues'),
        getBookings: () => request('/bookings'),
        createBooking: (data) => request('/bookings', 'POST', data),
        cancelBooking: (id) => request(`/bookings/${encodeURIComponent(id)}`, 'DELETE'),
        getBookingHistory: (status = '') => request(`/bookings/history?status=${encodeURIComponent(status)}`),

        // Contraseña
        requestPasswordReset: (email) => request('/auth/password/request', 'POST', { email }),
        resetPassword: (token, password) => request('/auth/password/reset', 'POST', { token, password }),

        // Admin
        getAdminUsers: () => request('/admin/users'),
        getAdminEvents: () => request('/admin/events'),
        moderateUser: (uid, action, reason = '') => request(`/admin/users/${encodeURIComponent(uid)}/${action}`, 'POST', { reason }),
        moderateEvent: (eventId, decision, reason = '') => request(`/admin/events/${encodeURIComponent(eventId)}/moderate`, 'POST', { decision, reason }),
        getGlobalAnalytics: () => request('/admin/analytics'),

        request,
        buildUrl
    };

    globalThis.SubsonicAPI = endpoints;
})();
