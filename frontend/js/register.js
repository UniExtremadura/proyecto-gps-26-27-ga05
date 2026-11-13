/**
 * Registro - Crear nueva cuenta con Firebase + Backend
 */

let GOOGLE_REGISTER_IN_PROGRESS = false;

globalThis.load_register = async function() {
    console.log('Página de Registro cargada');

    const registerCard = document.querySelector('.register-card');
    if (registerCard?.dataset.bound === '1') {
        // Evita listeners duplicados cuando el loader se ejecuta más de una vez.
        return;
    }
    if (registerCard) {
        registerCard.dataset.bound = '1';
    }
    
    const registerSubmitBtn = document.getElementById('register-submit');
    const googleBtn = document.getElementById('google-btn');
    const registerRoleSelect = document.getElementById('register-role');
    const loginLink = document.querySelector('a[href*="login"]');

    // Redireccionar si ya está autenticado
    if (AUTH.isLoggedIn()) {
        App.navigate('index');
        return;
    }

    // Setup toggle de contraseñas
    setupPasswordToggle('toggle-register-pwd', 'register-password');
    setupPasswordToggle('toggle-register-confirm', 'register-confirm-password');

    // Mostrar/ocultar campos de proveedor según rol seleccionado
    if (registerRoleSelect) {
        registerRoleSelect.addEventListener('change', toggleProviderFields);
    }
    toggleProviderFields();

    // Enviar registro
    if (registerSubmitBtn) {
        registerSubmitBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await handleRegister();
        });
    }

    // Google register
    if (googleBtn) {
        googleBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await handleGoogleRegister();
        });
    }

    // Link a login
    if (loginLink) {
        loginLink.addEventListener('click', (e) => {
            e.preventDefault();
            App.navigate('login');
        });
    }
};

/**
 * Setup toggle para mostrar/ocultar contraseña
 */
function setupPasswordToggle(buttonId, inputId) {
    const toggleBtn = document.getElementById(buttonId);
    const passwordInput = document.getElementById(inputId);

    if (toggleBtn && passwordInput) {
        toggleBtn.addEventListener('click', () => {
            const isPassword = passwordInput.getAttribute('type') === 'password';
            passwordInput.setAttribute('type', isPassword ? 'text' : 'password');
            toggleBtn.classList.toggle('is-visible', isPassword);
            toggleBtn.setAttribute('title', isPassword ? 'Ocultar contraseña' : 'Mostrar contraseña');
            toggleBtn.setAttribute('aria-label', isPassword ? 'Ocultar contraseña' : 'Mostrar contraseña');
        });
    }
}

/**
 * Mostrar/ocultar campos de proveedor según el rol
 */
function toggleProviderFields() {
    const role = document.getElementById('register-role')?.value || '';
    const providerFields = document.getElementById('provider-fields');
    if (!providerFields) return;

    providerFields.style.display = role === 'proveedor' ? 'block' : 'none';
}

/**
 * Manejar registro con email/contraseña
 */
async function handleRegister() {
    try {
        if (typeof firebase === 'undefined' || !firebase.auth) {
            alert('Error de configuración: Firebase no está cargado. Recarga la página e inténtalo de nuevo.');
            return;
        }

        // Recolectar datos
        const email = document.getElementById('register-email')?.value.trim();
        const username = document.getElementById('register-username')?.value.trim();
        const password = document.getElementById('register-password')?.value;
        const confirmPassword = document.getElementById('register-confirm-password')?.value;
        const role = document.getElementById('register-role')?.value || 'cliente';
        const address = document.getElementById('register-address')?.value.trim() || '';
        const postalCode = document.getElementById('register-postal-code')?.value.trim() || '';
        const city = document.getElementById('register-city')?.value.trim() || '';
        const country = document.getElementById('register-country')?.value.trim() || '';
        const profileImageUrl = document.getElementById('register-avatar-url')?.value.trim() || '';

        // Validaciones básicas
        if (!email || !username || !password || !confirmPassword) {
            alert('Por favor completa todos los campos requeridos');
            return;
        }

        if (password !== confirmPassword) {
            alert('Las contraseñas no coinciden');
            return;
        }

        if (password.length < 6) {
            alert('La contraseña debe tener al menos 6 caracteres');
            return;
        }

        // Datos del usuario
        const userData = {
            email: email,
            password: password,
            name: username,
            role: role || 'cliente',
            address,
            postal_code: postalCode,
            city,
            country,
            profile_image_url: profileImageUrl
        };

        // TK-001-2: alta local con JWT (fallback sin Firebase).
        if (globalThis.SubsonicLocalAuth) {
            try {
                const local = await globalThis.SubsonicLocalAuth.register(userData);
                alert('¡Bienvenido! Tu cuenta ha sido creada.');
                App.navigate(App.getRoleHomePage(local.user?.role));
                return;
            } catch (localError) {
                console.warn('Registro local no disponible:', localError.message);
            }
        }

        // Antes de intentar registrar, comprobar si el email ya existe
        const check = await AUTH.checkEmail(email);
        if (check && check.success && check.exists) {
            const errEl = document.getElementById('register-error');
            const msg = 'Ya existe una cuenta registrada con este email.';
            if (errEl) {
                errEl.textContent = msg;
                errEl.style.display = 'block';
            } else {
                alert(msg);
            }
            return;
        }

        // Si es proveedor, agregar campos adicionales
        if (role === 'proveedor') {
            userData.company_name = document.getElementById('register-company-name')?.value.trim();
            userData.business_area = document.getElementById('register-business-area')?.value.trim();
            userData.card_number = document.getElementById('register-card-number')?.value.trim();

            if (!userData.company_name || !userData.business_area || !userData.card_number) {
                alert('Por favor completa todos los campos de proveedor');
                return;
            }
        }

        // Mostrar loading
        const btn = document.getElementById('register-submit');
        btn.disabled = true;
        btn.textContent = 'Registrando...';

        try {
            // 1. Registrar en backend (crea Auth + Firestore)
            const result = await AUTH.register(userData);

            if (result.success) {
                console.log('Registro exitoso');
                alert('¡Bienvenido! Tu cuenta ha sido creada.');
                
                // 2. Auto-login en Firebase cliente para obtener token
                const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
                const idToken = await userCredential.user.getIdToken();

                // 3. Crear sesión de backend
                const loginResult = await AUTH.login(idToken);
                if (loginResult.success) {
                    const home = App.getRoleHomePage(loginResult.user?.role || role);
                    setTimeout(() => App.navigate(home), 500);
                } else {
                    setTimeout(() => App.navigate('login'), 500);
                }
            } else {
                alert('Error en registro: ' + (result.error || 'Desconocido'));
                btn.disabled = false;
                btn.textContent = 'CREAR CUENTA';
            }
        } catch (registerError) {
            console.error('Register flow error:', registerError);
            
            // Mensajes de error específicos
            let errorMsg = 'Error desconocido';
            if (registerError.code === 'auth/email-already-in-use') {
                errorMsg = 'Este email ya está registrado';
            } else if (registerError.code === 'auth/invalid-email') {
                errorMsg = 'Email inválido';
            } else if (registerError.code === 'auth/weak-password') {
                errorMsg = 'Contraseña muy débil';
            } else if (registerError.code === 'auth/configuration-not-found') {
                errorMsg = 'Firebase Authentication no está configurado. Activa Email/Password en Firebase Console.';
            } else {
                errorMsg = registerError.message;
            }
            
            alert('Fallo: ' + errorMsg);
            btn.disabled = false;
            btn.textContent = 'CREAR CUENTA';
        }
    } catch (error) {
        console.error('Error en registro:', error);
        const btn = document.getElementById('register-submit');
        btn.disabled = false;
        btn.textContent = 'CREAR CUENTA';
    }
}

