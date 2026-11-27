/* =========================================================
   ACESSIBILIDADE: UserWay + VLibras
   - UserWay: botão flutuante com ajustes (tamanho da letra, contraste,
     espaçamento, leitor de tela etc.).
   - VLibras: tradutor de Português para Libras (governo federal).

   Este arquivo só carrega os dois serviços. O bloco HTML do VLibras
   (<div vw ...>) fica no index.html.
   ========================================================= */

// 1) COLE AQUI o ID da conta do UserWay (cadastro grátis em userway.org;
//    o ID aparece em userway.org/code). Enquanto estiver vazio, o UserWay
//    NÃO é carregado e o VLibras continua funcionando normalmente.
const USERWAY_ACCOUNT_ID = "rEuKa3Z2Ns";

// 2) Posição do ícone do UserWay: 1 = topo direito, 2 = meio direito,
//    3 = canto inferior direito. (O VLibras fica na lateral direita.)
const USERWAY_POSICAO = "3";

// Endereço oficial do VLibras
const VLIBRAS_APP = "https://vlibras.gov.br/app";

/* ---------------------------------------------------------
   Carrega um script externo e avisa quando terminar
   --------------------------------------------------------- */
function carregarScript(src, atributos = {}, aoCarregar) {
    const script = document.createElement("script");
    script.src = src;
    script.async = true;

    Object.entries(atributos).forEach(([nome, valor]) => script.setAttribute(nome, valor));

    if (aoCarregar) script.onload = aoCarregar;
    script.onerror = () => console.warn("Acessibilidade: não foi possível carregar " + src);

    (document.body || document.head).appendChild(script);
}

/* ---------------------------------------------------------
   VLibras: só inicia DEPOIS que o script terminar de carregar
   --------------------------------------------------------- */
function iniciarVLibras() {
    carregarScript(VLIBRAS_APP + "/vlibras-plugin.js", {}, () => {
        new window.VLibras.Widget(VLIBRAS_APP);
    });
}

/* ---------------------------------------------------------
   UserWay: precisa do ID da conta
   --------------------------------------------------------- */
function iniciarUserWay() {
    if (!USERWAY_ACCOUNT_ID) {
        console.warn("Acessibilidade: UserWay desligado. Preencha USERWAY_ACCOUNT_ID em acessibilidade.js.");
        return;
    }

    carregarScript("https://cdn.userway.org/widget.js", {
        "data-account": USERWAY_ACCOUNT_ID,
        "data-position": USERWAY_POSICAO,
    });
}

function iniciarAcessibilidade() {
    // evita carregar duas vezes se este arquivo for incluído de novo
    if (window.__hcAcessibilidade) return;
    window.__hcAcessibilidade = true;

    iniciarVLibras();
    iniciarUserWay();
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciarAcessibilidade);
} else {
    iniciarAcessibilidade();
}
