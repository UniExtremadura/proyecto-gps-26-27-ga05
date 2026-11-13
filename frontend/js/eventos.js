/* ================================================================
 *  eventos.js
 * ================================================================ */


/* ========================
 *  DATOS DE EVENTOS
 * ======================== */
const fallbackEvents = [
    {
        id: "riverland-fest-2026",
        artist: "RIVERLAND FEST 2026",
        type: "Festival",
        date: "20-06-2026",
        loc: "Pravia, Asturias",
        month: "06",
        cardImg: "./assets/img/riverland.png",
        heroImg: "./assets/img/riverland.png",
        description: "Festival de musica y cultura en el corazon de Asturias.",
        isMultiDay: true,
        prices: { general: 60, vip: 150, camping: 45 },
        lineup: [
            { name: "DJ Voltage", role: "Headliner", img: "" },
            { name: "Neon Shadow", role: "Support", img: "" },
            { name: "The Glitch", role: "Special Guest", img: "" }
        ]
    },
    {
        id: "boombastic-costa-del-sol-2026",
        artist: "BOOMBASTIC COSTA DEL SOL 2026",
        type: "Festival",
        date: "12-07-2026",
        loc: "Torre del Mar, Malaga",
        month: "07",
        cardImg: "./assets/img/boombastic.jpg",
        heroImg: "./assets/img/boombastic.jpg",
        description: "Festival de playa con el mejor ambiente del verano.",
        isMultiDay: true,
        prices: { general: 65, vip: 160, camping: 50 },
        lineup: [
            { name: "Beach Pulse", role: "Headliner", img: "" },
            { name: "Solar Noise", role: "Support", img: "" },
            { name: "Mar de Neon", role: "Guest", img: "" }
        ]
    },
    {
        id: "medusa-zevra-festival-2026",
        artist: "MEDUSA-ZEVRA FESTIVAL 2026",
        type: "Festival",
        date: "15-08-2026",
        loc: "Cullera, Valencia",
        month: "08",
        cardImg: "./assets/img/zevra.jpg",
        heroImg: "./assets/img/zevra.jpg",
        description: "Festival de musica y arte en la costa mediterranea.",
        isMultiDay: true,
        prices: { general: 70, vip: 170, camping: 55 },
        lineup: [
            { name: "Neon Storm", role: "Headliner", img: "" },
            { name: "Acid Circuit", role: "Support", img: "" },
            { name: "Synthex", role: "Guest", img: "" }
        ]
    }
];

let allEvents = [];

function getEventIdFromRoute() {
    const hash = globalThis.location.hash || "";
    const hashQuery = hash.includes("?") ? hash.slice(hash.indexOf("?") + 1) : "";
    const querySource = hashQuery || (globalThis.location.search || "").replace(/^\?/, "");
    const params = new URLSearchParams(querySource);
    return params.get("id") || "";
}

function openEventFromRouteIfAny() {
    const eventId = getEventIdFromRoute();
    if (!eventId) return;

    const exists = allEvents.some(function (ev) { return ev.id === eventId; });
    if (exists) {
        showDetail(eventId);
    }
}

function normalizeEvent(ev) {
    const location = ev.loc || ev.location || "";
    const cardImage = ev.cardImg || ev.image || ev.image_url || "";
    const heroImage = ev.heroImg || ev.image || ev.image_url || "";
    const artistName = ev.artist || ev.name || ev.title || "Festival";

    return {
        id: ev.id,
        artist: artistName,
        type: ev.type || "Festival",
        date: ev.date || "",
        loc: location,
        month: ev.month || "",
        cardImg: cardImage,
        heroImg: heroImage,
        description: ev.description || "",
        isMultiDay: Boolean(ev.isMultiDay),
        prices: ev.prices || {
            general: Number(ev.ticket_price) || 0,
            vip: Number(ev.ticket_price) ? Number(ev.ticket_price) * 2 : 0,
            camping: 0
        },
        lineup: Array.isArray(ev.lineup) ? ev.lineup : []
    };
}

