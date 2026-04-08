const root = document.documentElement;
const themeToggles = document.querySelectorAll("#themeToggle, #themeToggleMobile");
const savedTheme = localStorage.getItem("theme");
const themeColorMeta = document.querySelector('meta[name="theme-color"]');

const syncTheme = (theme) => {
    const isLight = theme === "light";
    root.classList.toggle("light", isLight);
    localStorage.setItem("theme", isLight ? "light" : "dark");

    themeToggles.forEach((toggle) => {
        toggle?.setAttribute("aria-pressed", isLight ? "true" : "false");
        toggle?.setAttribute("title", isLight ? "Switch to dark mode" : "Switch to light mode");
    });

    if (themeColorMeta) {
        themeColorMeta.setAttribute("content", isLight ? "#f8fafc" : "#0f172a");
    }
};

syncTheme(savedTheme === "light" ? "light" : "dark");

themeToggles.forEach((toggle) => {
    toggle?.addEventListener("click", () => {
        syncTheme(root.classList.contains("light") ? "dark" : "light");
    });
});

if (window.AOS) {
    AOS.init({
        duration: 700,
        easing: "ease-out-cubic",
        once: true,
        offset: 40,
    });
}

const scrollButton = document.getElementById("scrollToTop");
window.addEventListener("scroll", () => {
    if (!scrollButton) {
        return;
    }
    scrollButton.classList.toggle("is-visible", window.scrollY > 500);
});

scrollButton?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});

document.querySelectorAll("[data-counter]").forEach((counter) => {
    const rawValue = counter.dataset.counter || counter.textContent;
    const numeric = parseInt(String(rawValue).replace(/[^\d]/g, ""), 10);
    if (Number.isNaN(numeric)) {
        return;
    }

    let current = 0;
    const suffix = String(rawValue).replace(String(numeric), "");
    const step = Math.max(1, Math.ceil(numeric / 36));
    const updateCounter = () => {
        current += step;
        if (current >= numeric) {
            counter.textContent = `${numeric}${suffix}`;
            return;
        }
        counter.textContent = `${current}${suffix}`;
        requestAnimationFrame(updateCounter);
    };
    updateCounter();
});

const filterButtons = document.querySelectorAll("[data-filter]");
const projectCards = document.querySelectorAll("[data-project-card]");

filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const filter = button.dataset.filter;
        filterButtons.forEach((item) => item.classList.remove("is-active"));
        button.classList.add("is-active");

        projectCards.forEach((card) => {
            const matches = filter === "all" || card.dataset.filterValue === filter;
            card.style.display = matches ? "" : "none";
        });
    });
});

const messageField = document.getElementById("id_message");
const messageCount = document.getElementById("messageCount");

const syncMessageCount = () => {
    if (messageField && messageCount) {
        messageCount.textContent = String(messageField.value.length);
    }
};

messageField?.addEventListener("input", syncMessageCount);
syncMessageCount();

const attachToggle = document.getElementById("attachToggle");
const attachmentWrap = document.getElementById("attachmentWrap");

const syncAttachmentVisibility = () => {
    if (!attachToggle || !attachmentWrap) {
        return;
    }
    attachmentWrap.hidden = !attachToggle.checked;
};

attachToggle?.addEventListener("change", syncAttachmentVisibility);
syncAttachmentVisibility();

document.querySelectorAll("[data-project-gallery]").forEach((gallery) => {
    const activeImage = gallery.querySelector("[data-gallery-active-image]");
    const imageLabel = gallery.querySelector("[data-gallery-image-label]");
    const thumbnails = gallery.querySelectorAll("[data-gallery-thumb]");

    thumbnails.forEach((thumbnail) => {
        thumbnail.addEventListener("click", () => {
            if (!activeImage) {
                return;
            }

            activeImage.src = thumbnail.dataset.imageUrl || activeImage.src;
            activeImage.alt = thumbnail.dataset.imageAlt || activeImage.alt;

            if (imageLabel) {
                imageLabel.textContent = thumbnail.dataset.imageLabel || "Project View";
            }

            thumbnails.forEach((item) => {
                item.classList.remove("is-active");
                item.setAttribute("aria-pressed", "false");
            });

            thumbnail.classList.add("is-active");
            thumbnail.setAttribute("aria-pressed", "true");
        });
    });
});
