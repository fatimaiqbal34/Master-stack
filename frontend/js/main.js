document.addEventListener("DOMContentLoaded", () => {

    const currentPage = window.location.pathname.split("/").pop() || "index.html";

    const navHTML = `
        <nav class="navbar">
            <div class="container nav-inner">

                <a href="index.html" class="logo">
                    Fatima<span>.</span>Iqbal
                </a>

                <button class="menu-btn" id="menuBtn">
                    ☰
                </button>

                <div class="nav-links" id="navLinks">
                    <a href="index.html">Home</a>
                    <a href="stack.html">AI Stack</a>
                    <a href="agents.html">Agents</a>
                    <a href="projects.html">Projects</a>
                    <a href="skills.html">Skills</a>
                    <a href="about.html">About</a>
                    <a href="agents.html" class="nav-button">Try Agents →</a>
                </div>

            </div>
        </nav>
    `;

    document.body.insertAdjacentHTML("afterbegin", navHTML);

    const footerHTML = `
        <footer>
            <div class="container footer-inner">

                <div>
                    <div class="footer-name">Fatima Iqbal</div>
                    <div class="copyright">
                        © 2026 Fatima Iqbal. All rights reserved.
                    </div>
                </div>

                <div class="footer-links">
                    <a href="https://github.com/fatimaiqbal34"
                       target="_blank">
                        GitHub
                    </a>

                    <a href="https://fatimaiqbal34.github.io/my-portfolio/"
                       target="_blank">
                        Portfolio
                    </a>
                </div>

            </div>
        </footer>
    `;

    document.body.insertAdjacentHTML("beforeend", footerHTML);

    /* Mobile menu */

    const menuBtn = document.getElementById("menuBtn");
    const navLinks = document.getElementById("navLinks");

    menuBtn.addEventListener("click", () => {
        navLinks.classList.toggle("open");
    });

    /* Active page */

    document.querySelectorAll(".nav-links a").forEach(link => {
        const href = link.getAttribute("href");

        if (href === currentPage) {
            link.classList.add("active");
        }
    });

});