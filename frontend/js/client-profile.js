// CLIENT PROFILE MANAGEMENT

document.addEventListener('DOMContentLoaded', () => {
    initClientProfile().catch((error) => {
        console.error('Error iniciando perfil cliente:', error);
    });
});

async function initClientProfile() {
    const localUser = AUTH.getUser();
    if (localUser?.role !== 'cliente') {
        globalThis.location.hash = 'login';
        return;
    }

    setupClientMenuListeners();
    setupClientLogoutListeners();
    setupProfileFormSubmit();
    setupAvatarControls();

    setTimeout(() => {
        if (globalThis.setNeuralGlowColors) {
            globalThis.setNeuralGlowColors([0, 212, 255], [157, 0, 255]);
        }
    }, 100);

    await refreshProfileAndOrders();
}

async function refreshProfileAndOrders() {
    const fallbackUser = AUTH.getUser();
    let profileUser = fallbackUser;

    try {
        const profileResponse = await SubsonicAPI.getUserProfile();
        if (profileResponse?.user) {
            profileUser = profileResponse.user;
            localStorage.setItem(AUTH.USER_KEY, JSON.stringify(profileUser));
        }
    } catch (error) {
        console.warn('No se pudo cargar perfil desde API, se usa caché local.', error);
    }

    if (!profileUser) {
        globalThis.location.hash = 'login';
        return;
    }

    populateClientProfileData(profileUser);
    await loadOrderHistory();
}

function populateClientProfileData(user) {
    const safeName = user.name || 'Cliente';
    const safeEmail = user.email || '';
    const avatarImg = document.getElementById('client-avatar');
    const avatarUrl = (user.profile_image_url || '').trim() || buildAvatarFallback(safeName);

    if (avatarImg) {
        avatarImg.src = avatarUrl;
        avatarImg.onerror = () => {
            avatarImg.src = buildAvatarFallback(safeName);
        };
    }

    const headerName = document.getElementById('client-name');
    if (headerName) headerName.textContent = safeName;

    const headerEmail = document.getElementById('client-email');
    if (headerEmail) headerEmail.textContent = safeEmail;

    const memberDate = document.getElementById('client-member-date');
    if (memberDate) {
        const createdAt = user.created_at ? new Date(user.created_at) : null;
        if (createdAt && !Number.isNaN(createdAt.getTime())) {
            memberDate.textContent = `Miembro desde: ${createdAt.toLocaleDateString('es-ES', { year: 'numeric', month: 'long' })}`;
        } else {
            memberDate.textContent = 'Miembro desde: -';
        }
    }

    const fullnameInput = document.getElementById('client-fullname');
    const emailInput = document.getElementById('client-email-input');
    const addressInput = document.getElementById('client-address');
    const postalCodeInput = document.getElementById('client-postal-code');
    const cityInput = document.getElementById('client-city');
    const countryInput = document.getElementById('client-country');

    if (fullnameInput) fullnameInput.value = safeName;
    if (emailInput) emailInput.value = safeEmail;
    if (addressInput) addressInput.value = user.address || '';
    if (postalCodeInput) postalCodeInput.value = user.postal_code || '';
    if (cityInput) cityInput.value = user.city || '';
    if (countryInput) countryInput.value = user.country || '';
}

async function loadOrderHistory() {
    const ticketsList = document.getElementById('tickets-list');
    const merchList = document.getElementById('merch-list');
    if (!ticketsList || !merchList) return;

    let orders = [];
    try {
        const ordersResponse = await SubsonicAPI.getUserOrders();
        const rawOrders = Array.isArray(ordersResponse?.data) ? ordersResponse.data : [];
        orders = await enrichClientOrdersWithImages(rawOrders);
    } catch (error) {
        console.warn('No se pudieron cargar pedidos del usuario.', error);
        orders = [];
    }

    const ticketOrders = [];
    const merchOrders = [];

    orders.forEach((order) => {
        const items = Array.isArray(order.items) ? order.items : [];
        if (items.length === 0) return;

        const hasTicket = items.some((item) => isTicketItem(item));
        const hasMerch = items.some((item) => !isTicketItem(item));

        if (hasTicket) ticketOrders.push(order);
        if (hasMerch) merchOrders.push(order);
    });

    renderOrderGroup(ticketsList, ticketOrders, 'entradas');
    renderOrderGroup(merchList, merchOrders, 'merch');
}

