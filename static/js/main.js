const root = document.documentElement;
const themeToggles = document.querySelectorAll("#themeToggle, #themeToggleMobile");
const themeColorMeta = document.querySelector('meta[name="theme-color"]');

const getSavedTheme = () => {
    try {
        return window.localStorage.getItem("theme");
    } catch (error) {
        return null;
    }
};

const persistTheme = (theme) => {
    try {
        window.localStorage.setItem("theme", theme);
    } catch (error) {
        // Ignore storage failures so the toggle still works for the current session.
    }
};

const syncTheme = (theme) => {
    const isLight = theme === "light";
    root.classList.toggle("light", isLight);
    persistTheme(isLight ? "light" : "dark");

    themeToggles.forEach((toggle) => {
        toggle?.setAttribute("aria-pressed", isLight ? "true" : "false");
        toggle?.setAttribute("aria-label", isLight ? "Switch to dark mode" : "Switch to light mode");
        toggle?.setAttribute("title", isLight ? "Switch to dark mode" : "Switch to light mode");
    });

    if (themeColorMeta) {
        themeColorMeta.setAttribute("content", isLight ? "#f8fafc" : "#0f172a");
    }
};

const savedTheme = getSavedTheme();
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

const whatsappWidget = document.querySelector("[data-whatsapp-widget]");
const whatsappWidgetToggle = document.getElementById("whatsappWidgetToggle");
const whatsappWidgetCard = document.getElementById("whatsappWidgetCard");
const whatsappChatIcon = document.querySelector('[data-whatsapp-icon="chat"]');
const whatsappCloseIcon = document.querySelector('[data-whatsapp-icon="close"]');

const syncWhatsAppWidget = (isOpen) => {
    if (!whatsappWidget || !whatsappWidgetToggle || !whatsappWidgetCard) {
        return;
    }

    whatsappWidget.classList.toggle("is-open", isOpen);
    whatsappWidgetToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    whatsappWidgetToggle.setAttribute("aria-label", isOpen ? "Close WhatsApp chat" : "Open WhatsApp chat");
    whatsappWidgetCard.hidden = !isOpen;
    whatsappWidgetCard.setAttribute("aria-hidden", isOpen ? "false" : "true");

    if (whatsappChatIcon) {
        whatsappChatIcon.hidden = isOpen;
    }
    if (whatsappCloseIcon) {
        whatsappCloseIcon.hidden = !isOpen;
    }
};

if (whatsappWidget && whatsappWidgetToggle && whatsappWidgetCard) {
    syncWhatsAppWidget(false);

    whatsappWidgetToggle.addEventListener("click", () => {
        const isOpen = whatsappWidgetToggle.getAttribute("aria-expanded") === "true";
        syncWhatsAppWidget(!isOpen);
    });

    document.addEventListener("click", (event) => {
        if (!whatsappWidget.classList.contains("is-open")) {
            return;
        }

        if (!whatsappWidget.contains(event.target)) {
            syncWhatsAppWidget(false);
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && whatsappWidget.classList.contains("is-open")) {
            syncWhatsAppWidget(false);
        }
    });
}

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

const welcomePopup = document.getElementById("welcomePopup");
const popupStorageKey = "portfolio_welcome_popup_dismissed_v2";

const closeWelcomePopup = () => {
    if (!welcomePopup) {
        return;
    }
    welcomePopup.hidden = true;
    welcomePopup.setAttribute("aria-hidden", "true");
    try {
        window.localStorage.setItem(popupStorageKey, "true");
    } catch (error) {
        // Ignore storage failures and just close the popup for the current view.
    }
};

if (welcomePopup) {
    let popupDismissed = false;
    try {
        popupDismissed = window.localStorage.getItem(popupStorageKey) === "true";
    } catch (error) {
        popupDismissed = false;
    }

    if (!popupDismissed) {
        window.setTimeout(() => {
            welcomePopup.hidden = false;
            welcomePopup.setAttribute("aria-hidden", "false");
        }, 700);
    }

    welcomePopup.querySelectorAll("[data-popup-close]").forEach((button) => {
        button.addEventListener("click", closeWelcomePopup);
    });

    const welcomePopupForm = document.getElementById("welcomePopupForm");
    welcomePopupForm?.addEventListener("submit", () => {
        try {
            window.localStorage.setItem(popupStorageKey, "true");
        } catch (error) {
            // Ignore storage failures so form submission still succeeds.
        }
    });

    welcomePopup.addEventListener("click", (event) => {
        if (event.target === welcomePopup) {
            closeWelcomePopup();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !welcomePopup.hidden) {
            closeWelcomePopup();
        }
    });
}