/**
 * Manejar registro con Google
 */
async function handleGoogleRegister() {
    try {
        if (GOOGLE_REGISTER_IN_PROGRESS) {
            return;
        }

        if (typeof firebase === 'undefined' || !firebase.auth) {
            alert('Firebase no está cargado. Recarga la página e inténtalo de nuevo.');
            return;
        }

        const roleSelect = document.getElementById('register-role');
        const role = roleSelect?.value || '';

        if (!role || (role !== 'cliente' && role !== 'proveedor')) {
            alert('Antes de registrarte con Google, selecciona si la cuenta será de cliente o proveedor.');
            roleSelect?.focus();
            return;
        }

        const profileData = {
            role,
            name: document.getElementById('register-username')?.value.trim() || '',
            address: document.getElementById('register-address')?.value.trim() || '',
            postal_code: document.getElementById('register-postal-code')?.value.trim() || '',
            city: document.getElementById('register-city')?.value.trim() || '',
            country: document.getElementById('register-country')?.value.trim() || '',
            profile_image_url: document.getElementById('register-avatar-url')?.value.trim() || ''
        };

        if (role === 'proveedor') {
            profileData.company_name = document.getElementById('register-company-name')?.value.trim() || '';
            profileData.business_area = document.getElementById('register-business-area')?.value.trim() || '';
            profileData.card_number = document.getElementById('register-card-number')?.value.trim() || '';

            if (!profileData.company_name || !profileData.business_area || !profileData.card_number) {
                alert('Para cuenta de proveedor, completa empresa, area de negocio y cuenta bancaria antes de continuar con Google.');
                return;
            }
        }

        GOOGLE_REGISTER_IN_PROGRESS = true;
        const googleBtn = document.getElementById('google-btn');
        if (googleBtn) {
            googleBtn.disabled = true;
            googleBtn.textContent = 'Conectando con Google...';
        }

        const provider = new firebase.auth.GoogleAuthProvider();
        const userCredential = await firebase.auth().signInWithPopup(provider);
        const idToken = await userCredential.user.getIdToken();

        const loginResult = await AUTH.googleRegister(idToken, profileData);
        if (loginResult.success) {
            console.log('Registro/Login con Google exitoso');
            const home = App.getRoleHomePage(loginResult.user?.role);
            setTimeout(() => App.navigate(home), 500);
        } else {
            alert('Error: ' + (loginResult.error || 'Registro fallido'));
        }
    } catch (error) {
        console.error('Google register error:', error);
        if (error.code !== 'auth/popup-closed-by-user') {
            if (error.code === 'auth/operation-not-allowed') {
                alert('Google no está habilitado en Firebase Authentication. Activa el proveedor Google en Firebase Console.');
                return;
            }
            if (error.code === 'auth/cancelled-popup-request') {
                alert('Ya hay una ventana de Google abierta. Ciérrala o complétala y vuelve a intentarlo con un solo click.');
                return;
            }
            if (error.code === 'auth/popup-blocked') {
                alert('El navegador ha bloqueado la ventana emergente de Google. Permite popups para localhost:3000 y reintenta.');
                return;
            }
            alert('Fallo: ' + error.message);
        }
    } finally {
        GOOGLE_REGISTER_IN_PROGRESS = false;
        const googleBtn = document.getElementById('google-btn');
        if (googleBtn) {
            googleBtn.disabled = false;
            googleBtn.textContent = 'Registrarse con Google';
        }
    }
}

// Auto-ejecutar
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', globalThis.load_register);
} else {
    globalThis.load_register();
}
