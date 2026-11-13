/**
 * Flujo OAuth simplificado para el entorno local.
 *
 * El backend expone /api/auth/google-register para crear/recuperar la cuenta a
 * partir de un perfil ya validado. En local usamos perfiles demo para que el
 * botón de Google/Apple sea funcional sin configurar credenciales externas.
 */
(function () {
    const DEMO_PROFILES = {
        google: {
            provider: 'google',
            uid: 'google-demo',
            email: 'google.demo@subsonicfest.com',
            name: 'Usuario Google Demo',
            picture: ''
        },
        apple: {
            provider: 'apple',
            uid: 'apple-demo',
            email: 'apple.demo@subsonicfest.com',
            name: 'Usuario Apple Demo',
            picture: ''
        }
    };

    function redirectAfterLogin(role) {
        const target = role === 'admin' ? 'admin-panel'
            : role === 'gestor' ? 'manager-events'
            : 'index';
        globalThis.location.hash = `#${target}`;
        globalThis.location.reload();
    }

    async function loginWithProvider(provider) {
        const base = DEMO_PROFILES[provider];
        if (!base) throw new Error('Proveedor OAuth no soportado');

        const response = await globalThis.SubsonicAPI.oauthDemo({
            ...base,
            role: 'cliente'
        });
        const token = response?.token || response?.sessionToken;
        if (!token || !response?.user) throw new Error('No se pudo iniciar sesión con el proveedor');

        globalThis.AUTH.setSession(token, response.user);
        redirectAfterLogin(response.user.role);
        return response;
    }

    async function handleCallback() {
        const params = new URLSearchParams(globalThis.location.search);
        const hashQuery = String(globalThis.location.hash || '').split('?')[1] || '';
        const hashParams = new URLSearchParams(hashQuery);
        const provider = (params.get('provider') || hashParams.get('provider') || 'google').toLowerCase();
        const email = params.get('email') || hashParams.get('email') || `${provider}.demo@subsonicfest.com`;
        const name = params.get('name') || hashParams.get('name') || `Usuario ${provider} Demo`;

        if (params.get('error') || hashParams.get('error')) {
            throw new Error(params.get('error') || hashParams.get('error'));
        }

        const response = await globalThis.SubsonicAPI.oauthDemo({
            provider,
            uid: `${provider}-${email}`,
            email,
            name,
            picture: params.get('picture') || hashParams.get('picture') || '',
            role: params.get('role') || hashParams.get('role') || 'cliente'
        });

        const token = response?.token || response?.sessionToken;
        if (!token || !response?.user) throw new Error('No se pudo completar el inicio de sesión');
        globalThis.AUTH.setSession(token, response.user);
        redirectAfterLogin(response.user.role);
        return response;
    }

    globalThis.OAUTH = {
        loginWithProvider,
        handleCallback,
        start: loginWithProvider
    };
})();
