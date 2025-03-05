document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded! Waiting for user interaction...");

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
    let registerForm = document.getElementById("register-form");
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
        document.getElementById("registration-form")?.reset();
    });

    /* =======================================================
    SECTION 3: Hide Registration Form After Successful Submission
    ======================================================= */
    if (successMessage && successMessage.classList.contains("show")) {
        console.log("Registration successful! Hiding the form...");
        registerForm.style.display = "none";
    }

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

        //Skip validation of card fields if promo is applied
        if (isPromoApplied && currentId === "payment-info") {
            emptyFields = emptyFields.filter(input => !["card_number", "expiry_date", "cvv"].includes(input.name));
        }

        if (emptyFields.length > 0) {
            emptyFields.forEach(input => showError(input, "This field is required."));
            emptyFields[0].focus();
            return;
        }

        console.log(`Transitioning from ${currentId} to ${nextId}`);

        // Hide current section
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
    SECTION 7: Expiry Date Validation (March 2025 & Onwards)
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
        console.log("Processing Payment...");

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
    SECTION 9: Promo Code Handling (Fully Fixed)
    ======================================================= */
    function applyPromoCode() {
        let promoCodeValue = promoCodeInput.value.trim();
        let isValidPromo = promoCodeValue === "CI25MP3";

        if (isValidPromo) {
            promoMessage.innerText = "Promo applied! No payment required.";
            promoMessage.style.color = "green";

            // Disable card input fields, clear them, and allow Next button
            [cardNumber, expiryDate, cvv].forEach(field => {
                field.disabled = true;
                field.style.backgroundColor = "#e9ecef";
                field.value = "";
                field.removeAttribute("required");
            });

            nextButton.disabled = false;
        } else {
            promoMessage.innerText = "Invalid promo code.";
            promoMessage.style.color = "red";

            // Re-enable card input fields and set them as required again
            [cardNumber, expiryDate, cvv].forEach(field => {
                field.disabled = false;
                field.style.backgroundColor = "";
                field.setAttribute("required", "true");
            });

            nextButton.disabled = true;
        }
    }

    promoCodeInput.addEventListener("input", function () {
        if (!promoCodeInput.value.trim()) {
            [cardNumber, expiryDate, cvv].forEach(field => {
                field.disabled = false;
                field.style.backgroundColor = "";
                field.setAttribute("required", "true");
            });

            nextButton.disabled = true;
            promoMessage.innerText = "";
        }
    });

    document.querySelector(".promo-code button")?.addEventListener("click", applyPromoCode);
});