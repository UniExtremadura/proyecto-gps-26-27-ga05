/** Registro local de usuarios. */
(function () {
    function setStatus(message, isError = false) {
        const status = document.getElementById('register-status');
        if (!status) return;
        status.textContent = message || '';
        status.classList.toggle('error', isError);
        status.classList.toggle('success', !isError && Boolean(message));
    }

    function redirectAfterRegister(role) {
        const target = role === 'admin' ? 'admin-panel'
            : role === 'gestor' ? 'manager-events'
            : 'index';
        globalThis.location.hash = `#${target}`;
        globalThis.location.reload();
    }

    async function submitRegister(event) {
        event?.preventDefault?.();
        const name = document.getElementById('register-name')?.value.trim();
        const email = document.getElementById('register-email')?.value.trim();
        const password = document.getElementById('register-password')?.value || '';
        const confirm = document.getElementById('register-password-confirm')?.value || '';
        const role = document.getElementById('register-role')?.value || 'cliente';
        const company = document.getElementById('register-company-name')?.value.trim() || '';
        const businessArea = document.getElementById('register-business-area')?.value.trim() || '';
        const button = document.getElementById('register-submit');

        if (!name || !email || !password) {
            setStatus('Nombre, correo y contraseña son obligatorios.', true);
            return;
        }
        if (password !== confirm) {
            setStatus('Las contraseñas no coinciden.', true);
            return;
        }
        if (password.length < 8 || !/[A-Z]/.test(password) || !/\d/.test(password)) {
            setStatus('La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.', true);
            return;
        }

        if (button) button.disabled = true;
        setStatus('Creando cuenta...');
        try {
            const response = await globalThis.AUTH.register({
                name,
                email,
                password,
                role,
                company_name: company,
                business_area: businessArea
            });
            setStatus('Cuenta creada. Redirigiendo...');
            redirectAfterRegister(response?.user?.role);
        } catch (error) {
            setStatus(error.message || 'No se pudo crear la cuenta.', true);
        } finally {
            if (button) button.disabled = false;
        }
    }

    function toggleCompanyFields() {
        const role = document.getElementById('register-role')?.value;
        document.querySelectorAll('.provider-only').forEach((element) => {
            element.classList.toggle('hidden', role !== 'proveedor');
        });
    }

    function bind() {
        document.querySelector('#register-form')?.addEventListener('submit', submitRegister);
        document.getElementById('register-submit')?.addEventListener('click', submitRegister);
        document.getElementById('register-role')?.addEventListener('change', toggleCompanyFields);
        toggleCompanyFields();
    }

    globalThis.load_register = bind;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bind);
    } else {
        bind();
    }
})();
