/**
 * TK-001-2: formularios de autenticación contra la API local con JWT.
 * Se usa como fallback cuando Firebase Auth no está configurado.
 */
globalThis.SubsonicLocalAuth = {
    apiBase: 'http://subsonic-backend-pi.asatfyfmapbdgdfk.polandcentral.azurecontainer.io:8000/api',

    async request(path, body) {
        const response = await fetch(`${this.apiBase}${path}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            throw new Error(data.detail || 'Error de autenticación');
        }
        return data;
    },

    saveSession(data) {
        if (!data || !data.token) return;
        localStorage.setItem('sessionToken', data.token);
        localStorage.setItem('subsonicUser', JSON.stringify(data.user || {}));
    },

    async login(email, password) {
        const data = await this.request('/auth/local/login', { email, password });
        this.saveSession(data);
        return data;
    },

    async register(userData) {
        const data = await this.request('/auth/local/register', userData);
        this.saveSession(data);
        return data;
    },

    async logout() {
        const token = localStorage.getItem('sessionToken');
        if (token) {
            await fetch(`${this.apiBase}/auth/local/logout`, {
                method: 'POST',
                headers: { Authorization: `Bearer ${token}` }
            }).catch(() => {});
        }
        localStorage.removeItem('sessionToken');
        localStorage.removeItem('subsonicUser');
    }
};