function resolveOrderItemImage(item) {
    const direct = item?.image || item?.image_url || item?.cardImg || item?.heroImg;
    if (typeof direct === 'string' && direct.trim()) {
        return normalizeImageUrl(direct.trim());
    }

    if (Array.isArray(item?.images)) {
        const first = item.images.find((img) => typeof img === 'string' && img.trim());
        if (first) return normalizeImageUrl(first.trim());
    }

    return '';
}

function resolveSourceImage(source) {
    const direct = source?.image || source?.image_url || source?.cardImg || source?.heroImg;
    if (typeof direct === 'string' && direct.trim()) {
        return normalizeImageUrl(direct.trim());
    }

    if (Array.isArray(source?.images)) {
        const first = source.images.find((img) => typeof img === 'string' && img.trim());
        if (first) return normalizeImageUrl(first.trim());
    }

    return '';
}

function normalizeImageUrl(url) {
    const value = String(url || '').trim();
    if (!value) return '';

    if (value.startsWith('/frontend/assets/')) {
        return value.replace('/frontend/assets/', '/assets/');
    }

    if (value.startsWith('frontend/assets/')) {
        return `/${value.replace(/^frontend\//, '')}`;
    }

    return value;
}

async function enrichClientOrdersWithImages(orders) {
    if (!Array.isArray(orders) || orders.length === 0) return orders;

    const hasMissingImages = orders.some((order) => {
        const items = Array.isArray(order?.items) ? order.items : [];
        return items.some((item) => !resolveOrderItemImage(item));
    });

    if (!hasMissingImages) return orders;

    try {
        const [productsResponse, eventsResponse] = await Promise.all([
            SubsonicAPI.getAllProducts(),
            SubsonicAPI.getAllEvents()
        ]);

        const products = Array.isArray(productsResponse?.data) ? productsResponse.data : [];
        const events = Array.isArray(eventsResponse?.data) ? eventsResponse.data : [];

        const productById = new Map(products.map((product) => [String(product.id), product]));
        const productByName = new Map(products.map((product) => [String(product.name || '').toLowerCase(), product]));
        const eventById = new Map(events.map((event) => [String(event.id), event]));
        const eventByName = new Map(events.map((event) => [String(event.name || '').toLowerCase(), event]));

        return orders.map((order) => {
            const items = Array.isArray(order?.items) ? order.items : [];
            const nextItems = items.map((item) => {
                if (resolveOrderItemImage(item)) return item;

                const ticket = isTicketItem(item);
                const source = ticket
                    ? eventById.get(String(item?.event_id || '')) || eventByName.get(String(item?.event_name || item?.name || '').toLowerCase())
                    : productById.get(String(item?.id || '')) || productByName.get(String(item?.name || '').toLowerCase());

                if (!source) return item;

                const image = resolveSourceImage(source);
                if (!image) return item;

                const fallbackImages = Array.isArray(item.images) ? item.images : [];
                const resolvedImages = Array.isArray(source.images) ? source.images : fallbackImages;

                return {
                    ...item,
                    image,
                    images: resolvedImages
                };
            });

            return {
                ...order,
                items: nextItems
            };
        });
    } catch (error) {
        console.warn('No se pudieron enriquecer imágenes en perfil de cliente:', error);
        return orders;
    }
}

