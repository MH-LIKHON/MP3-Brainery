$(document).ready(function () {
    console.log("JavaScript Loaded!"); // Debugging step

    // Toggle Navigation Menu on Small Screens
    $(".navbar-toggler").click(function () {
        $("#navbarNav").toggleClass("show");
    });

    // Smooth Scroll for Anchor Links
    $("a[href^='#']").on("click", function (event) {
        event.preventDefault();
        $("html, body").animate({
            scrollTop: $($.attr(this, "href")).offset().top
        }, 500);
    });
});