function resolveLineupArtistImage(artist) {
    const rawImage =
        (artist && (artist.image || artist.img || artist.photo || artist.profile_image_url)) ||
        '';

    if (!rawImage) {
        return './assets/img/User.png';
    }

    let image = String(rawImage).trim();
    if (!image) {
        return './assets/img/User.png';
    }

    if (image.startsWith('/frontend/assets/')) {
        image = image.replace('/frontend/assets/', './assets/');
    }

    return image;
}

async function loadEventsFromApi() {
    try {
        const response = await SubsonicAPI.getAllEvents();
        const apiEvents = Array.isArray(response.data) ? response.data : [];

        if (!apiEvents.length) {
            allEvents = [...fallbackEvents];
            return;
        }

        allEvents = apiEvents.map(normalizeEvent);
    } catch (error) {
        console.error("No se pudieron cargar eventos desde API, usando fallback:", error);
        allEvents = [...fallbackEvents];
    }
}


/* ================================================================
 *   VISTA 1 LISTADO DE EVENTOS  (filtros avanzados + grid)
 * ================================================================ */

/* Variables de filtro */
let searchText = "";
let searchNameFilter = ""; // Búsqueda por nombre desde navbar
let selectedCities = [];
let dateStart = null;
let dateEnd = null;

/* Lista de ciudades reconocidas a nivel mundial (sin localizaciones exactas) */
const recognizedCities = [
    "Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Málaga",
    "Zaragoza", "Córdoba", "Valladolid", "Alicante", "Toledo", "Granada",
    "Cuenca", "Salamanca", "Cádiz", "Oviedo", "Murcia", "Palma", "Ibiza",
    "París", "Londres", "Berlín", "Ámsterdam", "Milán", "Roma", "Venecia",
    "Estocolmo", "Copenhague", "Viena", "Praga", "Varsovia", "Bruselas",
    "Zúrich", "Ginebra", "Estambul", "Atenas", "Barcelona", "Lisboa",
    "Nueva York", "Los Ángeles", "Chicago", "Miami", "San Francisco", "Boston",
    "Tokio", "Osaka", "Kioto", "Bangkok", "Singapur", "Hong Kong",
    "Sydney", "Melbourne", "Sídney", "Dubái", "Abu Dabi", "Tel Aviv",
    "Estambul", "Bangkok", "Manila", "Kuala Lumpur", "Ciudad de México",
    "Toronto", "Vancouver", "Montréal", "São Paulo", "Río de Janeiro",
    "Buenos Aires", "Santiago", "Lima", "Bogotá", "Cartagena"
].sort();

/** Convierte fecha YYYY-MM-DD a objeto Date */
function parseDate(dateStr) {
    if (!dateStr) return null;
    const [year, month, day] = dateStr.split('-');
    return new Date(year, month - 1, day);
}

/** Extrae la fecha de un evento (busca varias propiedades) */
function getEventDate(event) {
    if (event.date) {
        // Formato: "DD-MM-YYYY"
        const parts = event.date.split('-');
        if (parts.length === 3) {
            return new Date(parts[2], parts[1] - 1, parts[0]);
        }
    }
    if (event.start_date) {
        return parseDate(event.start_date);
    }
    return null;
}

/** Filtra eventos según búsqueda, ciudades y rango de fechas */
function filterEvents() {
    return allEvents.filter(function (ev) {
        // Búsqueda en múltiples campos
        let matchSearch = 
            ev.artist.toLowerCase().includes(searchText.toLowerCase()) ||
            (ev.name && ev.name.toLowerCase().includes(searchText.toLowerCase())) ||
            (ev.title && ev.title.toLowerCase().includes(searchText.toLowerCase())) ||
            (ev.description && ev.description.toLowerCase().includes(searchText.toLowerCase())) ||
            (ev.loc && ev.loc.toLowerCase().includes(searchText.toLowerCase())) ||
            (ev.location && ev.location.toLowerCase().includes(searchText.toLowerCase()));
        
        // Filtro de nombre desde navbar (comienza con)
        let matchName = true;
        if (searchNameFilter.trim().length > 0) {
            const eventName = (ev.name || ev.title || ev.artist || "").toLowerCase();
            matchName = eventName.startsWith(searchNameFilter.toLowerCase());
        }
        
        // Filtro de ciudades (múltiples seleccionadas)
        let matchCity = selectedCities.length === 0;
        if (!matchCity) {
            const eventCity = (ev.loc || ev.location || "").toLowerCase();
            matchCity = selectedCities.some(city => eventCity.includes(city.toLowerCase()));
        }
        
        // Filtro de fecha (rango)
        let matchDate = true;
        if (dateStart || dateEnd) {
            const eventDate = getEventDate(ev);
            if (eventDate) {
                if (dateStart) matchDate = matchDate && eventDate >= dateStart;
                if (dateEnd) matchDate = matchDate && eventDate <= dateEnd;
            } else {
                matchDate = false;
            }
        }
        
        return matchSearch && matchName && matchCity && matchDate;
    });
}