function renderOrderGroup(container, orders, kind) {
    if (!orders.length) {
        container.innerHTML = `<p class="empty-state">Aún no tienes ${kind === 'entradas' ? 'entradas registradas' : 'compras de merchandising registradas'}.</p>`;
        return;
    }

    const sortedOrders = [...orders].sort((a, b) => {
        const aDate = new Date(a.created_at || 0).getTime();
        const bDate = new Date(b.created_at || 0).getTime();
        return bDate - aDate;
    });

    container.innerHTML = sortedOrders.slice(0, 6).map((order) => {
        const items = Array.isArray(order.items) ? order.items : [];
        const visibleItems = items.filter((item) => kind === 'entradas' ? isTicketItem(item) : !isTicketItem(item));
        const mainItem = visibleItems[0] || null;
        const title = mainItem?.name || mainItem?.product_name || mainItem?.event_name || 'Pedido';
        const image = resolveOrderItemImage(mainItem);
        const qty = visibleItems.reduce((sum, item) => sum + Number(item.quantity || item.qty || 1), 0);
        const createdAt = order.created_at ? new Date(order.created_at) : null;
        const dateLabel = createdAt && !Number.isNaN(createdAt.getTime())
            ? createdAt.toLocaleDateString('es-ES')
            : 'Fecha no disponible';

        return `
            <div class="ticket-item">
                <div class="ticket-thumb" aria-hidden="true">
                    ${image
                        ? `<img src="${escapeHtml(image)}" alt="${escapeHtml(title)}" loading="lazy" decoding="async">`
                        : '<span class="ticket-thumb-fallback">🛍️</span>'}
                </div>
                <div class="ticket-info">
                    <h3>${escapeHtml(title)}</h3>
                    <p>${qty} item(s) • ${dateLabel}</p>
                </div>
                <div class="ticket-status">
                    <button class="qr-btn" type="button">#${escapeHtml(String(order.id || order.order_id || '').slice(-6) || '-----')}</button>
                </div>
            </div>
        `;
    }).join('');
}

function setupProfileFormSubmit() {
    const form = document.getElementById('client-profile-form');

    if (!form) return;
    form.addEventListener('submit', handleProfileSubmit);
}

function setupAvatarControls() {
    const trigger = document.getElementById('client-avatar-trigger');
    const actions = document.getElementById('client-avatar-actions');
    const fileInput = document.getElementById('client-avatar-file');
    const uploadOption = document.getElementById('avatar-upload-option');
    const urlOption = document.getElementById('avatar-url-option');

    if (trigger && actions) {
        const toggleActions = (forceVisible) => {
            const willShow = typeof forceVisible === 'boolean'
                ? forceVisible
                : actions.classList.contains('hidden');
            actions.classList.toggle('hidden', !willShow);
        };

        trigger.addEventListener('click', () => toggleActions());
        trigger.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                toggleActions();
            }
        });

        document.addEventListener('click', (event) => {
            if (!actions.contains(event.target) && !trigger.contains(event.target)) {
                toggleActions(false);
            }
        });
    }

    if (uploadOption && fileInput) {
        uploadOption.addEventListener('click', () => {
            actions?.classList.add('hidden');
            fileInput.click();
        });
    }

    if (urlOption) {
        urlOption.addEventListener('click', async () => {
            actions?.classList.add('hidden');
            const value = await globalThis.showSubsonicPrompt('Pega la URL de tu foto de perfil:', 'https://', {
                title: 'Cambiar foto de perfil',
                confirmText: 'Guardar',
                cancelText: 'Cancelar'
            });
            if (!value) return;

            const avatarUrl = value.trim();
            if (!avatarUrl) return;

            const avatarImage = document.getElementById('client-avatar');
            if (avatarImage) {
                avatarImage.src = avatarUrl;
                avatarImage.onerror = () => {
                    showSaveMessage('La URL no parece una imagen válida.', true);
                    const name = document.getElementById('client-fullname')?.value || 'Cliente';
                    avatarImage.src = buildAvatarFallback(name);
                };
            }

            saveAvatarImmediately(avatarUrl);
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', async () => {
            const file = fileInput.files?.[0];
            if (!file) return;

            if (!String(file.type || '').startsWith('image/')) {
                showSaveMessage('Solo se permiten archivos de imagen.', true);
                fileInput.value = '';
                return;
            }

            try {
                showSaveMessage('Procesando imagen...', false);
                const rawDataUrl = await readFileAsDataUrl(file);
                const croppedDataUrl = await openAvatarCropper(rawDataUrl);
                const dataUrl = await processImageDataUrl(croppedDataUrl);
                const avatarImage = document.getElementById('client-avatar');
                if (avatarImage) avatarImage.src = dataUrl;
                await saveAvatarImmediately(dataUrl);
            } catch (error) {
                if (String(error?.message || '').toLowerCase().includes('cancelada')) {
                    return;
                }
                showSaveMessage(error.message || 'No se pudo procesar la imagen.', true);
            } finally {
                fileInput.value = '';
            }
        });
    }

}

