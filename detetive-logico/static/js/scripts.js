// Loading para Home
setTimeout(() => {
    window.location.href = urlHome;
}, 3000);

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


let tempo = 180;
const timer = document.getElementById('timer');

const countdown = setInterval(() => {
    tempo--;
    timer.textContent = tempo;
    if (tempo <= 0) {
        clearInterval(countdown);
        alert('⏰ Tempo Esgotado!');
        window.location.href = "/tutorial/verificar";
    }
}, 1000);


document.addEventListener('DOMContentLoaded', () => {
    const bloqueados = document.querySelectorAll('.bloqueado');

    bloqueados.forEach(card => {
        card.addEventListener('click', (e) => {
            e.preventDefault();
            alert('Este modo estará disponível em breve!');
        });
    });
});