/** Renderiza el display de filtros activos */
function updateActiveFiltersDisplay() {
    const container = document.getElementById('activeFiltersDisplay');
    if (!container) return;
    
    const filters = [];
    
    // Agregar filtro de fecha si existe
    if (dateStart || dateEnd) {
        const startStr = dateStart ? dateStart.toLocaleDateString('es-ES') : '...';
        const endStr = dateEnd ? dateEnd.toLocaleDateString('es-ES') : '...';
        filters.push({
            text: `📅 ${startStr} → ${endStr}`,
            type: 'date'
        });
    }
    
    // Agregar filtros de ciudades
    selectedCities.forEach(city => {
        filters.push({
            text: `🏙️ ${city}`,
            type: 'city',
            value: city
        });
    });
    
    // Agregar filtro de nombre si existe
    if (searchNameFilter.trim().length > 0) {
        filters.push({
            text: `📝 ${searchNameFilter}`,
            type: 'name'
        });
    }
    
    if (filters.length === 0) {
        container.innerHTML = '<span class=\"no-filters-text\">Sin filtros aplicados</span>';
    } else {
        container.innerHTML = filters.map(f => {
            if (f.type === 'date') {
                return `<div class="filter-tag">${f.text} <span class="filter-tag-remove" onclick="clearDateFilter()">×</span></div>`;
            } else if (f.type === 'name') {
                return `<div class="filter-tag">${f.text} <span class="filter-tag-remove" onclick="clearNameFilter()">×</span></div>`;
            } else {
                return `<div class="filter-tag">${f.text} <span class="filter-tag-remove" onclick="removeCityFilter('${f.value}')">×</span></div>`;
            }
        }).join('');
    }
}

/** Limpia el filtro de fechas */
function clearDateFilter() {
    dateStart = null;
    dateEnd = null;
    document.getElementById('dateStart').value = '';
    document.getElementById('dateEnd').value = '';
    updateActiveFiltersDisplay();
    renderEvents();
}

/** Elimina una ciudad del filtro */
function removeCityFilter(city) {
    selectedCities = selectedCities.filter(c => c !== city);
    renderSelectedCities();
    updateActiveFiltersDisplay();
    renderEvents();
}

/** Limpia el filtro de nombre (búsqueda) */
function clearNameFilter() {
    searchNameFilter = "";
    const searchInput = document.getElementById('nameSearchInput');
    if (searchInput) {
        searchInput.value = '';
    }
    updateActiveFiltersDisplay();
    renderEvents();
}

/** Renderiza el display de ciudades seleccionadas */
function renderSelectedCities() {
    const container = document.getElementById('selectedCities');
    if (!container) return;
    
    if (selectedCities.length === 0) {
        container.innerHTML = '';
    } else {
        container.innerHTML = selectedCities.map(city => 
            `<div class=\"city-chip\">🏙️ ${city} <span class=\"city-chip-remove\" onclick=\"removeCityFilter('${city}')\">×</span></div>`
        ).join('');
    }
}

