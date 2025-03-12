$(document).ready(function () {
    console.log("✅ Dashboard Loaded!");

    // Get CSRF token from meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // ==============================
    // 🔹 Sidebar Toggle Functionality
    // ==============================
    $(".sidebar-toggle").click(function () {
        $(".sidebar").toggleClass("collapsed");
    });

    $(".sidebar").addClass("collapsed");

    function autoCollapseSidebar() {
        $(".sidebar").addClass("collapsed");
    }

    // ==============================
    // 🔹 Show Toast Notification
    // ==============================
    function showToast(message, type = "success") {
        let toastContainer = $("#toast-container");
        if (toastContainer.length === 0) {
            $("body").append('<div id="toast-container" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;"></div>');
            toastContainer = $("#toast-container");
        }

        let toastHtml = `<div class="toast align-items-center text-white bg-${type} border-0 show" role="alert" aria-live="assertive" aria-atomic="true" style="margin-bottom: 10px;">
                            <div class="d-flex">
                                <div class="toast-body">${message}</div>
                                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                            </div>
                        </div>`;

        toastContainer.append(toastHtml);
        setTimeout(() => $(".toast").first().remove(), 3000);
    }

    // ==============================
    // 🔹 Load Subjects into Sidebar
    // ==============================
    function loadSubjects() {
        $.getJSON("/dashboard/subjects", function (subjects) {
            let subjectHtml = "";
            subjects.forEach(subject => {
                subjectHtml += `<li class="list-group-item list-group-item-action subject-item" data-id="${subject._id}">${subject.icon} ${subject.name}</li>`;
            });
            $("#subject-list").html(subjectHtml);
        }).fail(() => {
            showToast("❌ Error loading subjects.", "danger");
        });
    }

    // ==============================
    // 🔹 Load Topics for a Subject
    // ==============================
    $(document).on("click", ".subject-item", function () {
        let subjectId = $(this).data("id");
        $("#subject-title").text("📚 Topics");
        loadTopics(subjectId);
        autoCollapseSidebar();
    });

    function loadTopics(subjectId) {
        $.getJSON(`/dashboard/topics/${subjectId}`, function (topics) {
            let topicHtml = `<div class="row row-cols-1 row-cols-md-3 g-3">`;
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
            $("#study-content").html(topicHtml);
        }).fail(() => {
            showToast("❌ Error loading topics.", "danger");
        });
    }

    // ==============================
    // 🔹 Save a Topic (CREATE)
    // ==============================
    $(document).on("click", ".save-topic", function () {
        let topicTitle = $(this).data("title");

        if (!topicTitle || topicTitle.trim() === "") {
            showToast("❌ Error: Topic title is missing!", "danger");
            return;
        }

        $.ajax({
            url: "/dashboard/save_topic",
            method: "POST",
            contentType: "application/json",
            headers: { "X-CSRFToken": csrfToken },
            data: JSON.stringify({ title: topicTitle }),
            success: function (response) {
                showToast("✅ " + response.message);
                loadSavedTopics(); // Refresh saved topics after saving
            },
            error: function (xhr) {
                let errorMessage = xhr.responseJSON?.error || "Could not save the topic.";
                showToast("❌ Error: " + errorMessage, "danger");
            }
        });
    });

    // ==============================
    // 🔹 Load Saved Topics on Login
    // ==============================
    function loadSavedTopics() {
        $("#subject-title").text("📌 Saved Topics");

        $.getJSON("/dashboard/saved_topics", function (savedTopics) {
            let savedHtml = `<div class="row row-cols-1 row-cols-md-3 g-3">`;

            if (savedTopics.length > 0) {
                savedTopics.forEach(topic => {
                    let savedDate = topic.timestamp ? new Date(topic.timestamp).toLocaleString() : "Unknown Date";

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
                savedHtml += "<p class='text-center text-muted'>No saved topics yet.</p>";
            }

            savedHtml += "</div>";
            $("#study-content").html(savedHtml);
        }).fail(() => {
            showToast("❌ Error loading saved topics.", "danger");
        });

        autoCollapseSidebar();
    }

    // ==============================
    // 🔹 Open a Saved Topic
    // ==============================
    $(document).on("click", ".read-topic", function () {
        let topicTitle = $(this).data("title");

        if (!topicTitle) {
            showToast("❌ Error: No topic title provided!", "danger");
            return;
        }

        let wikiUrl = `https://en.wikipedia.org/wiki/${encodeURIComponent(topicTitle)}`;
        $("#wikiContent").attr("src", wikiUrl);
        $("#wikiModalLabel").text(topicTitle);
        $("#wikiModal").modal("show");
    });


    // ==============================
    // 🔹 Edit a Saved Topic
    // ==============================
    $(document).on("click", ".edit-topic", function () {
        let topicId = $(this).data("id");
        let newTitle = prompt("Enter new name for the topic:");

        if (newTitle) {
            $.ajax({
                url: `/dashboard/update_topic/${topicId}`,
                method: "PUT",
                contentType: "application/json",
                headers: { "X-CSRFToken": csrfToken },
                data: JSON.stringify({ new_title: newTitle }),
                success: function (response) {
                    showToast(response.message);
                    loadSavedTopics();
                },
                error: function () {
                    showToast("❌ Error updating topic.", "danger");
                }
            });
        }
    });

    // ==============================
    // 🔹 Delete a Saved Topic
    // ==============================
    $(document).on("click", ".delete-topic", function () {
        let topicId = $(this).data("id");

        $.ajax({
            url: `/dashboard/delete_topic/${topicId}`,
            method: "DELETE",
            headers: { "X-CSRFToken": csrfToken },
            success: function (response) {
                showToast(response.message);
                loadSavedTopics();
            },
            error: function () {
                showToast("❌ Error deleting topic.", "danger");
            }
        });
    });

    // ==============================
    // 🔹 Open Wikipedia Page in Popup Modal (For Subjects & Saved Topics)
    // ==============================
    $(document).on("click", ".open-topic", function () {
        let wikiTitle = $(this).data("wiki-title");  // Use stored Wikipedia title

        if (!wikiTitle) {
            showToast("❌ Error: No Wikipedia title found!", "danger");
            return;
        }

        // Generate Wikipedia URL
        let wikiUrl = `https://en.wikipedia.org/wiki/${encodeURIComponent(wikiTitle)}`;

        // Update the iframe source and show the modal
        $("#wikiContent").attr("src", wikiUrl);
        $("#wikiModalLabel").text(wikiTitle);
        $("#wikiModal").modal("show");
    });


    // ==============================
    // 🔹 Logout (Fixed)
    // ==============================
    $(document).on("click", "#logout-button", function () {
        $.ajax({
            url: "/dashboard/auth/logout",
            method: "POST",
            headers: { "X-CSRFToken": csrfToken },  // Ensure CSRF token is sent
            success: function (response) {
                showToast("✅ " + response.message);
                setTimeout(() => {
                    window.location.href = "/auth/login";  // Redirect after logout
                }, 1000);
            },
            error: function () {
                showToast("❌ Logout failed. Please try again.", "danger");
            }
        });
    });

    // ==============================
    // 🔹 Handle "Saved Topics" Button Click
    // ==============================
    $(document).on("click", "#load-saved-topics", function () {
        loadSavedTopics();  // Call the function to load saved topics
    });



    // Load subjects and saved topics on dashboard load
    loadSubjects();
    loadSavedTopics();
});