async function saveAvatarImmediately(avatarValue) {
    try {
        const response = await SubsonicAPI.updateUserProfile({
            profile_image_url: avatarValue
        });
        if (response?.user) {
            localStorage.setItem(AUTH.USER_KEY, JSON.stringify(response.user));
        }
        showSaveMessage('Foto de perfil guardada correctamente.', false);
    } catch (error) {
        showSaveMessage(error.message || 'No se pudo guardar la foto de perfil.', true);
    }
}

function readFileAsDataUrl(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            const result = reader.result;
            if (typeof result === 'string') {
                resolve(result);
                return;
            }
            reject(new Error('No se pudo interpretar la imagen seleccionada.'));
        };
        reader.onerror = () => reject(new Error('No se pudo leer el archivo.'));
        reader.readAsDataURL(file);
    });
}

function resizeDataUrlImage(dataUrl, maxSize = 512, quality = 0.84) {
    return new Promise((resolve, reject) => {
        const image = new Image();
        image.onload = () => {
            const canvas = document.createElement('canvas');
            const ratio = Math.min(1, maxSize / Math.max(image.width, image.height));
            canvas.width = Math.max(1, Math.round(image.width * ratio));
            canvas.height = Math.max(1, Math.round(image.height * ratio));
            const ctx = canvas.getContext('2d');
            if (!ctx) {
                reject(new Error('No se pudo procesar la imagen en el navegador.'));
                return;
            }
            ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
            const compressed = canvas.toDataURL('image/jpeg', quality);
            resolve(compressed);
        };
        image.onerror = () => reject(new Error('Archivo de imagen inválido.'));
        image.src = dataUrl;
    });
}

async function processImageFile(file) {
    const rawDataUrl = await readFileAsDataUrl(file);
    return processImageDataUrl(rawDataUrl);
}

async function processImageDataUrl(dataUrl) {
    const compressed = await resizeDataUrlImage(dataUrl);

    if (compressed.length > 850000) {
        throw new Error('La imagen es demasiado grande. Usa una imagen más ligera.');
    }

    return compressed;
}