/** Renderiza sugerencias de ciudades basadas en búsqueda */
function updateCitySuggestions(query) {
    const container = document.getElementById('citySuggestions');
    if (!container) return;
    
    if (query.trim().length === 0) {
        container.style.display = 'none';
        return;
    }
    
    const qLower = query.toLowerCase();
    const filtered = recognizedCities.filter(city => 
        city.toLowerCase().includes(qLower) && !selectedCities.includes(city)
    );
    
    if (filtered.length === 0) {
        container.style.display = 'none';
    } else {
        container.innerHTML = filtered.map(city => 
            `<div class=\"city-suggestion-item\" onclick=\"selectCity('${city}')\">${city}</div>`
        ).join('');
        container.style.display = 'block';
    }
}

/** Selecciona una ciudad y la añade al filtro */
function selectCity(city) {
    if (!selectedCities.includes(city)) {
        selectedCities.push(city);
    }
    document.getElementById('citySearch').value = '';
    updateCitySuggestions('');
    renderSelectedCities();
    updateActiveFiltersDisplay();
    renderEvents();
}

/** Conecta los filtros y la barra de búsqueda */
function setupFilters() {
    const dateStartInput = document.getElementById('dateStart');
    const dateEndInput = document.getElementById('dateEnd');
    const citySearchInput = document.getElementById('citySearch');
    const clearAllBtn = document.getElementById('clearAllFilters');
    
    // Evento: cambio de fecha inicio
    if (dateStartInput && !dateStartInput.dataset.bound) {
        dateStartInput.dataset.bound = '1';
        dateStartInput.addEventListener('change', function () {
            dateStart = this.value ? parseDate(this.value) : null;
            updateActiveFiltersDisplay();
            renderEvents();
        });
    }
    
    // Evento: cambio de fecha fin
    if (dateEndInput && !dateEndInput.dataset.bound) {
        dateEndInput.dataset.bound = '1';
        dateEndInput.addEventListener('change', function () {
            dateEnd = this.value ? parseDate(this.value) : null;
            updateActiveFiltersDisplay();
            renderEvents();
        });
    }
    
    // Evento: búsqueda de ciudades
    if (citySearchInput && !citySearchInput.dataset.bound) {
        citySearchInput.dataset.bound = '1';
        citySearchInput.addEventListener('input', function () {
            updateCitySuggestions(this.value);
        });
        
        // Cerrar sugerencias al perder foco
        citySearchInput.addEventListener('blur', () => {
            setTimeout(() => {
                document.getElementById('citySuggestions').style.display = 'none';
            }, 200);
        });
    }
    
    // Evento: limpiar todos los filtros
    if (clearAllBtn && !clearAllBtn.dataset.bound) {
        clearAllBtn.dataset.bound = '1';
        clearAllBtn.addEventListener('click', function () {
            searchText = '';
            selectedCities = [];
            dateStart = null;
            dateEnd = null;
            searchNameFilter = "";
            
            if (dateStartInput) dateStartInput.value = '';
            if (dateEndInput) dateEndInput.value = '';
            if (citySearchInput) citySearchInput.value = '';
            
            renderSelectedCities();
            updateActiveFiltersDisplay();
            renderEvents();
        });
    }
    
    // Mostrar filtros activos al cargar
    updateActiveFiltersDisplay();
    renderSelectedCities();
}

/** Genera las tarjetas del grid */
function renderEvents() {
    let grid = document.getElementById("eventsGrid");
    if (!grid) return;
    grid.innerHTML = "";

    let events = filterEvents();

    events.forEach(function (ev) {
        let card = document.createElement("div");
        card.className = "event-card";

        card.innerHTML =
            /* --- Cabecera de la tarjeta (imagen + fecha + artista) --- */
            '<div class="event-header">' +
                /* IMAGEN TARJETA: si ev.cardImg está vacío se muestra el placeholder oscuro */
                (ev.cardImg
                    ? '<img class="event-header-img" src="' + ev.cardImg + '" alt="' + ev.artist + '">'
                    : '<!-- TODO: Añadir imagen de tarjeta para ' + ev.artist + ' -->') +
                '<span class="event-date">' + ev.date + '</span>' +
                '<h3 class="event-artist">' + ev.artist + '</h3>' +
            '</div>' +

            /* --- Cuerpo de la tarjeta (ubicación + precio + botón) --- */
            '<div class="event-body">' +
                '<div class="event-location">' +
                    '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24">' +
                        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" ' +
                            'd="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>' +
                        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" ' +
                            'd="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>' +
                    '</svg>' +
                    ev.loc +
                '</div>' +
                '<div class="event-price">' +
                    'Desde <strong>' + ev.prices.general + '€</strong>' +
                '</div>' +
                '<div class="event-card-actions">' +
                    '<button class="more-info-btn" data-id="' + ev.id + '">Más Info +</button>' +
                '</div>' +
            '</div>';

        grid.appendChild(card);

        /* Listener: abrir detalle al hacer click en cualquier parte de la tarjeta */
        card.addEventListener("click", function () {
            showDetail(ev.id);
        });
    });
}


