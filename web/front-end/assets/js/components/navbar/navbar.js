class Navbar extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <header>
                <nav class="navbar hc-nav px-3 px-md-5 py-3">
                    <ul class="navbar-nav flex-row gap-4 gap-md-5 ms-auto">
                        <li class="nav-item"><a class="nav-link" href="#login">Início</a></li>
                        <li class="nav-item"><a class="nav-link" href="#sobre-nos">Sobre Nós</a></li>
                        <li class="nav-item"><a class="nav-link" href="#suporte">Suporte</a></li>
                        <li class="nav-item"><a class="nav-link fw-bold" href="https://aacd.org.br/" target="_blank" rel="noopener">AACD</a></li>
                    </ul>
                </nav>
            </header>
        `;
    }
}

customElements.define("hc-navbar", Navbar);