$(document).ready(function () {
    console.log("✅ Dashboard Loaded!");

    /* =======================================================
     SECTION 1: CSRF Token Setup
    ======================================================= */

    // Retrieve CSRF token from the meta tag for security in AJAX requests
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    /* =======================================================
     SECTION 2: Sidebar Toggle Functionality
     ======================================================= */

    // When the sidebar toggle button is clicked, toggle the "collapsed" class
    $(".sidebar-toggle").click(function () {
        $(".sidebar").toggleClass("collapsed");
    });

    // Ensure the sidebar starts in a collapsed state on page load
    $(".sidebar").addClass("collapsed");

    // Function to automatically collapse the sidebar
    function autoCollapseSidebar() {
        $(".sidebar").addClass("collapsed");
    }

    /* =======================================================
    SECTION 3: Show Toast Notification
    ======================================================= */

    // Function to display a toast notification with a message and type
    function showToast(message, type = "success") {
        let toastContainer = $("#toast-container");

        // Create the toast container dynamically if it does not exist
        if (toastContainer.length === 0) {
            $("body").append('<div id="toast-container" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;"></div>');
            toastContainer = $("#toast-container");
        }

        // Construct the toast notification HTML structure
        let toastHtml = `<div class="toast align-items-center text-white bg-${type} border-0 show" role="alert" aria-live="assertive" aria-atomic="true" style="margin-bottom: 10px;">
                            <div class="d-flex">
                                <div class="toast-body">${message}</div>
                                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                            </div>
                        </div>`;

        // Append toast notification to the container
        toastContainer.append(toastHtml);

        // Automatically remove the toast after 3 seconds
        setTimeout(() => $(".toast").first().remove(), 3000);
    }

    /* =======================================================
    SECTION 4: Load Subjects into Sidebar
    ======================================================= */

    // Function to fetch and display the list of subjects in the sidebar
    function loadSubjects() {
        $.getJSON("/dashboard/subjects", function (subjects) {
            let subjectHtml = "";

            // Loop through each subject and create a list item
            subjects.forEach(subject => {
                subjectHtml += `<li class="list-group-item list-group-item-action subject-item" data-id="${subject._id}">${subject.icon} ${subject.name}</li>`;
            });

            // Insert the subjects into the sidebar
            $("#subject-list").html(subjectHtml);
        }).fail(() => {
            // Show an error message if subjects fail to load
            showToast("❌ Error loading subjects.", "danger");
        });
    }

    /* =======================================================
    SECTION 5: Load Topics for a Subject
    ======================================================= */

    // When a subject is clicked, fetch and display its topics
    $(document).on("click", ".subject-item", function () {
        let subjectId = $(this).data("id");

        // Update the page title to reflect the selected subject
        $("#subject-title").text("📚 Topics");

        // Load the topics associated with the selected subject
        loadTopics(subjectId);

        // Collapse the sidebar automatically after selection
        autoCollapseSidebar();
    });

    // Function to fetch and display topics for a given subject
    function loadTopics(subjectId) {
        $.getJSON(`/dashboard/topics/${subjectId}`, function (topics) {
            let topicHtml = `<div class="row row-cols-1 row-cols-md-3 g-3">`;

            // Loop through each topic and create a card for it
            topics.forEach(topic => {
                topicHtml += `
                    <div class="col">
                        <div class="card shadow-sm p-3">
                            <div class="card-body text-center">
                                <h6 class="fw-bold mb-2">${topic.title}</h6>
                                <p class="text-muted small">${topic.description}</p>
                                <button class="btn btn-info btn-sm read-topic mt-2" data-title="${topic.title}">🔗 Read More</button>
                                <button class="btn btn-success btn-sm save-topic mt-2" data-title="${topic.title}">💾 Save</button>
                            </div>
                        </div>
                    </div>`;
            });

            topicHtml += `</div>`;

            // Insert the topics into the study content section
            $("#study-content").html(topicHtml);
        }).fail(() => {
            // Show an error message if topics fail to load
            showToast("❌ Error loading topics.", "danger");
        });
    }

    /* =======================================================
    SECTION 6: Save a Topic (CREATE)
    ======================================================= */

    // When the save button is clicked, attempt to save the selected topic
    $(document).on("click", ".save-topic", function () {
        let topicTitle = $(this).data("title");

        // Validate that a topic title is provided before proceeding
        if (!topicTitle || topicTitle.trim() === "") {
            showToast("❌ Error: Topic title is missing!", "danger");
            return;
        }

        // Send an AJAX request to save the topic to the database
        $.ajax({
            url: "/dashboard/save_topic",
            method: "POST",
            contentType: "application/json",
            headers: { "X-CSRFToken": csrfToken },
            data: JSON.stringify({ title: topicTitle }),
            success: function (response) {
                // Show success message and refresh saved topics
                showToast("✅ " + response.message);
                loadSavedTopics();
            },
            error: function (xhr) {
                // Show error message if saving fails
                let errorMessage = xhr.responseJSON?.error || "Could not save the topic.";
                showToast("❌ Error: " + errorMessage, "danger");
            }
        });
    });

    /* =======================================================
    SECTION 7: Load Saved Topics on Login
    ======================================================= */

    // Function to fetch and display saved topics
    function loadSavedTopics() {
        // Update the page title to indicate saved topics
        $("#subject-title").text("📌 Saved Topics");

        // Send an AJAX request to fetch saved topics from the server
        $.getJSON("/dashboard/saved_topics", function (savedTopics) {
            let savedHtml = `<div class="row row-cols-1 row-cols-md-3 g-3">`;

            // Check if there are any saved topics
            if (savedTopics.length > 0) {
                savedTopics.forEach(topic => {
                    // Format timestamp for display or show "Unknown Date" if unavailable
                    let savedDate = topic.timestamp ? new Date(topic.timestamp).toLocaleString() : "Unknown Date";

                    // Create a card for each saved topic with relevant details and actions
                    savedHtml += `
                        <div class="col">
                            <div class="card shadow-sm p-3">
                                <div class="card-body text-center">
                                    <h6 class="fw-bold mb-2">${topic.title}</h6>
                                    <p class="text-muted small"><i class="fa-solid fa-calendar-days"></i> ${savedDate}</p>
                                    <button class="btn btn-success btn-sm open-topic mt-2" data-id="${topic._id}" data-wiki-title="${topic.wiki_title || topic.title}">🔗 Open</button>
                                    <button class="btn edit-topic border-0" data-id="${topic._id}" style="color: #FFC107; font-size: 22px;">✏️</button>
                                    <button class="btn delete-topic border-0" data-id="${topic._id}" style="color: #DC3545; font-size: 26px;">❌</button>
                                </div>
                            </div>
                        </div>`;
                });
            } else {
                // Display message if no saved topics are available
                savedHtml += "<p class='text-center text-muted'>No saved topics yet.</p>";
            }

            savedHtml += "</div>";

            // Insert the saved topics into the study content section
            $("#study-content").html(savedHtml);
        }).fail(() => {
            // Show an error message if the request fails
            showToast("❌ Error loading saved topics.", "danger");
        });

        // Collapse the sidebar automatically after loading topics
        autoCollapseSidebar();
    }

    /* =======================================================
    SECTION 8: Open a Saved Topic
    ======================================================= */

    // When a saved topic is clicked, open its Wikipedia page in a modal
    $(document).on("click", ".read-topic", function () {
        let topicTitle = $(this).data("title");

        // Validate that the topic title is available before proceeding
        if (!topicTitle) {
            showToast("❌ Error: No topic title provided!", "danger");
            return;
        }

        // Construct the Wikipedia URL for the selected topic
        let wikiUrl = `https://en.wikipedia.org/wiki/${encodeURIComponent(topicTitle)}`;

        // Set the iframe source to the Wikipedia page and update the modal title
        $("#wikiContent").attr("src", wikiUrl);
        $("#wikiModalLabel").text(topicTitle);

        // Display the Wikipedia modal
        $("#wikiModal").modal("show");
    });

    /* =======================================================
    SECTION 9: Edit a Saved Topic
    ======================================================= */

    // When the edit button is clicked, prompt the user to rename the topic
    $(document).on("click", ".edit-topic", function () {
        let topicId = $(this).data("id");

        // Prompt the user to enter a new topic title
        let newTitle = prompt("Enter new name for the topic:");

        // Proceed only if the user provides a new title
        if (newTitle) {
            // Send an AJAX request to update the topic title in the database
            $.ajax({
                url: `/dashboard/update_topic/${topicId}`,
                method: "PUT",
                contentType: "application/json",
                headers: { "X-CSRFToken": csrfToken },
                data: JSON.stringify({ new_title: newTitle }),
                success: function (response) {
                    // Show success message and refresh saved topics list
                    showToast(response.message);
                    loadSavedTopics();
                },
                error: function () {
                    // Show error message if updating fails
                    showToast("❌ Error updating topic.", "danger");
                }
            });
        }
    });

    /* =======================================================
     SECTION 10: Delete a Saved Topic
     ======================================================= */

    // When the delete button is clicked, remove the selected topic
    $(document).on("click", ".delete-topic", function () {
        let topicId = $(this).data("id");

        // Send an AJAX request to delete the topic from the database
        $.ajax({
            url: `/dashboard/delete_topic/${topicId}`,
            method: "DELETE",
            headers: { "X-CSRFToken": csrfToken },
            success: function (response) {
                // Show success message and refresh saved topics list
                showToast(response.message);
                loadSavedTopics();
            },
            error: function () {
                // Show error message if deletion fails
                showToast("❌ Error deleting topic.", "danger");
            }
        });
    });

    /* =======================================================
    SECTION 11: Open Wikipedia Page in Popup Modal
    ======================================================= */

    // When a topic is clicked, open its Wikipedia page in a modal
    $(document).on("click", ".open-topic", function () {
        let wikiTitle = $(this).data("wiki-title");

        // Validate that a Wikipedia title exists before proceeding
        if (!wikiTitle) {
            showToast("❌ Error: No Wikipedia title found!", "danger");
            return;
        }

        // Construct the Wikipedia URL for the selected topic
        let wikiUrl = `https://en.wikipedia.org/wiki/${encodeURIComponent(wikiTitle)}`;

        // Update the iframe source with the Wikipedia URL
        $("#wikiContent").attr("src", wikiUrl);

        // Update the modal title with the topic name
        $("#wikiModalLabel").text(wikiTitle);

        // Display the Wikipedia modal
        $("#wikiModal").modal("show");
    });

    /* =======================================================
        SECTION 12: Logout Functionality
    ======================================================= */

    // When the logout button is clicked, log the user out and redirect to login page
    $(document).on("click", "#logout-button", function () {
        const base = (window.APP_PREFIX || "");
        const userRole = $(this).data("role");
        
        // Get user role from button attribute
        const logoutEndpoint = base + "/auth/logout";

        // Server expects GET, do a simple redirect
        window.location.href = logoutEndpoint;
    });

    /* =======================================================
    SECTION 13: Handle "Saved Topics" Button Click
    ======================================================= */

    // When the "Saved Topics" button is clicked, load saved topics
    $(document).on("click", "#load-saved-topics", function () {
        loadSavedTopics();
    });

    /* =======================================================
    SECTION 14: Load Dashboard Data on Page Load
    ======================================================= */

    // Load subjects and saved topics automatically when the dashboard is loaded
    loadSubjects();
    loadSavedTopics();
});