/* ================================================================
 *  VISTA 2 – DETALLE DE UN EVENTO  (info + compra)
 * ================================================================ */

/* Estado del configurador de compra */
let quantity    = 1;
let ticketType  = "general";
let wantsCamping = false;
let campingZone  = "Norte";

/** Calcula el total según las opciones elegidas */
function computeTotal(prices) {
    let unit = prices[ticketType] + (wantsCamping ? prices.camping : 0);
    return unit * quantity;
}

/** Muestra la vista de detalle para el evento con id dado */
function showDetail(eventId) {
    let ev = allEvents.find(function (e) { return e.id === eventId; });
    if (!ev) return;

    /* Ocultar listado, mostrar detalle */
    document.getElementById("listingView").classList.add("hidden");
    document.getElementById("detailView").classList.remove("hidden");
    window.scrollTo(0, 0);

    /* Resetear estado de compra */
    quantity     = 1;
    ticketType   = "general";
    wantsCamping = false;
    campingZone  = "Norte";

    renderDetail(ev);
}

/** Vuelve al listado de eventos */
function backToListing() {
    document.getElementById("detailView").classList.add("hidden");
    document.getElementById("listingView").classList.remove("hidden");
    window.scrollTo(0, 0);
}

/** Genera todo el HTML del detalle */
function renderDetail(ev) {
    let container = document.getElementById("eventDetailContainer");
    if (!container) return;

    let role     = AUTH.getRole();
    let isBuyer  = role === "cliente" || role === "proveedor";
    let prices   = ev.prices;

    container.innerHTML =
        /* COLUMNA IZQUIERDA: INFO DEL EVENTO */
        '<div class="detail-info">' +

            /* Botón volver */
            '<button id="backBtn" class="back-btn">&larr; Volver a eventos</button>' +

            /* Hero del evento */
            '<div class="detail-hero">' +
                /* IMAGEN HERO: si heroImg está¡ vacío se muestra un degradado de fondo */
                (ev.heroImg
                    ? '<img class="detail-hero-img" src="' + ev.heroImg + '" alt="' + ev.artist + '">'
                    : '<!-- TODO: Añadir imagen hero para ' + ev.artist + ' -->') +
                '<div class="detail-hero-overlay"></div>' +
                '<div class="detail-hero-content">' +
                    '<span class="detail-badge">' +
                        (ev.isMultiDay ? "Múltiples días &bull; Festival" : "Evento") +
                    '</span>' +
                    '<h1 class="detail-title">' + ev.artist + '</h1>' +
                '</div>' +
            '</div>' +

            /* Fichas de fecha y ubicación */
            '<div class="detail-meta">' +
                '<div class="meta-card">' +
                    '<span class="meta-label">Fecha</span>' +
                    '<span class="meta-value">' + ev.date + '</span>' +
                '</div>' +
                '<div class="meta-card">' +
                    '<span class="meta-label">Ubicación</span>' +
                    '<span class="meta-value meta-value--accent">' + ev.loc + '</span>' +
                '</div>' +
            '</div>' +

            /* Descripción */
            '<div class="detail-section">' +
                '<h2>Sobre el evento</h2>' +
                '<p>' + ev.description + '</p>' +
            '</div>' +

            /* Lineup - solo mostrar si hay artistas */
            (ev.lineup && ev.lineup.length > 0
                ? '<div class="detail-section">' +
                    '<h2>Lineup</h2>' +
                    '<div class="lineup-grid">' +
                        ev.lineup.map(function (artist) {
                            const artistImage = resolveLineupArtistImage(artist);
                            return (
                                '<div class="lineup-card">' +
                                    '<div class="lineup-left">' +
                                        '<div class="lineup-avatar">' +
                                            '<img src="' + artistImage + '" alt="' + artist.name + '" onerror="this.src=\'./assets/img/User.png\'">' +
                                        '</div>' +
                                        '<div class="lineup-text">' +
                                            '<p class="lineup-name">' + artist.name + '</p>' +
                                            '<p class="lineup-role">' + artist.role + '</p>' +
                                        '</div>' +
                                    '</div>' +
                                '</div>'
                            );
                        }).join("") +
                    '</div>' +
                '</div>'
                : '') +

        '</div>' +

        /* ————– COLUMNA DERECHA: CONFIGURADOR DE COMPRA ————– */
        '<div class="detail-purchase">' +
            '<div class="purchase-card">' +
                '<h3 class="purchase-title">Configura tu pase</h3>' +

                /* 1. Tipo de acceso */
                '<div class="purchase-section">' +
                    '<p class="purchase-label">1. Tipo de Acceso</p>' +
                    '<div class="ticket-grid">' +
                        '<button id="btnGeneral" class="ticket-btn selected">General<br>' + prices.general + '&euro;</button>' +
                        '<button id="btnVip" class="ticket-btn">VIP &#9733;<br>' + prices.vip + '&euro;</button>' +
                    '</div>' +
                    '<p id="vipNote" class="vip-note hidden">Acceso a zonas exclusivas, fast-track y barras privadas.</p>' +
                '</div>' +

                /* 2. Acampada (only si es evento de varios días) */
                (ev.isMultiDay
                ? '<div class="purchase-section separator">' +
                    '<div class="camp-header">' +
                        '<p class="purchase-label">2. Acampada (+' + prices.camping + '&euro;)</p>' +
                        '<div id="campSwitch" class="flip-switch">' +
                            '<div class="thumb"></div>' +
                        '</div>' +
                    '</div>' +
                    '<div id="campOptions" class="camp-options hidden">' +
                        '<p class="camp-hint">Selecciona tu zona en el mapa</p>' +
                        '<div class="camp-map">' +
                            /* Aquí se puede poner una imagen de mapa real del recinto */
                            '<!-- TODO: Imagen de mapa del recinto -->' +
                            '<div class="camp-map-grid"></div>' +
                            '<div class="camp-map-venue">Recinto</div>' +
                            '<button id="zoneN" class="camp-zone camp-zone--top">Z. Norte</button>' +
                            '<button id="zoneS" class="camp-zone camp-zone--bottom">Z. Sur</button>' +
                            '<button id="zoneB" class="camp-zone camp-zone--right">Bosque</button>' +
                        '</div>' +
                    '</div>' +
                  '</div>'
                : '') +

                /* 3. Cantidad */
                '<div class="purchase-section separator">' +
                    '<p class="purchase-label">' + (ev.isMultiDay ? '3' : '2') + '. Personas</p>' +
                    '<div class="qty-selector">' +
                        '<button id="decQty" class="qty-btn">−</button>' +
                        '<div class="qty-display">' +
                            '<span id="qtyDisplay" class="qty-number">1</span>' +
                            '<span class="qty-sub">Entradas</span>' +
                        '</div>' +
                        '<button id="incQty" class="qty-btn qty-btn--accent">+</button>' +
                    '</div>' +
                '</div>' +

                /* Total */
                '<div class="purchase-total">' +
                    '<span class="total-label">Total Estimado</span>' +
                    '<span id="totalAmount" class="total-amount">0&euro;</span>' +
                '</div>' +

                /* Botón comprar */
                '<button id="purchaseBtn" class="purchase-btn ' + (isBuyer ? '' : 'disabled') + '">' +
                    (isBuyer ? 'Añadir al carrito' : 'Identifícate para comprar') +
                '</button>' +
                (isBuyer ? ''
                    : '<p class="purchase-note">Debes iniciar sesión para completar la reserva.</p>') +

            '</div>' +
        '</div>';

    /* Listeners del detalle */
    setupDetailListeners(ev, isBuyer);
}

