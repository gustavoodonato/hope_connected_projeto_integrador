/* =========================================================
   AS ROTAS
   chave = o que aparece depois do # no endereço (ex.: index.html#login)
   id    = id da <div class="tela"> que será mostrada
   publica: true  -> qualquer pessoa abre
   tipo           -> só quem entrou com esse tipo de conta abre
   ========================================================= */

const rotas = {
    "login":               { id: "login",               titulo: "Hope Connected",                       publica: true },
    "sobre-nos":           { id: "sobre-nos",           titulo: "Hope Connected | Sobre nós",           publica: true },
    "suporte":             { id: "suporte",             titulo: "Hope Connected | Suporte",             publica: true },
    "usuario-empresa":     { id: "usuario-empresa",     titulo: "Hope Connected | Empresa",             tipo: "empresa" },
    "usuario-solicitante": { id: "usuario-solicitante", titulo: "Hope Connected | Solicitante",         tipo: "aacd" },
};

// Para onde cada tipo de conta vai depois de entrar (os valores do <select> do login)
const TELA_DE_CADA_TIPO = {
    empresa: "usuario-empresa",
    aacd: "usuario-solicitante",
};

/* =========================================================
   SESSÃO PROVISÓRIA
   Só guarda o tipo de conta para decidir qual tela mostrar.
   Quem confirma de verdade que o usuário pode entrar é o back-end:
   quando ele existir, chame iniciarSessao() só depois que o servidor responder "ok".
   ========================================================= */

const CHAVE_SESSAO = "hc-tipo";

function iniciarSessao(tipo) {
    sessionStorage.setItem(CHAVE_SESSAO, tipo);
    location.hash = "#" + TELA_DE_CADA_TIPO[tipo]; // vai para a tela do usuário
}

function encerrarSessao() {
    sessionStorage.removeItem(CHAVE_SESSAO);
}

/* =========================================================
   MOSTRAR A TELA
   ========================================================= */

// Troca o endereço sem criar um item extra no histórico do navegador
function irPara(nome) {
    location.replace("#" + nome);
}

function mostrarTela(rota) {
    const tela = document.getElementById(rota.id);

    // se o id da rota não existe no HTML, avisa em vez de deixar a página em branco
    if (!tela) {
        console.error(`Rota sem tela: não existe <div id="${rota.id}"> no index.html`);
        return;
    }

    // esconde todas as telas
    document.querySelectorAll(".tela").forEach((t) => t.classList.add("d-none"));

    // mostra só a escolhida
    tela.classList.remove("d-none");
    document.title = rota.titulo;
    window.scrollTo(0, 0);
    marcarItemDoMenu();
}

// Deixa em destaque, no menu lateral, o item da tela atual.
// O componente do menu também deve chamar esta função quando terminar de ser desenhado.
function marcarItemDoMenu() {
    const hashAtual = location.hash || "#login";

    document.querySelectorAll(".hc-side-item").forEach((item) => {
        const ativo = item.getAttribute("href") === hashAtual;
        item.classList.toggle("active", ativo);

        if (ativo) item.setAttribute("aria-current", "page");
        else item.removeAttribute("aria-current");
    });
}

function atualizarTela() {
    const nome = location.hash.replace("#", "") || "login";
    const rota = Object.hasOwn(rotas, nome) ? rotas[nome] : null;

    // endereço que não existe: volta para o login
    if (!rota) return irPara("login");

    const tipoLogado = sessionStorage.getItem(CHAVE_SESSAO);

    if (nome === "login") {
        encerrarSessao(); // chegar no login é o mesmo que sair
    } else if (!rota.publica) {
        if (!tipoLogado) return irPara("login");                                  // não entrou
        if (rota.tipo !== tipoLogado) return irPara(TELA_DE_CADA_TIPO[tipoLogado]); // tela de outro tipo de conta
    }

    mostrarTela(rota);
}

// roda quando o hash muda (clicou num link ou no botão voltar)
window.addEventListener("hashchange", atualizarTela);

// roda uma vez ao abrir a página
atualizarTela();