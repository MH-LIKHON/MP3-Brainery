$(document).ready(function () {
    console.log("[DEBUG] Admin Dashboard JavaScript Loaded!");

    /* =======================================================
    SECTION 1: Sidebar Toggle Functionality
    ======================================================= */

    // Sidebar Toggle Functionality
    $(".sidebar-toggle").click(function () {
        $(".sidebar").toggleClass("collapsed");
    });

    // Close sidebar when clicking anywhere on the main content
    $(".flex-grow-1").click(function () {
        if (!$(".sidebar").hasClass("collapsed")) {
            $(".sidebar").addClass("collapsed");
        }
    });

    /* =======================================================
    SECTION 2: User Actions - Promote & Delete
    ======================================================= */

    // Get CSRF token from meta tag
    const csrfToken = document.querySelector("meta[name='csrf-token']").getAttribute("content");

    /**
     * Promote a user to admin
     * @param {string} userId - The ID of the user to be promoted
     */
    window.promoteUser = function (userId) {
        console.log("[DEBUG] Sending Promote Request for User ID:", userId);

        fetch(`/admin/promote/${userId}`, {
            method: "POST", // Send as POST request
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Include CSRF token for security
            },
            body: JSON.stringify({}) // Send an empty JSON body
        })
            .then(response => {
                console.log("[DEBUG] Promote Response Status:", response.status);
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    showPopupMessage("User promoted successfully!", "success"); // Show success message
                    setTimeout(() => location.reload(), 1000); // Refresh the page after success
                } else {
                    showPopupMessage(data.error || "Failed to promote user.", "error"); // Show error message
                }
            })
            .catch(error => {
                console.error("[DEBUG] Error:", error);
                showPopupMessage("An error occurred.", "error"); // Handle request errors
            });
    };

    /**
     * Delete a user
     * @param {string} userId - The ID of the user to be deleted
     */
    window.deleteUser = function (userId) {
        console.log("[DEBUG] Sending Delete Request for User ID:", userId);

        fetch(`/admin/delete/${userId}`, {
            method: "POST", // Send as POST request
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Include CSRF token for security
            },
            body: JSON.stringify({}) // Send an empty JSON body
        })
            .then(response => {
                console.log("[DEBUG] Delete Response Status:", response.status);
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    showPopupMessage("User deleted successfully!", "success"); // Show success message
                    setTimeout(() => location.reload(), 1000); // Refresh the page after success
                } else {
                    showPopupMessage(data.error || "Failed to delete user.", "error"); // Show error message
                }
            })
            .catch(error => {
                console.error("[DEBUG] Error:", error);
                showPopupMessage("An error occurred.", "error"); // Handle request errors
            });
    };

    /* =======================================================
    SECTION 3: Logout Functionality
    ======================================================= */

    $("#logout-button").click(function () {
        window.location.href = "/auth/logout";
    });


    /* =======================================================
    SECTION 4: Popup Message Functionality
    ======================================================= */

    /**
     * Display a temporary popup message
     * @param {string} message - Message to display
     * @param {string} type - "success" or "error"
     */
    function showPopupMessage(message, type) {
        const popup = $("<div>").addClass("popup-message").text(message); // Create message box

        popup.css({
            "position": "fixed",
            "top": "50%",
            "left": "50%",
            "transform": "translate(-50%, -50%)",
            "background-color": type === "success" ? "#28a745" : "#dc3545", // Green for success, red for error
            "color": "white",
            "padding": "15px 20px",
            "border-radius": "8px",
            "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
            "z-index": "9999",
            "opacity": "1",
            "transition": "opacity 0.5s ease-in-out"
        });

        $("body").append(popup); // Append popup message to body

        setTimeout(() => {
            popup.fadeOut(500, function () {
                $(this).remove(); // Remove message after fade out
            });
        }, 2000);
    }

    /* =======================================================
    SECTION 5: Debugging - Check Button Clicks
    ======================================================= */

    $(".icon-promote, .icon-delete").on("click", function () {
        console.log("[DEBUG] Button Clicked:", this);
    });
});
