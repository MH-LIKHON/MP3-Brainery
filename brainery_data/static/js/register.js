document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded! Waiting for user interaction...");

    /* =======================================================
    SECTION 1: Element Selection
    ======================================================= */
    // Selecting all necessary DOM elements for later manipulation
    let packages = document.querySelectorAll(".package");  // Package selection elements
    let selectedPlanInput = document.getElementById("selected_plan");  // Hidden input field for the selected plan
    let personalInfo = document.getElementById("personal-info");  // Personal information form
    let paymentForm = document.getElementById("payment-info");  // Payment information form
    let passwordInfo = document.getElementById("password-info");  // Password section form
    let submitButton = document.querySelector("#password-info .submit-btn");  // Submit button in the password section
    let successMessage = document.getElementById("success-message");  // Success message element
    let registerForm = document.getElementById("register-form");  // The registration form
    let nextButton = document.querySelector("#payment-info .next-btn");  // Next button in the payment section
    let errorMessageBox = document.getElementById("error-message-box");  // Box to display error messages

    // Form fields related to payment information
    let cardNumber = document.querySelector('input[name="card_number"]');
    let expiryDate = document.querySelector('input[name="expiry_date"]');
    let cvv = document.querySelector('input[name="cvv"]');
    let promoCodeInput = document.getElementById("promo-code");  // Promo code input field
    let promoMessage = document.getElementById("promo-message");  // Promo code message display

    /* =======================================================
    SECTION 2: Reset Form on Page Reload
    ======================================================= */
    // Ensures the form is reset when the page is reloaded
    window.addEventListener("load", function () {
        console.log("Resetting form on page reload...");
        document.getElementById("registration-form")?.reset();  // Reset the registration form
    });

    /* =======================================================
    SECTION 3: Hide Registration Form After Successful Submission
    ======================================================= */
    // If the registration is successful, hide the registration form
    if (successMessage && successMessage.classList.contains("show")) {
        console.log("Registration successful! Hiding the form...");
        registerForm.style.display = "none";  // Hide the form after successful registration
    }

    /* =======================================================
    SECTION 4: Package Selection Handling
    ======================================================= */
    // Adding event listeners to each package option
    packages.forEach(package => {
        package.addEventListener("click", function () {
            console.log("Package Selected:", this.dataset.name);

            // Remove "selected" class from all other packages
            packages.forEach(p => p.classList.remove("selected"));

            // Add "selected" class to the clicked package
            this.classList.add("selected");

            // Set the value of the hidden input to the selected plan details
            selectedPlanInput.value = `${this.dataset.name} - £${this.dataset.price}`;
            console.log("Selected Plan:", selectedPlanInput.value);

            // Show the personal info section
            personalInfo.style.display = "block";
            setTimeout(() => { personalInfo.style.opacity = 1; }, 100);
            personalInfo.scrollIntoView({ behavior: "smooth" });
        });
    });

    /* =======================================================
    SECTION 5: Field Validation & Error Handling
    ======================================================= */
    // Function to show an error message next to the invalid input field
    function showError(input, message) {
        let errorSpan = input.parentElement.querySelector(".error-message");
        if (!errorSpan) {
            // Create a new error message span if it doesn't exist
            errorSpan = document.createElement("span");
            errorSpan.classList.add("error-message");
            errorSpan.style.color = "red";  // Red color for error messages
            input.parentElement.appendChild(errorSpan);
        }
        errorSpan.innerText = message;  // Set the error message
        input.style.border = "2px solid red";  // Set the input field border to red
    }

    // Function to clear all errors from input fields
    function clearErrors() {
        document.querySelectorAll(".error-message").forEach(el => el.remove());  // Remove all error messages
        document.querySelectorAll("input").forEach(el => el.style.border = "");  // Reset border color for inputs
    }

    /* =======================================================
    SECTION 6: Step Navigation & Validation (Next Button)
    ======================================================= */
    // Function to handle the transition between different steps (sections)
    function nextStep(currentId, nextId) {
        let currentSection = document.getElementById(currentId);  // Current section ID (e.g. "personal-info")
        let nextSection = document.getElementById(nextId);  // Next section ID (e.g. "payment-info")

        if (!currentSection || !nextSection) {
            console.error("ERROR: Missing section IDs", currentId, nextId);
            return;
        }

        clearErrors();  // Clear any existing errors before proceeding

        // Get all required input fields in the current section
        let requiredFields = currentSection.querySelectorAll("input[required]");
        let emptyFields = Array.from(requiredFields).filter(input => input.value.trim() === "");

        let isPromoApplied = promoCodeInput.value.trim() === "CI25MP3";  // Check if promo code is applied

        // Skip validation of card fields if promo code is applied
        if (isPromoApplied && currentId === "payment-info") {
            emptyFields = emptyFields.filter(input => !["card_number", "expiry_date", "cvv"].includes(input.name));
        }

        // If there are any empty required fields, show error messages and stop
        if (emptyFields.length > 0) {
            emptyFields.forEach(input => showError(input, "This field is required."));
            emptyFields[0].focus();  // Focus on the first empty field
            return;
        }

        console.log(`Transitioning from ${currentId} to ${nextId}`);

        // Hide current section with a fade-out effect
        currentSection.style.opacity = 0;
        setTimeout(() => {
            currentSection.style.display = "none";  // Hide the current section
            nextSection.style.display = "block";  // Show the next section
            setTimeout(() => { nextSection.style.opacity = 1; }, 100);  // Fade-in the next section
            nextSection.scrollIntoView({ behavior: "smooth" });  // Smoothly scroll to the next section
        }, 200);
    }

    window.nextStep = nextStep;  // Expose the nextStep function globally

    /* =======================================================
    SECTION 7: Expiry Date Validation (March 2025 & Onwards)
    ======================================================= */
    // Function to validate the expiry date input (must be from March 2025 onwards)
    function validateExpiryDate(expiryDate) {
        let [month, year] = expiryDate.split("/").map(Number);  // Extract month and year from input
        return !(isNaN(month) || isNaN(year) || month < 1 || month > 12 || year < 25 || (year === 25 && month < 3));  // Validate expiry date
    }

    /* =======================================================
    SECTION 8: Payment Form Submission & Validation
    ======================================================= */
    // Handle the payment form submission and validate the payment details
    paymentForm.addEventListener("submit", function (event) {
        event.preventDefault();
        console.log("Processing Payment...");

        clearErrors();  // Clear any previous error messages

        let isPromoApplied = promoCodeInput.value.trim() === "CI25MP3";  // Check if promo code is applied

        if (!isPromoApplied) {
            // Validate payment details if promo code is not applied
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
        nextStep("payment-info", "password-info");  // Move to the next step (password section)
    });

    /* =======================================================
    SECTION 9: Promo Code Handling (Fully Fixed)
    ======================================================= */
    // Function to handle promo code input and apply its benefits
    function applyPromoCode() {
        let promoCodeValue = promoCodeInput.value.trim();  // Get the promo code value
        let isValidPromo = promoCodeValue === "CI25MP3";  // Check if the promo code is valid

        if (isValidPromo) {
            promoMessage.innerText = "Promo applied! No payment required.";  // Display success message
            promoMessage.style.color = "green";  // Set the message color to green

            // Disable card input fields, clear them, and allow Next button
            [cardNumber, expiryDate, cvv].forEach(field => {
                field.disabled = true;
                field.style.backgroundColor = "#e9ecef";
                field.value = "";  // Clear the field values
                field.removeAttribute("required");
            });

            nextButton.disabled = false;  // Enable the Next button
        } else {
            promoMessage.innerText = "Invalid promo code.";  // Display error message
            promoMessage.style.color = "red";  // Set the message color to red

            // Re-enable card input fields and set them as required again
            [cardNumber, expiryDate, cvv].forEach(field => {
                field.disabled = false;
                field.style.backgroundColor = "";
                field.setAttribute("required", "true");
            });

            nextButton.disabled = true;  // Disable the Next button
        }
    }

    // Event listener for promo code input to apply promo code dynamically
    promoCodeInput.addEventListener("input", function () {
        if (!promoCodeInput.value.trim()) {
            // Restore input fields when promo code is removed
            [cardNumber, expiryDate, cvv].forEach(field => {
                field.disabled = false;
                field.style.backgroundColor = "";
                field.setAttribute("required", "true");
            });

            nextButton.disabled = true;  // Disable the Next button
            promoMessage.innerText = "";  // Clear promo message
        }
    });

    // Event listener for the promo code apply button
    document.querySelector(".promo-code button")?.addEventListener("click", applyPromoCode);  // Apply promo code
});
