document.addEventListener("DOMContentLoaded", () => {
    // 1. Highlight Active Navigation Item Automatically
    setActiveNavLink();

    // 2. Initialize Mobile Sidebar Toggle (if toggle button exists)
    initMobileMenu();
});

/**
 * Automatically sets the 'active' class on the sidebar link 
 * matching the current page URL.
 */
function setActiveNavLink() {
    const currentPath = window.location.pathname.split("/").pop() || "index.html";
    const navItems = document.querySelectorAll(".sidebar-nav .nav-item");

    navItems.forEach((link) => {
        const href = link.getAttribute("href");
        if (href === currentPath) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
}

/**
 * Handles mobile sidebar menu open/close toggling.
 */
function initMobileMenu() {
    const toggleBtn = document.getElementById("sidebarToggle");
    const sidebar = document.querySelector(".sidebar");

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener("click", () => {
            sidebar.classList.toggle("open");
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener("click", (e) => {
            if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
                sidebar.classList.remove("open");
            }
        });
    }
}

/**
 * Helper to display temporary toast notifications in UI.
 */
function showNotification(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 12px 20px;
        background: #1e293b;
        color: #fff;
        border: 1px solid var(--border);
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 1000;
        font-size: 0.9rem;
        transition: opacity 0.3s ease;
    `;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}