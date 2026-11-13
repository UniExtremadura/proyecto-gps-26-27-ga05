/** Efecto decorativo de fondo: red neuronal luminosa. */
(function () {
    let canvas = null;
    let context = null;
    let particles = [];
    let animationFrame = null;
    let colorA = [0, 212, 255];
    let colorB = [157, 0, 255];

    function rgba(color, alpha) {
        return `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${alpha})`;
    }

    function ensureCanvas() {
        canvas = document.getElementById('neural-glow-canvas');
        if (!canvas) {
            canvas = document.createElement('canvas');
            canvas.id = 'neural-glow-canvas';
            canvas.setAttribute('aria-hidden', 'true');
            document.body.prepend(canvas);
        }
        canvas.style.position = 'fixed';
        canvas.style.inset = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.zIndex = '0';
        canvas.style.pointerEvents = 'none';
        context = canvas.getContext('2d');
        resize();
    }

    function resize() {
        if (!canvas) return;
        canvas.width = globalThis.innerWidth;
        canvas.height = globalThis.innerHeight;
    }

    function createParticles() {
        const count = Math.min(80, Math.max(24, Math.floor(globalThis.innerWidth / 22)));
        particles = Array.from({ length: count }, () => ({
            x: Math.random() * (canvas?.width || 1),
            y: Math.random() * (canvas?.height || 1),
            vx: (Math.random() - 0.5) * 0.35,
            vy: (Math.random() - 0.5) * 0.35,
            radius: Math.random() * 1.8 + 0.6
        }));
    }

    function draw() {
        if (!context || !canvas) return;
        context.clearRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < particles.length; i += 1) {
            const particle = particles[i];
            particle.x += particle.vx;
            particle.y += particle.vy;

            if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;

            context.beginPath();
            context.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            context.fillStyle = rgba(colorA, 0.55);
            context.fill();

            for (let j = i + 1; j < particles.length; j += 1) {
                const other = particles[j];
                const dx = particle.x - other.x;
                const dy = particle.y - other.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < 130) {
                    context.beginPath();
                    context.moveTo(particle.x, particle.y);
                    context.lineTo(other.x, other.y);
                    context.strokeStyle = rgba(colorB, (1 - distance / 130) * 0.18);
                    context.lineWidth = 0.7;
                    context.stroke();
                }
            }
        }

        animationFrame = globalThis.requestAnimationFrame(draw);
    }

    function initNeuralGlow() {
        if (globalThis.matchMedia?.('(prefers-reduced-motion: reduce)').matches) return;
        ensureCanvas();
        createParticles();
        if (animationFrame) globalThis.cancelAnimationFrame(animationFrame);
        draw();
        globalThis.addEventListener('resize', resize, { passive: true });
    }

    function destroyNeuralGlow() {
        if (animationFrame) globalThis.cancelAnimationFrame(animationFrame);
        animationFrame = null;
        if (canvas) {
            const ctx = canvas.getContext('2d');
            ctx?.clearRect(0, 0, canvas.width, canvas.height);
        }
    }

    function setNeuralGlowColors(primary, secondary) {
        if (Array.isArray(primary)) colorA = primary;
        if (Array.isArray(secondary)) colorB = secondary;
    }

    globalThis.initNeuralGlow = initNeuralGlow;
    globalThis.destroyNeuralGlow = destroyNeuralGlow;
    globalThis.setNeuralGlowColors = setNeuralGlowColors;
})();