/** Conecta todos los botones del configurador de compra */
function setupDetailListeners(ev, isBuyer) {
    let prices     = ev.prices;
    let btnGen     = document.getElementById("btnGeneral");
    let btnVip     = document.getElementById("btnVip");
    let vipNote    = document.getElementById("vipNote");
    let campSwitch = document.getElementById("campSwitch");
    let campOpts   = document.getElementById("campOptions");
    let zoneN      = document.getElementById("zoneN");
    let zoneS      = document.getElementById("zoneS");
    let zoneB      = document.getElementById("zoneB");
    let qtyDisp    = document.getElementById("qtyDisplay");
    let decQty     = document.getElementById("decQty");
    let incQty     = document.getElementById("incQty");
    let totalEl    = document.getElementById("totalAmount");
    let backBtn    = document.getElementById("backBtn");
    let purchaseBtn = document.getElementById("purchaseBtn");

    function refresh() {
        totalEl.textContent = computeTotal(prices) + "€";
    }

    /* Volver */
    backBtn.addEventListener("click", backToListing);

    /* Tipo de entrada */
    btnGen.addEventListener("click", function () {
        ticketType = "general";
        btnGen.classList.add("selected");
        btnVip.classList.remove("selected");
        vipNote.classList.add("hidden");
        refresh();
    });
    btnVip.addEventListener("click", function () {
        ticketType = "vip";
        btnVip.classList.add("selected");
        btnGen.classList.remove("selected");
        vipNote.classList.remove("hidden");
        refresh();
    });

    /* Acampada */
    if (campSwitch) {
        campSwitch.addEventListener("click", function () {
            wantsCamping = !wantsCamping;
            campSwitch.classList.toggle("on", wantsCamping);
            campOpts.classList.toggle("hidden", !wantsCamping);
            refresh();
        });
    }
    if (zoneN) {
        [zoneN, zoneS, zoneB].forEach(function (btn) {
            btn.addEventListener("click", function () {
                campingZone = btn.textContent.trim();
                [zoneN, zoneS, zoneB].forEach(function (b) {
                    b.classList.toggle("selected", b === btn);
                });
            });
        });
    }

    /* Cantidad */
    decQty.addEventListener("click", function () {
        if (quantity > 1) quantity--;
        qtyDisp.textContent = quantity;
        refresh();
    });
    incQty.addEventListener("click", function () {
        quantity++;
        qtyDisp.textContent = quantity;
        refresh();
    });

    /* Calcular total inicial */
    refresh();

    if (purchaseBtn) {
        purchaseBtn.addEventListener('click', function () {
            if (!isBuyer) {
                globalThis.showAuthRequiredModal();
                return;
            }

            const unitPrice = prices[ticketType] + (wantsCamping ? prices.camping : 0);
            const ticketName = `${ev.artist} - ${ticketType === 'vip' ? 'Entrada VIP' : 'Entrada General'}`;

            globalThis.SubsonicCart.addItem({
                id: `${ev.id}_${ticketType}_${wantsCamping ? 'camp' : 'nocamp'}`,
                event_id: ev.id,
                event_name: ev.artist,
                name: ticketName,
                type: 'Ticket',
                category: 'Festival',
                price: unitPrice,
                image: ev.cardImg || ev.heroImg || ev.image || ev.image_url || '',
                images: [ev.cardImg || ev.heroImg || ev.image || ev.image_url || ''].filter(Boolean),
                qty: quantity,
                camping: wantsCamping,
                camping_zone: wantsCamping ? campingZone : '',
                ticket_type: ticketType,
                location: ev.loc,
                event_date: ev.date,
                timestamp: Date.now()
            });

            alert('Entradas añadidas al carrito correctamente.');
        });
    }
}


