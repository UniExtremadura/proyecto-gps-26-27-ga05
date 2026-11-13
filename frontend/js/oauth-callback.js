/** Finaliza el flujo OAuth y guarda la sesión. */
(function () {
    async function run() {
        const status = document.getElementById('oauthStatus');
        if (!globalThis.OAUTH) {
            if (status) status.textContent = 'No se pudo cargar el módulo OAuth.';
            return;
        }
        try {
            if (status) status.textContent = 'Completando inicio de sesión...';
            await globalThis.OAUTH.handleCallback();
        } catch (error) {
            if (status) {
                status.textContent = error.message || 'No se pudo completar el inicio de sesión.';
                status.classList.add('error');
            }
        }
    }

    globalThis.load_oauth_callback = run;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', run);
    } else {
        run();
    }
})();
