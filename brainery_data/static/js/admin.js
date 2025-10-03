$(document).ready(function () {
    console.log("[DEBUG] Admin Dashboard JavaScript Loaded!");

    /* =======================================================
    SECTION 1: Sidebar Toggle Functionality
    ======================================================= */

    // Sidebar Toggle Functionality
    $(".sidebar-toggle").click(function () {
        const s  = document.querySelector(".sidebar");
        const $s = $(s);
        const collapsing = !$s.hasClass("collapsed"); // true if we're about to collapse

        $s.toggleClass("collapsed");

        if (collapsing) {
            // collapsing: wait for transform transition to finish, then clear inline height
            const onEnd = (e) => {
            if (e.propertyName !== "transform") return;
            s.removeEventListener("transitionend", onEnd);
            if ($s.hasClass("collapsed")) {
                s.style.removeProperty("height");
                s.style.removeProperty("min-height");
            }
            };
            s.addEventListener("transitionend", onEnd);

            // fallback in case transitionend doesn’t fire
            setTimeout(() => {
            if ($s.hasClass("collapsed")) {
                s.style.removeProperty("height");
                s.style.removeProperty("min-height");
            }
            }, 400);
        } else {
            // expanding: re-apply height on next frame
            requestAnimationFrame(() => window.dispatchEvent(new Event("resize")));
        }
    });


    // Close sidebar when clicking anywhere on the main content (admin)
    $(".dashboard-content").click(function () {
        const s  = document.querySelector(".sidebar");
        const $s = $(s);

        if (!$s.hasClass("collapsed")) {
            $s.addClass("collapsed");

            const onEnd = (e) => {
            if (e.propertyName !== "transform") return;
            s.removeEventListener("transitionend", onEnd);
            if ($s.hasClass("collapsed")) {
                s.style.removeProperty("height");
                s.style.removeProperty("min-height");
            }
            };
            s.addEventListener("transitionend", onEnd);

            // fallback
            setTimeout(() => {
            if ($s.hasClass("collapsed")) {
                s.style.removeProperty("height");
                s.style.removeProperty("min-height");
            }
            }, 400);
        }
    });


    // Sidebar to match viewport height
    (function fixSidebarHeight(){
    const s = document.querySelector('.sidebar');
    if (!s) return;

    const apply = () => {
    // skip when collapsed (no need to set height while hidden)
    if (s.classList.contains("collapsed")) return;

    // prefer visualViewport on mobile, fallback to innerHeight
    const h = (window.visualViewport && window.visualViewport.height) || window.innerHeight || 0;

    // lock height so CSS can't override it
    s.style.setProperty("height", h + "px", "important");
    s.style.setProperty("min-height", h + "px", "important");
    };


    // apply now and on viewport changes
    apply();
    window.addEventListener('resize', apply);
    if (window.visualViewport) window.visualViewport.addEventListener('resize', apply);
    })();

    /* =======================================================
    SECTION 2: User Actions - Promote & Delete (API helpers)
    ======================================================= */

    // Get CSRF token from meta tag (robust)
    function getCsrf() {
        const meta = document.querySelector("meta[name='csrf-token']");
        return meta ? meta.getAttribute("content") : "";
    }
    const csrfToken = getCsrf();

    /**
     * Promote a user to admin (API helper)
     * @param {string|number} userId - The ID of the user to be promoted
     */
    window.promoteUser = function (userId) {
        console.log("[DEBUG] Sending Promote Request for User ID:", userId);

        fetch(`/admin/promote/${userId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest"
            },
            body: JSON.stringify({})
        })
        .then(response => {
            console.log("[DEBUG] Promote Response Status:", response.status);
            return response.json();
        })
        .then(data => {
            if (data.success) {
                showPopupMessage("User promoted successfully!", "success");
                setTimeout(() => location.reload(), 1000);
            } else {
                showPopupMessage(data.error || "Failed to promote user.", "error");
            }
        })
        .catch(error => {
            console.error("[DEBUG] Error:", error);
            showPopupMessage("An error occurred.", "error");
        });
    };

    /**
     * Delete a user (API helper)
     * @param {string|number} userId - The ID of the user to be deleted
     */
    window.deleteUser = function (userId) {
        console.log("[DEBUG] Sending Delete Request for User ID:", userId);

        fetch(`/admin/delete/${userId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest"
            },
            body: JSON.stringify({})
        })
        .then(response => {
            console.log("[DEBUG] Delete Response Status:", response.status);
            return response.json();
        })
        .then(data => {
            if (data.success) {
                showPopupMessage("User deleted successfully!", "success");
                setTimeout(() => location.reload(), 1000);
            } else {
                showPopupMessage(data.error || "Failed to delete user.", "error");
            }
        })
        .catch(error => {
            console.error("[DEBUG] Error:", error);
            showPopupMessage("An error occurred.", "error");
        });
    };

    /* =======================================================
    SECTION 2A: Delegated Click Handlers (prevent default + pass ID)
    ======================================================= */

    // Extract user id from element or its nearest row
    function extractUserId(el) {
        // Prefer explicit data-user-id on the clicked element
        let id = el.getAttribute && el.getAttribute("data-user-id");
        if (id) return id;
        // Fallback: find nearest ancestor that has data-user-id (e.g., <tr>)
        const row = el.closest && el.closest("[data-user-id]");
        return row ? row.getAttribute("data-user-id") : null;
    }

    // Intercept promote icon/button clicks
    $(document).on("click", ".icon-promote", function (e) {
        // Prevent anchor default navigation like href="/admin/promote/"
        e.preventDefault();
        const id = extractUserId(this);
        if (!id) {
            console.warn("[DEBUG] Promote clicked but no data-user-id found.");
            showPopupMessage("Missing user id for promote.", "error");
            return;
        }
        window.promoteUser(id);
    });

    // Intercept delete icon/button clicks
    $(document).on("click", ".icon-delete", function (e) {
        // Prevent anchor default navigation like href="/admin/delete/"
        e.preventDefault();
        const id = extractUserId(this);
        if (!id) {
            console.warn("[DEBUG] Delete clicked but no data-user-id found.");
            showPopupMessage("Missing user id for delete.", "error");
            return;
        }
        window.deleteUser(id);
    });

    /* =======================================================
    SECTION 3: Logout Functionality
    ======================================================= */

    $("#logout-button").click(function () {
        window.location.href = (window.APP_PREFIX || "") + "/auth/logout";
    });

    /* =======================================================
    SECTION 4: Popup Message Functionality
    ======================================================= */

    function showPopupMessage(message, type) {
        const popup = $("<div>").addClass("popup-message").text(message);

        popup.css({
            "position": "fixed",
            "top": "50%",
            "left": "50%",
            "transform": "translate(-50%, -50%)",
            "background-color": type === "success" ? "#28a745" : "#dc3545",
            "color": "white",
            "padding": "15px 20px",
            "border-radius": "8px",
            "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
            "z-index": "9999",
            "opacity": "1",
            "transition": "opacity 0.5s ease-in-out"
        });

        $("body").append(popup);

        setTimeout(() => {
            popup.fadeOut(500, function () {
                $(this).remove();
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





