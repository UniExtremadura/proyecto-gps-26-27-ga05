/**
 * TK-007-2: carga diferida de imágenes y recursos del catálogo.
 */
(function () {
    function loadImage(image) {
        const source = image.dataset.src;
        if (!source) return;
        image.src = source;
        image.removeAttribute('data-src');
        image.classList.add('lazy-loaded');
    }

    function initLazyImages() {
        const images = document.querySelectorAll('img[data-src]');
        if (!('IntersectionObserver' in globalThis)) {
            images.forEach(loadImage);
            return;
        }
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                loadImage(entry.target);
                observer.unobserve(entry.target);
            });
        }, { rootMargin: '200px 0px' });
        images.forEach((image) => observer.observe(image));
    }

    function prefetchOnIdle() {
        if (!('requestIdleCallback' in globalThis)) return;
        globalThis.requestIdleCallback(() => {
            ['eventos', 'tienda'].forEach((page) => {
                const link = document.createElement('link');
                link.rel = 'prefetch';
                link.href = `./paginas/${page}.html`;
                document.head.appendChild(link);
            });
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        initLazyImages();
        prefetchOnIdle();
    });

    globalThis.refreshLazyImages = initLazyImages;
})();
