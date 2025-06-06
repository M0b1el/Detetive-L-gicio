// Loading para Home (usado na tela inicial com loading)
if (typeof urlHome !== 'undefined') {
    setTimeout(() => {
        window.location.href = urlHome;
    }, 3000);
}

// Menu sanduíche
function toggleMenu() {
    const menu = document.getElementById("menu");
    if (menu.style.display === "flex") {
        menu.style.display = "none";
    } else {
        menu.style.display = "flex";
        menu.style.flexDirection = "column";
    }
}

// Timer do jogo
let tempoRestante = 300; // 5 minutos
let timerAtivo = false;

function iniciarTimer() {
    if (!timerAtivo) {
        timerAtivo = true;
        setInterval(atualizarTimer, 1000);
    }
}

function atualizarTimer() {
    if (tempoRestante <= 0) {
        clearInterval(timer);
        mostrarResultado(false, true);
        return;
    }

    const minutos = Math.floor(tempoRestante / 60).toString().padStart(2, '0');
    const segundos = (tempoRestante % 60).toString().padStart(2, '0');
    const tempoElemento = document.getElementById("tempo");
    if (tempoElemento) tempoElemento.textContent = `${minutos}:${segundos}`;
    tempoRestante--;
}

// Verificar se o jogador acertou
function verificarCulpado(nomeSelecionado) {
    clearInterval(timer);
    const acertou = nomeSelecionado === culpado;
    mostrarResultado(acertou, false);
}

// Exibe o resultado final
function mostrarResultado(acertou, tempoEsgotado) {
    const resultado = document.getElementById("resultado");
    resultado.classList.remove("oculto");

    if (tempoEsgotado) {
        resultado.textContent = "⏰ Tempo esgotado! Você perdeu!";
        resultado.style.color = "orange";
    } else if (acertou) {
        resultado.textContent = "🎉 Parabéns! Você acertou o culpado!";
        resultado.style.color = "lightgreen";
    } else {
        resultado.textContent = "❌ Resposta incorreta. Tente novamente!";
        resultado.style.color = "red";
    }

    // Desativa os botões de suspeito
    document.querySelectorAll(".btn-suspeito").forEach(btn => btn.disabled = true);
}

// Modo tutorial: exibir proposições clicando em dicas
document.querySelectorAll('.proposicao').forEach(item => {
    item.addEventListener('click', () => {
        item.classList.toggle('ativa');
    });
});

// Modo tutorial: marcar seleção de suspeitos
document.querySelectorAll('.btn-suspeito').forEach(botao => {
    botao.addEventListener('click', () => {
        const nome = botao.getAttribute('data-nome');
        verificarCulpado(nome);
    });
});

// Iniciar o jogo ao carregar se for o modo de jogo
window.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById("tempo")) {
        iniciarTimer();
    }
});
