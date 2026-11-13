/**
 * Login - Autenticación con Firebase + Backend
 */

// Función que se ejecuta cuando se carga la página de login
window.load_login = async function() {
    console.log('Página de Login cargada');

    const loginCard = document.querySelector('.login-card');
    if (loginCard && loginCard.dataset.bound === '1') {
        // Evita listeners duplicados cuando el loader se ejecuta más de una vez.
        return;
    }
    if (loginCard) {
        loginCard.dataset.bound = '1';
    }
    
    const togglePasswordBtn = document.getElementById('toggle-password');
    const passwordInput = document.getElementById('login-password');
    const loginSubmitBtn = document.getElementById('login-submit');
    const googleBtn = document.getElementById('google-btn');
    const registerLink = document.querySelector('a[href*="register"]');

    // Redireccionar si ya está autenticado
    if (AUTH.isLoggedIn()) {
        App.navigate('index');
        return;
    }

    // Toggle para ver/ocultar contraseña
    if (togglePasswordBtn && passwordInput) {
        togglePasswordBtn.addEventListener('click', () => {
            const isPassword = passwordInput.getAttribute('type') === 'password';
            passwordInput.setAttribute('type', isPassword ? 'text' : 'password');
            togglePasswordBtn.classList.toggle('is-visible', isPassword);
            togglePasswordBtn.setAttribute('title', isPassword ? 'Ocultar contraseña' : 'Mostrar contraseña');
            togglePasswordBtn.setAttribute('aria-label', isPassword ? 'Ocultar contraseña' : 'Mostrar contraseña');
        });
    }

    // Login con email/contraseña
    if (loginSubmitBtn) {
        loginSubmitBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await handleLogin();
        });
    }

    // Google Login
    if (googleBtn) {
        googleBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await handleGoogleLogin();
        });
    }

    // Link a registro
    if (registerLink) {
        registerLink.addEventListener('click', (e) => {
            e.preventDefault();
            App.navigate('register');
        });
    }
};

/**
 * Manejar login con email/contraseña (Firebase)
 */
async function handleLogin() {
    try {
        const email = document.getElementById('login-email')?.value.trim()
            || document.getElementById('login-name')?.value.trim();
        const password = document.getElementById('login-password')?.value;

        if (!email || !password) {
            alert('Por favor completa todos los campos');
            return;
        }

        // TK-001-2: intento de autenticación local con JWT.
        if (globalThis.SubsonicLocalAuth) {
            try {
                const local = await globalThis.SubsonicLocalAuth.login(email, password);
                const home = App.getRoleHomePage(local.user?.role);
                App.navigate(home);
                return;
            } catch (localError) {
                console.warn('Login local no disponible:', localError.message);
            }
        }

        const btn = document.getElementById('login-submit');
        btn.disabled = true;
        btn.textContent = 'Conectando...';

        // Si Firebase no está disponible, usar fallback directo al backend.
        if (typeof firebase === 'undefined' || !firebase.auth) {
            const fallbackNoFirebase = await AUTH.loginBasic(email, password);
            if (fallbackNoFirebase.success) {
                const home = App.getRoleHomePage(fallbackNoFirebase.user?.role);
                setTimeout(() => App.navigate(home), 300);
            } else {
                alert('Fallo: ' + (fallbackNoFirebase.error || 'No se pudo iniciar sesión'));
                btn.disabled = false;
                btn.textContent = 'INICIA SESIÓN';
            }
            return;
        }

        try {
            const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
            const idToken = await userCredential.user.getIdToken();

            const result = await AUTH.login(idToken);

            if (result.success) {
                console.log('Login exitoso:', result.user.name);
                const home = App.getRoleHomePage(result.user?.role);
                setTimeout(() => App.navigate(home), 500);
            } else {
                alert('Error: ' + (result.error || 'Login fallido'));
                btn.disabled = false;
                btn.textContent = 'INICIA SESIÓN';
            }
        } catch (firebaseError) {
            console.error('Firebase error:', firebaseError);
            let message = firebaseError.message || 'Credenciales inválidas';
            if (firebaseError.code === 'auth/configuration-not-found') {
                const fallback = await AUTH.loginBasic(email, password);
                if (fallback.success) {
                    const home = App.getRoleHomePage(fallback.user?.role);
                    setTimeout(() => App.navigate(home), 300);
                    return;
                }
                message = 'Firebase Auth no disponible y el fallback no pudo iniciar sesión. Verifica email/contraseña demo.';
            } else if (firebaseError.code === 'auth/invalid-credential' || firebaseError.code === 'auth/wrong-password' || firebaseError.code === 'auth/user-not-found' || firebaseError.code === 'auth/invalid-login-credentials') {
                message = 'Email o contraseña incorrectos.';
            }
            alert('Fallo: ' + message);
            btn.disabled = false;
            btn.textContent = 'INICIA SESIÓN';
        }
    } catch (error) {
        console.error('Error en login:', error);
        const btn = document.getElementById('login-submit');
        btn.disabled = false;
        btn.textContent = 'INICIA SESIÓN';
    }
}

/**
 * Manejar login con Google
 */
async function handleGoogleLogin() {
    try {
        if (typeof firebase === 'undefined' || !firebase.auth) {
            alert('Firebase no está cargado. Recarga la página e inténtalo de nuevo.');
            return;
        }

        const provider = new firebase.auth.GoogleAuthProvider();
        const userCredential = await firebase.auth().signInWithPopup(provider);
        const idToken = await userCredential.user.getIdToken();

        const result = await AUTH.login(idToken);

        if (result.success) {
            console.log('Google login exitoso');
            const home = App.getRoleHomePage(result.user?.role);
            setTimeout(() => App.navigate(home), 500);
        } else {
            alert('Error: ' + (result.error || 'Login fallido'));
        }
    } catch (error) {
        console.error('Google login error:', error);
        if (error.code !== 'auth/popup-closed-by-user') {
            if (error.code === 'auth/operation-not-allowed') {
                alert('Google no está habilitado en Firebase Authentication. Activa el proveedor Google en Firebase Console.');
                return;
            }
            alert('Fallo: ' + error.message);
        }
    }
}

// Auto-ejecutar
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', window.load_login);
} else {
    window.load_login();
}


// TK-004-3: botón de acceso con Apple
document.addEventListener('DOMContentLoaded', () => {
    const appleBtn = document.getElementById('apple-btn');
    if (appleBtn && globalThis.SubsonicOAuth) {
        appleBtn.addEventListener('click', (event) => {
            event.preventDefault();
            globalThis.SubsonicOAuth.startApple();
        });
    }
});
