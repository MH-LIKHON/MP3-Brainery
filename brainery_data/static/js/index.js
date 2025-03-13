document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Feature Modal System Loaded!");

    // Get the register page URL from the hidden input in index.html
    const registerUrl = document.getElementById("register-url")?.value || "/register";

    // Modal Content for Each Feature
    const modalContent = {
        contribute: {
            title: "📚 Become a Contributor",
            description: `
                <p>Brainery thrives because of passionate contributors like you! By sharing your knowledge, you empower others and build your reputation as an expert.</p>
                <h3>🔹 Ways to Contribute:</h3>
                <ul>
                    <li>✅ Upload educational materials (PDFs, videos, presentations)</li>
                    <li>✅ Write blogs and share insights on various topics</li>
                    <li>✅ Become a mentor and guide aspiring learners</li>
                    <li>✅ Suggest improvements and help refine course content</li>
                </ul>
                <h4 class="text-center mt-4">🚧 Contribution Portal Coming Soon 🚧</h4>
            `
        },
        courses: {
            title: "📖 Explore Our Interactive Courses",
            description: `
                <p>Our structured courses provide a hands-on learning experience tailored for beginners and professionals alike.</p>
                <h3>🌟 Popular Courses:</h3>
                <ul>
                    <li>💻 Web Development Masterclass</li>
                    <li>📊 Data Science & Machine Learning</li>
                    <li>🎨 UI/UX Design Fundamentals</li>
                    <li>📝 Creative Writing & Content Creation</li>
                    <li>🚀 Entrepreneurship & Business Strategy</li>
                </ul>
                <h4>📍 Course Features:</h4>
                <ul>
                    <li>✔ Live coding sessions & interactive quizzes</li>
                    <li>✔ Community discussion & Q&A forums</li>
                    <li>✔ Career guidance & resume-building support</li>
                </ul>
                <div class="text-center">
                    <a href="${registerUrl}" class="feature-btn mt-3">Join Now</a>
                </div>
            `
        },
        workshops: {
            title: "🎥 Live Workshops",
            description: `
                <p>We are launching expert-led live workshops covering diverse topics.</p>
                <h3>🛠 Upcoming Workshops:</h3>
                <ul>
                    <li>💡 AI & Future Technologies</li>
                    <li>🗣️ Public Speaking & Leadership</li>
                    <li>📊 Financial Literacy & Investing</li>
                    <li>🚀 Startup Growth Strategies</li>
                </ul>
                <p>Stay ahead by learning directly from industry experts!</p>
                <h4 class="text-center mt-4">🚧 Workshops Launching Soon 🚧</h4>
            `
        },
        career: {
            title: "🚀 Career Roadmap & Mentorship",
            description: `
                <h3>🔍 Find Your Ideal Career Path</h3>
                <p>Not sure which career suits you? Brainery's **step-by-step career roadmap** helps guide you toward success.</p>
                <h3>🔹 Career Growth Services:</h3>
                <ul>
                    <li>✅ One-on-one mentorship from industry leaders</li>
                    <li>✅ Resume and portfolio review sessions</li>
                    <li>✅ AI-driven personalized career suggestions</li>
                    <li>✅ Mock interviews with real recruiters</li>
                    <li>✅ Exclusive job opportunities & internships</li>
                </ul>
                <p>Leverage Brainery's resources to **fast-track your professional journey**.</p>
                <div class="text-center mt-3">
                    <a href="${registerUrl}" class="feature-btn">Join Brainery Now</a>
                </div>
            `
        }
    };

    // Function to Open a Modal
    function openModal(type) {
        if (!modalContent[type]) return;

        // Remove any existing modal to prevent duplication
        const existingModal = document.getElementById("dynamicModal");
        if (existingModal) existingModal.remove();

        // Create Modal HTML
        const modalHTML = `
            <div class="modal fade" id="dynamicModal" tabindex="-1" aria-labelledby="modalTitle" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content p-4">
                        <div class="modal-header">
                            <h2 class="modal-title" id="modalTitle">${modalContent[type].title}</h2>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">${modalContent[type].description}</div>
                    </div>
                </div>
            </div>
        `;

        // Inject Modal into DOM
        document.getElementById("dynamic-modal-container").innerHTML = modalHTML;

        // Show Modal
        const modalElement = new bootstrap.Modal(document.getElementById("dynamicModal"));
        modalElement.show();
    }

    // Attach Click Events to Feature Buttons
    document.querySelectorAll(".open-modal").forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            const type = this.getAttribute("data-type");
            openModal(type);
        });
    });
});
