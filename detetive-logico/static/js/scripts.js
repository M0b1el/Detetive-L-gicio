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