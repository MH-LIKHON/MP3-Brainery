document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded! Waiting for user interaction...");

    // ✅ Initialize EmailJS
    emailjs.init("service_9fhnu4c");
    console.log("✅ EmailJS Initialized!");

    /* =======================================================
    SECTION 1: Element Selection
    ======================================================= */
    let packages = document.querySelectorAll(".package");
    let selectedPlanInput = document.getElementById("selected_plan");
    let personalInfo = document.getElementById("personal-info");
    let paymentForm = document.getElementById("payment-info");
    let passwordInfo = document.getElementById("password-info");
    let submitButton = document.querySelector("#password-info .submit-btn");
    let successMessage = document.getElementById("success-message");
    let registerForm = document.getElementById("registration-form");
    let nextButton = document.querySelector("#payment-info .next-btn");
    let errorMessageBox = document.getElementById("error-message-box");

    let cardNumber = document.querySelector('input[name="card_number"]');
    let expiryDate = document.querySelector('input[name="expiry_date"]');
    let cvv = document.querySelector('input[name="cvv"]');
    let promoCodeInput = document.getElementById("promo-code");
    let promoMessage = document.getElementById("promo-message");

    /* =======================================================
    SECTION 2: Reset Form on Page Reload
    ======================================================= */
    window.addEventListener("load", function () {
        console.log("Resetting form on page reload...");
        registerForm?.reset();
    });

    /* =======================================================
    SECTION 3: Hide Registration Form After Successful Submission & Auto-Clear Messages
    ======================================================= */
    if (successMessage && successMessage.classList.contains("show")) {
        console.log("Registration successful! Hiding the form...");
        registerForm.style.display = "none";
    }

    setTimeout(() => {
        document.querySelectorAll(".alert").forEach(alert => {
            alert.style.transition = "opacity 0.5s";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 500);
        });
    }, 5000);

    /* =======================================================
    SECTION 4: Package Selection Handling
    ======================================================= */
    packages.forEach(package => {
        package.addEventListener("click", function () {
            console.log("Package Selected:", this.dataset.name);
            packages.forEach(p => p.classList.remove("selected"));
            this.classList.add("selected");
            selectedPlanInput.value = `${this.dataset.name} - £${this.dataset.price}`;
            console.log("Selected Plan:", selectedPlanInput.value);
            personalInfo.style.display = "block";
            setTimeout(() => { personalInfo.style.opacity = 1; }, 100);
            personalInfo.scrollIntoView({ behavior: "smooth" });
        });
    });

    /* =======================================================
    SECTION 5: Field Validation & Error Handling
    ======================================================= */
    function showError(input, message) {
        let errorSpan = input.parentElement.querySelector(".error-message");
        if (!errorSpan) {
            errorSpan = document.createElement("span");
            errorSpan.classList.add("error-message");
            errorSpan.style.color = "red";
            input.parentElement.appendChild(errorSpan);
        }
        errorSpan.innerText = message;
        input.style.border = "2px solid red";
    }

    function clearErrors() {
        document.querySelectorAll(".error-message").forEach(el => el.remove());
        document.querySelectorAll("input").forEach(el => el.style.border = "");
    }

    /* =======================================================
    SECTION 6: Step Navigation & Validation (Next Button)
    ======================================================= */
    function nextStep(currentId, nextId) {
        let currentSection = document.getElementById(currentId);
        let nextSection = document.getElementById(nextId);

        if (!currentSection || !nextSection) {
            console.error("ERROR: Missing section IDs", currentId, nextId);
            return;
        }

        clearErrors();
        let requiredFields = currentSection.querySelectorAll("input[required]");
        let emptyFields = Array.from(requiredFields).filter(input => input.value.trim() === "");

        let isPromoApplied = promoCodeInput.value.trim() === "CI25MP3";
        if (isPromoApplied && currentId === "payment-info") {
            emptyFields = emptyFields.filter(input => !["card_number", "expiry_date", "cvv"].includes(input.name));
        }

        if (emptyFields.length > 0) {
            emptyFields.forEach(input => showError(input, "This field is required."));
            emptyFields[0].focus();
            return;
        }

        console.log(`Transitioning from ${currentId} to ${nextId}`);
        currentSection.style.opacity = 0;
        setTimeout(() => {
            currentSection.style.display = "none";
            nextSection.style.display = "block";
            setTimeout(() => { nextSection.style.opacity = 1; }, 100);
            nextSection.scrollIntoView({ behavior: "smooth" });
        }, 200);
    }

    window.nextStep = nextStep;

    /* =======================================================
    SECTION 7: Expiry Date Validation
    ======================================================= */
    function validateExpiryDate(expiryDate) {
        let [month, year] = expiryDate.split("/").map(Number);
        return !(isNaN(month) || isNaN(year) || month < 1 || month > 12 || year < 25 || (year === 25 && month < 3));
    }

    /* =======================================================
    SECTION 8: Payment Form Submission & Validation
    ======================================================= */
    paymentForm.addEventListener("submit", function (event) {
        event.preventDefault();
        clearErrors();

        let isPromoApplied = promoCodeInput.value.trim() === "CI25MP3";
        if (!isPromoApplied) {
            if (!validateExpiryDate(expiryDate.value.trim())) {
                showError(expiryDate, "Expiry date must be March 2025 (03/25) or later.");
                return;
            }
            if (!cardNumber.value.trim()) {
                showError(cardNumber, "Card number is required.");
                return;
            }
            if (!cvv.value.trim()) {
                showError(cvv, "CVV is required.");
                return;
            }
        }

        console.log("Payment Validated. Moving to Password Section...");
        nextStep("payment-info", "password-info");
    });

    /* =======================================================
    SECTION 9: Promo Code Handling
    ======================================================= */
    function applyPromoCode() {
        let promoCodeValue = promoCodeInput.value.trim();
        let isValidPromo = promoCodeValue === "CI25MP3";

        promoMessage.innerText = isValidPromo ? "Promo applied! No payment required." : "Invalid promo code.";
        promoMessage.style.color = isValidPromo ? "green" : "red";

        [cardNumber, expiryDate, cvv].forEach(field => {
            field.disabled = isValidPromo;
            field.style.backgroundColor = isValidPromo ? "#e9ecef" : "";
            field.value = isValidPromo ? "" : field.value;
        });

        nextButton.disabled = !isValidPromo;
    }

    promoCodeInput.addEventListener("input", function () {
        if (!promoCodeInput.value.trim()) {
            [cardNumber, expiryDate, cvv].forEach(field => {
                field.disabled = false;
                field.style.backgroundColor = "";
            });
            nextButton.disabled = true;
            promoMessage.innerText = "";
        }
    });

    document.querySelector(".promo-code button")?.addEventListener("click", applyPromoCode);

    /* =======================================================
    SECTION 10: EmailJS - Send Registration Confirmation
    ======================================================= */
    function sendConfirmationEmail(name, email, selectedPlan) {
        console.log("📩 Sending email via EmailJS...", { name, email, selectedPlan });

        emailjs.send("service_9fhnu4c", "template_0h7vmqw", {
            name: name,
            email: email,
            selected_plan: selectedPlan
        }).then(response => console.log("✅ Email sent!", response))
            .catch(error => console.error("❌ Email failed:", error));
    }

    registerForm.addEventListener("submit", function (event) {
        event.preventDefault();
        sendConfirmationEmail(document.querySelector('input[name="first_name"]').value, document.querySelector('input[name="email"]').value, selectedPlanInput.value);
        setTimeout(() => this.submit(), 1500);
    });
});