/* ================================================================
 * INICIALIZACIÓN
 * ================================================================ */
document.addEventListener("DOMContentLoaded", function () {
    // Render inmediato para evitar vista vacía en la primera carga
    allEvents = [...fallbackEvents];
    renderEvents();
    setupFilters();
    openEventFromRouteIfAny();

    // Refrescar con datos reales de backend/Firebase en segundo plano
    loadEventsFromApi().then(() => {
        renderEvents();
        openEventFromRouteIfAny();
    });
});

globalThis.load_eventos = function () {
    if (!document.getElementById('eventsGrid')) return;

    // Render inmediato para evitar vista vacia al entrar por SPA
    allEvents = [...fallbackEvents];
    
    // Aplicar búsqueda desde navbar si existe
    const savedSearch = sessionStorage.getItem('eventSearchQuery');
    if (savedSearch) {
        searchText = savedSearch;
        searchNameFilter = savedSearch; // Agregar a filtro de nombre
        sessionStorage.removeItem('eventSearchQuery'); // Limpiar después de usar
        
        // Actualizar el campo de búsqueda si existe en la página
        let searchInput = document.getElementById('searchInput');
        if (searchInput && !searchInput.classList.contains('navbar-search-input')) {
            searchInput.value = searchText;
        }
    }
    
    renderEvents();
    setupFilters();
    openEventFromRouteIfAny();

    // Refresco en segundo plano con backend/Firebase
    loadEventsFromApi().then(() => {
        renderEvents();
        openEventFromRouteIfAny();
    });
};

