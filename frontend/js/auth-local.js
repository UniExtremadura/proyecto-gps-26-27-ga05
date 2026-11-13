/**
 * Compatibilidad con la capa de autenticación local histórica.
 * La implementación real vive en auth.js; aquí se exponen alias usados por
 * versiones antiguas de las páginas.
 */
(function () {
    globalThis.AuthLocal = {
        login: (email, password) => globalThis.AUTH.login(email, password),
        register: (data) => globalThis.AUTH.register(data),
        logout: () => globalThis.AUTH.logout(),
        getUser: () => globalThis.AUTH.getUser(),
        getRole: () => globalThis.AUTH.getRole(),
        isLoggedIn: () => globalThis.AUTH.isLoggedIn()
    };

    globalThis.updateAuthUI = function () {
        if (typeof globalThis.updateNavbarUI === 'function') globalThis.updateNavbarUI();
    };
})();
