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

    // Function to hide the sidebar when an option is selected
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
    // 🔹 Load Wikipedia Study Content
    // ==============================
    function loadStudyContent(topicId = null, subject = null) {
        $("#subject-title").text(subject || "📌 Saved Topic");
        $("#study-content").html("<p>Loading study materials...</p>");

        if (subject) {
            let wikiUrl = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(subject)}`;
            $.getJSON(wikiUrl, function (data) {
                if (data.type === "standard") {
                    let contentHtml = `
                        <h3>${data.title}</h3>
                        <p>${data.extract}</p>
                        <button class="btn btn-success btn-sm save-topic" data-title="${data.title}">💾</button>
                        <a href="${data.content_urls.desktop.page}" target="_blank" class="btn btn-primary btn-sm">Read More</a>
                    `;
                    $("#study-content").html(contentHtml);
                } else {
                    $("#study-content").html("<p>No study material found for this subject.</p>");
                }
            }).fail(function () {
                $("#study-content").html("<p>Error loading study materials. Try again later.</p>");
            });
        } else {
            $.getJSON(`/dashboard/get_topic/${topicId}`, function (data) {
                if (data) {
                    let contentHtml = `
                        <h3>${data.title}</h3>
                        <p>Saved topic content will be displayed here.</p>
                    `;
                    $("#study-content").html(contentHtml);
                } else {
                    $("#study-content").html("<p>Error: Topic not found.</p>");
                }
            }).fail(function () {
                $("#study-content").html("<p>Error loading saved topic.</p>");
            });
        }
    }

    // ==============================
    // 🔹 Save a Topic (CREATE)
    // ==============================
    $(document).on("click", ".save-topic", function () {
        let topicTitle = $(this).data("title");

        if (!topicTitle) {
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
                loadSavedTopics();
            },
            error: function (xhr) {
                showToast("❌ Error: Could not save the topic.", "danger");
            }
        });
    });

    // ==============================
    // 🔹 Load Saved Topics (READ)
    // ==============================
    function loadSavedTopics() {
        $("#subject-title").text("📌 Saved Topics");

        $.getJSON("/dashboard/saved_topics", function (data) {
            let savedHtml = `<div class="row row-cols-1 row-cols-md-3 g-3">`;

            if (data.length > 0) {
                data.forEach(function (topic) {
                    let savedDate = topic.timestamp
                        ? new Date(topic.timestamp).toLocaleString()
                        : "Unknown Date";

                    savedHtml += `
                        <div class="col">
                            <div class="card shadow-sm p-3 d-flex flex-column justify-content-between">
                                <div class="card-body text-center">
                                    <h6 class="fw-bold mb-2">${topic.title}</h6>
                                    <p class="text-muted small mb-1">
                                        <i class="fa-solid fa-calendar-days"></i> ${savedDate}
                                    </p>
                                    <button class="btn btn-success btn-sm open-topic mt-2" data-id="${topic._id}">
                                        🔗 Open
                                    </button>
                                </div>
                                <div class="d-flex justify-content-between px-2 mt-1">
                                    <button class="btn edit-topic border-0" data-id="${topic._id}" 
                                        style="color: #FFC107; font-size: 22px;">✏️</button>
                                    <button class="btn delete-topic border-0" data-id="${topic._id}" 
                                        style="color: #DC3545; font-size: 26px;">❌</button>
                                </div>
                            </div>
                        </div>`;
                });
            } else {
                savedHtml += "<p class='text-center text-muted'>No saved topics yet.</p>";
            }

            savedHtml += "</div>";
            $("#study-content").html(savedHtml);
        }).fail(function () {
            showToast("❌ Error: Could not load saved topics.", "danger");
        });

        autoCollapseSidebar();
    }

    // ✅ Fix for Open Topic Button
    $(document).on("click", ".open-topic", function () {
        let topicId = $(this).data("id");
        loadStudyContent(topicId);
    });

    // ==============================
    // 🔹 Rename a Topic (UPDATE)
    // ==============================
    $(document).on("click", ".edit-topic", function () {
        let topicId = $(this).data("id");
        let currentTitle = $(this).data("title");
        let newTitle = prompt("Enter new name for the topic:", currentTitle);

        if (newTitle && newTitle !== currentTitle) {
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
                    showToast("❌ Error: Could not update topic.", "danger");
                }
            });
        }
    });

    // ==============================
    // 🔹 Delete a Topic (DELETE)
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
                showToast("❌ Error: Could not delete topic.", "danger");
            }
        });
    });

    $(".subject-item").click(function () {
        let subject = $(this).data("subject");
        loadStudyContent(subject);
    });

    loadSavedTopics();
});