function bootEventosWhenReady(retries = 20) {
    if (document.getElementById('eventsGrid')) {
        globalThis.load_eventos();
        return;
    }
    if (retries <= 0) return;
    globalThis.setTimeout(() => bootEventosWhenReady(retries - 1), 50);
}

bootEventosWhenReady();


/* ================================================================
 * TK-006-2: buscador de catálogo contra /api/catalog/events
 * ================================================================ */
async function searchCatalogFromApi(query = '', genre = '') {
    const status = document.getElementById('catalogSearchStatus');
    const params = new URLSearchParams({ q: query, genre, page: '1', page_size: '24' });
    try {
        if (status) status.textContent = 'Buscando...';
        const response = await fetch(`${App.API_URL}/catalog/events?${params.toString()}`);
        const payload = await response.json();
        const items = payload?.data?.items || [];
        if (status) status.textContent = `${payload?.data?.total || 0} festivales encontrados`;
        if (Array.isArray(items) && items.length) {
            allEvents = items.map((event) => ({
                ...event,
                artist: event.name || event.title || event.artist,
                loc: event.location || event.loc,
                cardImg: event.image || event.cardImg,
                heroImg: event.image || event.heroImg
            }));
            renderEvents();
        }
    } catch (error) {
        console.error('Error buscando catálogo:', error);
        if (status) status.textContent = 'No se pudo consultar el catálogo.';
    }
}

async function loadCatalogFilters() {
    try {
        const response = await fetch(`${App.API_URL}/catalog/filters`);
        const payload = await response.json();
        const select = document.getElementById('catalogGenreSelect');
        if (!select) return;
        (payload?.data?.genres || []).forEach((genre) => {
            const option = document.createElement('option');
            option.value = genre;
            option.textContent = genre;
            select.appendChild(option);
        });
    } catch (error) {
        console.warn('No se pudieron cargar los filtros de catálogo:', error);
    }
}

function bindCatalogSearch() {
    const input = document.getElementById('catalogSearchInput');
    const genre = document.getElementById('catalogGenreSelect');
    const button = document.getElementById('catalogSearchButton');
    if (!input || !button || button.dataset.bound === '1') return;
    button.dataset.bound = '1';
    const run = () => searchCatalogFromApi(input.value.trim(), genre?.value || '');
    button.addEventListener('click', run);
    input.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            run();
        }
    });
    loadCatalogFilters();
}

const originalLoadEventos = globalThis.load_eventos;
globalThis.load_eventos = async function () {
    if (originalLoadEventos) await originalLoadEventos();
    bindCatalogSearch();
};
