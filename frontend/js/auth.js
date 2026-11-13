/**
 * Gestión de sesión local (JWT + usuario en localStorage).
 */
(function () {
    const TOKEN_KEY = 'subsonic_token';
    const USER_KEY = 'subsonic_user';
    const LEGACY_TOKEN_KEY = 'sessionToken';

    function safeParse(value) {
        if (!value) return null;
        try {
            return JSON.parse(value);
        } catch (_error) {
            return null;
        }
    }

    function getToken() {
        return localStorage.getItem(TOKEN_KEY) || localStorage.getItem(LEGACY_TOKEN_KEY) || '';
    }

    function getUser() {
        return safeParse(localStorage.getItem(USER_KEY));
    }

    function setSession(token, user) {
        if (token) {
            localStorage.setItem(TOKEN_KEY, token);
            localStorage.setItem(LEGACY_TOKEN_KEY, token);
        }
        if (user) {
            localStorage.setItem(USER_KEY, JSON.stringify(user));
        }
        notify();
    }

    function updateUser(user) {
        if (!user) return;
        localStorage.setItem(USER_KEY, JSON.stringify(user));
        notify();
    }

    function clearSession() {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(LEGACY_TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
        notify();
    }

    function notify() {
        if (typeof globalThis.updateNavbarUI === 'function') {
            globalThis.updateNavbarUI();
        }
    }

    function getRole() {
        const user = getUser();
        return user?.role || 'visitante';
    }

    function isLoggedIn() {
        return Boolean(getUser() && getToken());
    }

    async function login(email, password) {
        const response = await globalThis.SubsonicAPI.login(email, password);
        const token = response?.token || response?.sessionToken || '';
        const user = response?.user || null;
        if (!token || !user) throw new Error('Respuesta de autenticación inválida');
        setSession(token, user);
        return response;
    }

    async function register(data) {
        const response = await globalThis.SubsonicAPI.register(data);
        const token = response?.token || response?.sessionToken || '';
        const user = response?.user || null;
        if (token && user) setSession(token, user);
        return response;
    }

    async function logout() {
        try {
            if (getToken()) await globalThis.SubsonicAPI.logout();
        } catch (error) {
            console.warn('No se pudo cerrar la sesión en el servidor:', error);
        } finally {
            clearSession();
        }
    }

    function logoutAndReloadToLogin() {
        clearSession();
        globalThis.location.hash = '#login';
        globalThis.location.reload();
    }

    async function refreshUser() {
        if (!getToken()) return null;
        const response = await globalThis.SubsonicAPI.me();
        if (response?.user) updateUser(response.user);
        return response?.user || null;
    }

    globalThis.AUTH = {
        TOKEN_KEY,
        USER_KEY,
        getToken,
        getUser,
        setSession,
        updateUser,
        clearSession,
        getRole,
        isLoggedIn,
        login,
        register,
        logout,
        logoutAndReloadToLogin,
        refreshUser
    };
})();
