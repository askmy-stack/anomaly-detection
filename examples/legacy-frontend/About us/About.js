// This code will add a smooth scroll to the about us page
$(document).ready(function () {
    $('a[href*="about"]').on('click', function (e) {
        e.preventDefault();

        // Get the href of the link that was clicked
        var href = $(this).attr('href');

        // Scroll to the about us section
        $('html, body').animate({
            scrollTop: $(href).offset().top
        }, 500);
    });
});
