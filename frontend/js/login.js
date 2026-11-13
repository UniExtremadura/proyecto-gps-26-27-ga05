/** Login local con JWT. */
(function () {
    function setStatus(message, isError = false) {
        const status = document.getElementById('login-status');
        if (!status) return;
        status.textContent = message || '';
        status.classList.toggle('error', isError);
        status.classList.toggle('success', !isError && Boolean(message));
    }

    function redirectAfterLogin(role) {
        const target = role === 'admin' ? 'admin-panel'
            : role === 'gestor' ? 'manager-events'
            : 'index';
        globalThis.location.hash = `#${target}`;
        globalThis.location.reload();
    }

    async function submitLogin(event) {
        event?.preventDefault?.();
        const email = document.getElementById('login-email')?.value.trim();
        const password = document.getElementById('login-password')?.value || '';
        const button = document.getElementById('login-submit');

        if (!email || !password) {
            setStatus('Introduce tu correo y contraseña.', true);
            return;
        }

        if (button) button.disabled = true;
        setStatus('Entrando...');
        try {
            const response = await globalThis.AUTH.login(email, password);
            setStatus('Acceso correcto. Redirigiendo...');
            redirectAfterLogin(response?.user?.role);
        } catch (error) {
            setStatus(error.message || 'No se pudo iniciar sesión.', true);
        } finally {
            if (button) button.disabled = false;
        }
    }

    async function providerLogin(provider) {
        try {
            setStatus(`Conectando con ${provider}...`);
            await globalThis.OAUTH.loginWithProvider(provider);
        } catch (error) {
            setStatus(error.message || `No se pudo iniciar sesión con ${provider}.`, true);
        }
    }

    function togglePassword() {
        const input = document.getElementById('login-password');
        if (!input) return;
        input.type = input.type === 'password' ? 'text' : 'password';
    }

    function bind() {
        const form = document.querySelector('.login-card');
        form?.addEventListener('submit', submitLogin);
        document.getElementById('login-submit')?.addEventListener('click', submitLogin);
        document.getElementById('toggle-password')?.addEventListener('click', togglePassword);
        document.getElementById('google-btn')?.addEventListener('click', () => providerLogin('google'));
        document.getElementById('apple-btn')?.addEventListener('click', () => providerLogin('apple'));

        const user = globalThis.AUTH?.getUser?.();
        if (user) {
            redirectAfterLogin(user.role);
        }
    }

    globalThis.load_login = bind;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bind);
    } else {
        bind();
    }
})();
