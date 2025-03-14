$(document).ready(function () {
    console.log("JavaScript Loaded!");

    /* =======================================================
    SECTION 1: Toggle Navigation Menu on Small Screens
    ======================================================= */

    // When the navbar toggle button is clicked, toggle the visibility of the navigation menu
    $(".navbar-toggler").click(function () {
        $("#navbarNav").toggleClass("show");
    });

    /* =======================================================
    SECTION 2: Smooth Scroll for Anchor Links
    ======================================================= */

    // Enable smooth scrolling when clicking on anchor links (links with #)
    $("a[href^='#']").on("click", function (event) {
        event.preventDefault();

        // Animate scrolling to the target section smoothly
        $("html, body").animate({
            scrollTop: $($.attr(this, "href")).offset().top
        }, 500);
    });
});
