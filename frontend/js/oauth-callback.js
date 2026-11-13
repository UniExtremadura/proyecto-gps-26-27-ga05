/**
 * TK-004-3: procesa la vuelta del proveedor OAuth.
 */
async function handleOAuthCallback() {
    const status = document.getElementById('oauthCallbackStatus');
    const params = new URLSearchParams((globalThis.location.hash.split('?')[1] || ''));
    const provider = params.get('provider') || 'google';
    const demo = params.get('demo') === '1';

    try {
        if (status) status.textContent = 'Validando con ' + provider + '...';
        const payload = provider === 'apple'
            ? { identity_token: 'demo-apple-token', email: 'apple.demo@subsonicfest.com', name: 'Usuario Apple Demo' }
            : { id_token: params.get('id_token') || '', demo };
        const result = await globalThis.SubsonicOAuth.complete(provider, payload);
        if (status) status.textContent = 'Acceso concedido. Redirigiendo...';
        globalThis.setTimeout(() => App.navigate(App.getRoleHomePage(result.user?.role)), 500);
    } catch (error) {
        console.error('OAuth callback error:', error);
        if (status) status.textContent = error.message || 'No se pudo completar el acceso.';
    }
}

document.addEventListener('DOMContentLoaded', handleOAuthCallback);
