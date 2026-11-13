/**
 * TK-004-3: flujo OAuth en frontend (Google/Apple).
 */
globalThis.SubsonicOAuth = {
    apiBase: 'http://subsonic-backend-pi.asatfyfmapbdgdfk.polandcentral.azurecontainer.io:8000/api',

    async complete(provider, payload) {
        const response = await fetch(`${this.apiBase}/oauth/${provider}/callback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(data.detail || 'No se pudo completar OAuth');
        localStorage.setItem('sessionToken', data.token);
        localStorage.setItem('subsonicUser', JSON.stringify(data.user || {}));
        return data;
    },

    async startGoogle() {
        if (typeof firebase !== 'undefined' && firebase.auth) {
            const provider = new firebase.auth.GoogleAuthProvider();
            const credential = await firebase.auth().signInWithPopup(provider);
            const idToken = await credential.user.getIdToken();
            return this.complete('google', { id_token: idToken });
        }
        // Modo demo sin Firebase: vuelve por la página de callback.
        globalThis.location.hash = 'oauth-callback?provider=google&demo=1';
        return null;
    },

    async startApple() {
        // Apple requiere un Service ID y una clave privada; en desarrollo se simula.
        globalThis.location.hash = 'oauth-callback?provider=apple&demo=1';
        return null;
    }
};