function openAvatarCropper(sourceDataUrl) {
    return new Promise((resolve, reject) => {
        const modal = document.getElementById('avatar-crop-modal');
        const canvas = document.getElementById('avatar-crop-canvas');
        const zoomInput = document.getElementById('avatar-crop-zoom');
        const offsetXInput = document.getElementById('avatar-crop-offset-x');
        const offsetYInput = document.getElementById('avatar-crop-offset-y');
        const cancelBtn = document.getElementById('avatar-crop-cancel');
        const saveBtn = document.getElementById('avatar-crop-save');

        if (!modal || !canvas || !zoomInput || !offsetXInput || !offsetYInput || !cancelBtn || !saveBtn) {
            resolve(sourceDataUrl);
            return;
        }

        const ctx = canvas.getContext('2d');
        if (!ctx) {
            reject(new Error('No se pudo inicializar el editor de imagen.'));
            return;
        }

        const image = new Image();
        const state = {
            zoom: 1,
            offsetX: 0,
            offsetY: 0
        };

        let isDone = false;

        const cleanup = () => {
            zoomInput.removeEventListener('input', onControlChange);
            offsetXInput.removeEventListener('input', onControlChange);
            offsetYInput.removeEventListener('input', onControlChange);
            cancelBtn.removeEventListener('click', onCancel);
            saveBtn.removeEventListener('click', onSave);
            modal.removeEventListener('click', onBackdropClick);
            modal.classList.add('hidden');
        };

        const finalize = (cb) => {
            if (isDone) return;
            isDone = true;
            cleanup();
            cb();
        };

        const drawPreview = () => {
            const width = canvas.width;
            const height = canvas.height;
            ctx.clearRect(0, 0, width, height);
            ctx.fillStyle = '#0a0a0c';
            ctx.fillRect(0, 0, width, height);

            const fitScale = Math.max(width / image.width, height / image.height);
            const scale = fitScale * state.zoom;
            const drawWidth = image.width * scale;
            const drawHeight = image.height * scale;
            const x = (width - drawWidth) / 2 + state.offsetX;
            const y = (height - drawHeight) / 2 + state.offsetY;

            ctx.drawImage(image, x, y, drawWidth, drawHeight);
        };

        const onControlChange = () => {
            state.zoom = Number(zoomInput.value || 1);
            state.offsetX = Number(offsetXInput.value || 0);
            state.offsetY = Number(offsetYInput.value || 0);
            drawPreview();
        };

        const onCancel = () => {
            finalize(() => reject(new Error('Edición cancelada por el usuario.')));
        };

        const onSave = () => {
            const resultDataUrl = canvas.toDataURL('image/jpeg', 0.92);
            finalize(() => resolve(resultDataUrl));
        };

        const onBackdropClick = (event) => {
            if (event.target === modal) {
                onCancel();
            }
        };

        zoomInput.value = '1';
        offsetXInput.value = '0';
        offsetYInput.value = '0';

        zoomInput.addEventListener('input', onControlChange);
        offsetXInput.addEventListener('input', onControlChange);
        offsetYInput.addEventListener('input', onControlChange);
        cancelBtn.addEventListener('click', onCancel);
        saveBtn.addEventListener('click', onSave);
        modal.addEventListener('click', onBackdropClick);

        image.onload = () => {
            drawPreview();
            modal.classList.remove('hidden');
        };
        image.onerror = () => {
            finalize(() => reject(new Error('No se pudo abrir la imagen para recorte.')));
        };
        image.src = sourceDataUrl;
    });
}

