/**
 * TK-005-2: flujo web de reinicio de contraseña.
 */
function setResetStatus(message, isError = false) {
    const status = document.getElementById('reset-status');
    if (!status) return;
    status.textContent = message;
    status.classList.toggle('reset-error', isError);
}

async function requestResetLink() {
    const email = document.getElementById('reset-email')?.value.trim();
    if (!email) {
        setResetStatus('Introduce tu correo electrónico.', true);
        return;
    }
    try {
        const response = await SubsonicAPI.request('/auth/password/request', 'POST', { email });
        setResetStatus(response.message || 'Revisa tu correo electrónico.');
        if (response.token) {
            const step = document.getElementById('resetConfirmStep');
            step?.classList.remove('hidden');
            const tokenInput = document.getElementById('reset-token');
            if (tokenInput) tokenInput.value = response.token;
            const hint = document.getElementById('reset-demo-token');
            if (hint) hint.textContent = `Entorno de demostración: token ${response.token}`;
        }
    } catch (error) {
        setResetStatus(error.message || 'No se pudo solicitar el enlace.', true);
    }
}

async function confirmPasswordReset() {
    const token = document.getElementById('reset-token')?.value.trim();
    const password = document.getElementById('reset-password')?.value || '';
    if (!token || !password) {
        setResetStatus('Introduce el token y la nueva contraseña.', true);
        return;
    }
    try {
        await SubsonicAPI.request('/auth/password/reset', 'POST', { token, password });
        setResetStatus('Contraseña actualizada. Ya puedes iniciar sesión.');
        globalThis.setTimeout(() => { globalThis.location.hash = 'login'; }, 1200);
    } catch (error) {
        setResetStatus(error.message || 'No se pudo cambiar la contraseña.', true);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('reset-request-btn')?.addEventListener('click', requestResetLink);
    document.getElementById('reset-confirm-btn')?.addEventListener('click', confirmPasswordReset);
});
