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
    // 🔹 Load Subjects (Main Categories)
    // ==============================
    function loadSubjects() {
        $.getJSON("/dashboard/subjects", function (subjects) {
            let subjectsHtml = `<div class="list-group">`;

            subjects.forEach(subject => {
                subjectsHtml += `
                    <button class="list-group-item list-group-item-action subject-item" data-id="${subject._id}">
                        ${subject.icon} ${subject.name}
                    </button>`;
            });

            subjectsHtml += `</div>`;
            $("#subject-list").html(subjectsHtml);
        }).fail(function () {
            showToast("❌ Error: Could not load subjects.", "danger");
        });
    }

    // ==============================
    // 🔹 Load Topics for a Subject
    // ==============================
    function loadTopics(subjectId) {
        if (!subjectId) return;

        $("#subject-title").text("📚 Loading Topics...");
        $.getJSON(`/dashboard/topics/${subjectId}`, function (topics) {
            let topicsHtml = `<div class="row row-cols-1 row-cols-md-2 g-3">`;

            topics.forEach(topic => {
                topicsHtml += `
                    <div class="col">
                        <div class="card shadow-sm p-3">
                            <div class="card-body text-center">
                                <h6 class="fw-bold mb-2">${topic.title}</h6>
                                <p class="text-muted small">${topic.description}</p>
                                <button class="btn btn-primary btn-sm view-topic" data-title="${topic.title}">🔍 View</button>
                                <button class="btn btn-success btn-sm save-topic" data-title="${topic.title}">💾 Save</button>
                            </div>
                        </div>
                    </div>`;
            });

            topicsHtml += `</div>`;
            $("#study-content").html(topicsHtml);
            $("#subject-title").text("📌 Topics");
        }).fail(function () {
            showToast("❌ Error: Could not load topics.", "danger");
        });
    }

    // ==============================
    // 🔹 View Topic in Live Popup
    // ==============================
    $(document).on("click", ".view-topic", function () {
        let topicTitle = $(this).data("title");
        let wikiUrl = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(topicTitle)}`;

        $.getJSON(wikiUrl, function (data) {
            if (data.type === "standard") {
                let popupHtml = `
                    <div class="modal fade" id="topicModal" tabindex="-1">
                        <div class="modal-dialog modal-lg">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">${data.title}</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <p>${data.extract}</p>
                                    <a href="${data.content_urls.desktop.page}" target="_blank" class="btn btn-primary">Read More on Wikipedia</a>
                                </div>
                            </div>
                        </div>
                    </div>`;

                $("body").append(popupHtml);
                $("#topicModal").modal("show");
            } else {
                showToast("❌ No Wikipedia data found.", "danger");
            }
        }).fail(function () {
            showToast("❌ Error: Could not load topic details.", "danger");
        });
    });

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
            success: function () {
                showToast("✅ Topic saved!");
                loadSavedTopics();
            },
            error: function () {
                showToast("❌ Error: Could not save topic.", "danger");
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
                data.forEach(topic => {
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
                                    <button class="btn btn-primary btn-sm view-topic mt-2" data-title="${topic.title}">🔍 View</button>
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

    // ✅ Load Subjects on Page Load
    loadSubjects();

    // ✅ Load Topics when Subject is Clicked
    $(document).on("click", ".subject-item", function () {
        let subjectId = $(this).data("id");
        loadTopics(subjectId);
    });

    // ✅ Load Saved Topics on Button Click
    $("#load-saved-topics").click(function () {
        loadSavedTopics();
    });

    // ✅ Load Saved Topics on Page Load
    loadSavedTopics();
});
