class Sidebar extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <aside class="sidebar">
                <nav class="d-flex flex-sm-column justify-content-around justify-content-sm-start align-items-center gap-sm-2 h-100 py-2 py-sm-4">
                    <a href="perfil.html" class="hc-side-item"><i class="bi bi-person"></i><span>Perfil</span></a>
                    <a href="#" class="hc-side-item"><i class="bi bi-house"></i><span>Início</span></a>
                    <a href="#" class="hc-side-item"><i class="bi bi-info-square"></i><span>Sobre</span></a>
                    <a href="#" class="hc-side-item"><i class="bi bi-question-square"></i><span>Suporte</span></a>

                    <a href="../login/login.html" class="hc-side-item mt-sm-auto"><i class="bi bi-box-arrow-left"></i><span>Sair</span></a>
                </nav>
            </aside>
        `;
    }
}

customElements.define("hc-sidebar", Sidebar);