/** Perfil común para proveedores, gestores y administradores. */
(function () {
    function setStatus(message, isError = false) {
        const node = document.getElementById('profilePageStatus');
        if (!node) return;
        node.textContent = message || '';
        node.classList.toggle('error', isError);
        node.classList.toggle('success', !isError && Boolean(message));
    }

    function fill(profile) {
        const name = profile.name || '';
        const email = profile.email || '';
        const role = profile.role || '';

        const heading = document.getElementById('profilePageName');
        if (heading) heading.textContent = name || 'Usuario';
        const emailNode = document.getElementById('profilePageEmail');
        if (emailNode) emailNode.textContent = email;
        const roleNode = document.getElementById('profilePageRole');
        if (roleNode) roleNode.textContent = role.toUpperCase();
        const created = document.getElementById('profilePageCreated');
        if (created) {
            const date = profile.created_at ? new Date(profile.created_at) : null;
            created.textContent = date && !Number.isNaN(date.getTime())
                ? `Miembro desde ${date.toLocaleDateString('es-ES')}`
                : '';
        }

        const values = {
            'profileNameInput': name,
            'profileEmailInput': email,
            'profileAddressInput': profile.address || '',
            'profileCityInput': profile.city || '',
            'profilePostalInput': profile.postal_code || '',
            'profileCountryInput': profile.country || '',
            'profileCompanyInput': profile.company_name || '',
            'profileBusinessInput': profile.business_area || ''
        };
        Object.entries(values).forEach(([id, value]) => {
            const field = document.getElementById(id);
            if (field) field.value = value;
        });

        const avatar = document.getElementById('profilePageAvatar');
        if (avatar) {
            avatar.src = profile.profile_image_url
                || `https://ui-avatars.com/api/?name=${encodeURIComponent(name || 'U')}&background=00d4ff&color=000&bold=true&size=120`;
        }
    }

    async function load() {
        const page = document.getElementById('profilePage');
        if (!page) return;
        if (!globalThis.AUTH?.isLoggedIn?.()) {
            globalThis.location.hash = '#login';
            globalThis.location.reload();
            return;
        }

        try {
            const response = await globalThis.SubsonicAPI.getUserProfile();
            fill(response?.user || globalThis.AUTH.getUser() || {});
        } catch (error) {
            fill(globalThis.AUTH.getUser() || {});
            setStatus(error.message || 'No se pudo cargar el perfil.', true);
        }
    }

    async function save(event) {
        event?.preventDefault?.();
        const payload = {
            name: document.getElementById('profileNameInput')?.value.trim(),
            email: document.getElementById('profileEmailInput')?.value.trim(),
            address: document.getElementById('profileAddressInput')?.value.trim(),
            city: document.getElementById('profileCityInput')?.value.trim(),
            postal_code: document.getElementById('profilePostalInput')?.value.trim(),
            country: document.getElementById('profileCountryInput')?.value.trim(),
            company_name: document.getElementById('profileCompanyInput')?.value.trim(),
            business_area: document.getElementById('profileBusinessInput')?.value.trim()
        };

        if (!payload.name || !payload.email) {
            setStatus('Nombre y correo son obligatorios.', true);
            return;
        }

        try {
            setStatus('Guardando...');
            const response = await globalThis.SubsonicAPI.updateUserProfile(payload);
            if (response?.user) globalThis.AUTH.updateUser(response.user);
            else globalThis.AUTH.updateUser({ ...(globalThis.AUTH.getUser() || {}), ...payload });
            fill(response?.user || { ...(globalThis.AUTH.getUser() || {}), ...payload });
            setStatus('Perfil actualizado correctamente.');
        } catch (error) {
            setStatus(error.message || 'No se pudo guardar el perfil.', true);
        }
    }

    function bind() {
        const page = document.getElementById('profilePage');
        if (!page) return;
        document.getElementById('profilePageForm')?.addEventListener('submit', save);
        document.getElementById('profileLogout')?.addEventListener('click', () => globalThis.AUTH.logoutAndReloadToLogin());
        load();
    }

    globalThis.load_provider_profile = bind;
    globalThis.load_manager_profile = bind;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bind);
    } else {
        bind();
    }
})();