async function handleProfileSubmit(event) {
    event.preventDefault();

    const fullname = document.getElementById('client-fullname')?.value.trim() || '';
    const email = document.getElementById('client-email-input')?.value.trim().toLowerCase() || '';
    const currentPassword = (document.getElementById('client-current-password')?.value || '').trim();
    const password = (document.getElementById('client-password')?.value || '').trim();
    const confirmPassword = (document.getElementById('client-password-confirm')?.value || '').trim();
    const address = document.getElementById('client-address')?.value.trim() || '';
    const postalCode = document.getElementById('client-postal-code')?.value.trim() || '';
    const city = document.getElementById('client-city')?.value.trim() || '';
    const country = document.getElementById('client-country')?.value.trim() || '';

    if (!fullname || !email) {
        showSaveMessage('Nombre y correo son obligatorios.', true);
        return;
    }

    if (password && password.length < 6) {
        showSaveMessage('La contraseña debe tener al menos 6 caracteres.', true);
        return;
    }

    if (password && !currentPassword) {
        showSaveMessage('Debes introducir tu contraseña actual para cambiarla.', true);
        return;
    }

    if (password !== confirmPassword) {
        showSaveMessage('La confirmación de contraseña no coincide.', true);
        return;
    }

    const payload = {
        name: fullname,
        email
    };

    if (address) payload.address = address;
    if (postalCode) payload.postal_code = postalCode;
    if (city) payload.city = city;
    if (country) payload.country = country;
    if (password) {
        payload.old_password = currentPassword;
        payload.password = password;
        payload.confirm_password = confirmPassword;
    }

    const submitButton = event.target.querySelector('button[type="submit"]');
    if (submitButton) submitButton.disabled = true;

    try {
        const response = await SubsonicAPI.updateUserProfile(payload);
        if (response?.user) {
            localStorage.setItem(AUTH.USER_KEY, JSON.stringify(response.user));
        }

        const currentPasswordInput = document.getElementById('client-current-password');
        const passwordInput = document.getElementById('client-password');
        const confirmInput = document.getElementById('client-password-confirm');
        if (currentPasswordInput) currentPasswordInput.value = '';
        if (passwordInput) passwordInput.value = '';
        if (confirmInput) confirmInput.value = '';

        showSaveMessage('Perfil actualizado correctamente.', false);
        await refreshProfileAndOrders();
    } catch (error) {
        showSaveMessage(error.message || 'No se pudo guardar el perfil.', true);
    } finally {
        if (submitButton) submitButton.disabled = false;
    }
}

function setupClientMenuListeners() {
    const menuButtons = document.querySelectorAll('.menu-btn[data-section]');
    const sections = document.querySelectorAll('.profile-section-content');

    menuButtons.forEach((btn) => {
        btn.addEventListener('click', function() {
            const sectionKey = this.dataset.section;
            menuButtons.forEach((button) => button.classList.remove('active'));
            sections.forEach((section) => section.classList.remove('active'));
            this.classList.add('active');

            const targetSection = document.querySelector(`.profile-section-content[data-section="${sectionKey}"]`);
            if (targetSection) targetSection.classList.add('active');
        });
    });
}

function setupClientLogoutListeners() {
    const logoutBtn = document.getElementById('logout-btn');
    if (!logoutBtn) return;

    logoutBtn.addEventListener('click', () => {
        AUTH.logoutAndReloadToLogin();
    });
}

function showSaveMessage(message, isError) {
    const messageNode = document.getElementById('profile-save-message');
    if (!messageNode) return;

    messageNode.textContent = message;
    messageNode.classList.toggle('error', isError);
    messageNode.classList.toggle('success', !isError);
}

function buildAvatarFallback(name) {
    const safeName = encodeURIComponent((name || 'Cliente').trim());
    return `https://ui-avatars.com/api/?name=${safeName}&background=00d4ff&color=000&bold=true&size=120`;
}

function isTicketItem(item) {
    const type = String(item?.type || item?.category || '').toLowerCase();
    const name = String(item?.name || item?.event_name || '').toLowerCase();
    return type.includes('ticket') || type.includes('entrada') || name.includes('entrada');
}

function escapeHtml(value) {
    return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}



/* TK-003-1: cambio de email con verificación */
async function requestEmailChange() {
    const status = document.getElementById('profile-email-status');
    const email = document.getElementById('profile-new-email')?.value.trim();
    const password = document.getElementById('profile-current-password')?.value || '';
    if (!email || !password) {
        if (status) status.textContent = 'Introduce el nuevo correo y tu contraseña.';
        return;
    }
    try {
        const response = await SubsonicAPI.request('/profile', 'PUT', { email, password });
        if (status) {
            status.textContent = response.verification_required
                ? `Revisa ${email}. Token de prueba: ${response.verification_token}`
                : 'Perfil actualizado.';
        }
    } catch (error) {
        if (status) status.textContent = error.message || 'No se pudo solicitar el cambio.';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('profile-email-submit')?.addEventListener('click', requestEmailChange);
});
