$(document).ready(function () {
    console.log("Dashboard Loaded!");

    // ==============================
    // 🔹 Load Wikipedia Study Content
    // ==============================
    function loadStudyContent(subject) {
        $("#subject-title").text(subject);
        $("#study-content").html("<p>Loading study materials...</p>");

        let wikiUrl = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(subject)}`;

        $.getJSON(wikiUrl, function (data) {
            if (data.type === "standard") {
                let contentHtml = `
                    <h3>${data.title}</h3>
                    <p>${data.extract}</p>
                    <button class="btn btn-success save-topic" data-title="${data.title}">💾 Save Topic</button>
                    <a href="${data.content_urls.desktop.page}" target="_blank" class="btn btn-primary">Read More on Wikipedia</a>
                `;
                $("#study-content").html(contentHtml);
            } else {
                $("#study-content").html("<p>No study material found for this subject.</p>");
            }
        }).fail(function () {
            $("#study-content").html("<p>Error loading study materials. Try again later.</p>");
        });
    }

    // ==============================
    // 🔹 Save a Topic (CREATE)
    // ==============================
    $(document).on("click", ".save-topic", function () {
        let topicTitle = $(this).data("title");

        $.ajax({
            url: "/save_topic",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ title: topicTitle }),
            success: function (response) {
                alert(response.message);
                loadSavedTopics(); // Reload saved topics
            }
        });
    });

    // ==============================
    // 🔹 Load Saved Topics (READ)
    // ==============================
    function loadSavedTopics() {
        $.getJSON("/get_saved_topics", function (data) {
            let savedHtml = "";

            if (data.length > 0) {
                data.forEach(function (topic) {
                    savedHtml += `
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            <span class="topic-title">${topic.title}</span>
                            <div>
                                <button class="btn btn-warning btn-sm edit-topic" data-id="${topic._id}" data-title="${topic.title}">✏️ Edit</button>
                                <button class="btn btn-danger btn-sm delete-topic" data-id="${topic._id}">❌ Delete</button>
                            </div>
                        </li>`;
                });
            } else {
                savedHtml = "<p>No saved topics yet.</p>";
            }

            $("#saved-topics").html(savedHtml);
        });
    }

    // ==============================
    // 🔹 Rename a Topic (UPDATE)
    // ==============================
    $(document).on("click", ".edit-topic", function () {
        let topicId = $(this).data("id");
        let currentTitle = $(this).data("title");
        let newTitle = prompt("Enter new name for the topic:", currentTitle);

        if (newTitle && newTitle !== currentTitle) {
            $.ajax({
                url: `/update_topic/${topicId}`,
                method: "PUT",
                contentType: "application/json",
                data: JSON.stringify({ new_title: newTitle }),
                success: function (response) {
                    alert(response.message);
                    loadSavedTopics(); // Reload saved topics
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
            url: `/delete_topic/${topicId}`,
            method: "DELETE",
            success: function (response) {
                alert(response.message);
                loadSavedTopics(); // Reload saved topics
            }
        });
    });

    // ==============================
    // 🔹 Attach Click Event to Subject Items
    // ==============================
    $(".subject-item").click(function () {
        let subject = $(this).data("subject");
        loadStudyContent(subject);
    });

    // Load saved topics on page load
    loadSavedTopics();
});
