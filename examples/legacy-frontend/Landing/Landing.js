document.getElementById("explore").addEventListener("click", function () {
    window.location.href = "explore.html";
});

window.onload = function () {
    // Animate the navbar when the page loads
    var navbar = document.getElementById("navbar");
    navbar.style.opacity = 0;
    navbar.style.height = 0;

    var animateNavbar = function () {
        navbar.style.opacity += 0.05;
        navbar.style.height += 5;

        if (navbar.style.opacity < 1) {
            setTimeout(animateNavbar, 10);
        }
    };

    animateNavbar();
};
