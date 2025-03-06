$(document).ready(function () {
    console.log("JavaScript Loaded!");

    /* =======================================================
    SECTION 1: Toggle Navigation Menu on Small Screens
    ======================================================= */
    // When the hamburger menu icon (navbar-toggler) is clicked, toggle the "show" class on the navbar menu
    $(".navbar-toggler").click(function () {
        $("#navbarNav").toggleClass("show");  // This will either show or hide the menu on smaller screens
    });

    /* =======================================================
    SECTION 2: Smooth Scroll for Anchor Links
    ======================================================= */
    // When an anchor link (link to an element with an ID) is clicked, enable smooth scrolling
    $("a[href^='#']").on("click", function (event) {
        event.preventDefault();  // Prevent the default anchor click behavior (page jump)

        // Animate scrolling to the section with the corresponding ID
        $("html, body").animate({
            scrollTop: $($.attr(this, "href")).offset().top  // Get the target section's offset and scroll to it
        }, 500); // The scroll animation will take 500ms
    });
});
