document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded! Waiting for user interaction...");

    /* =======================================================
    SECTION 1: Initialize EmailJS
    ======================================================= */

    // Initialize EmailJS
    if (!window.emailjs) {
        console.error("❌ EmailJS script not loaded. Make sure to include the script in your HTML.");
        return;
    }

    // Attempt to initialize EmailJS with the provided API key
    try {
        emailjs.init("W2YSRyqhhCt5N8kVj");
        console.log("✅ EmailJS Initialized Successfully!");
    } catch (error) {
        console.error("❌ EmailJS Initialization Failed!", error);
        alert("⚠ EmailJS failed to initialize. Check your API key.");
    }

    /* =======================================================
    SECTION 2: Element Selection
    ======================================================= */

    // Get all required elements safely
    let packages = document.querySelectorAll(".package");
    let selectedPlanInput = document.getElementById("selected_plan");
    let personalInfo = document.getElementById("personal-info");
    let paymentForm = document.getElementById("payment-info");
    let passwordInfo = document.getElementById("password-info");
    let successMessage = document.getElementById("success-message");
    let nextButton = document.querySelector("#payment-info .next-btn");
    let errorMessageBox = document.getElementById("error-message-box");
    let cardNumber = document.querySelector('input[name="card_number"]');
    let expiryDate = document.querySelector('input[name="expiry_date"]');
    let cvv = document.querySelector('input[name="cvv"]');
    let promoCodeInput = document.getElementById("promo-code");
    let promoMessage = document.getElementById("promo-message");

    let registerForm = document.querySelector("form#registration-form");

    // Ensure the registration form exists before proceeding
    if (!registerForm) {
        console.error("❌ Registration form not found! Ensure the correct ID is used.");
        return;  // Stop script execution if the form is missing
    } else {
        console.log("✅ Registration form detected.");
    }

    // Ensure the submit button exists before adding an event listener
    let submitButton = document.querySelector("#password-info .submit-btn");

    if (submitButton) {
        submitButton.addEventListener("click", function () {
            console.log("✅ Submit button clicked!");
        });
    } else {
        console.error("❌ Submit button not found! Ensure correct selector.");
    }

    // Ensure the registration form exists before using it
    if (!registerForm) {
        console.error("❌ Registration form not found! Ensure the correct ID is used.");
    } else {
        console.log("✅ Registration form detected.");
    }

    // Ensure the personal info section exists before modifying it
    if (!personalInfo) {
        console.error("❌ Personal Info section not found!");
    }

    // Ensure the payment form exists before using it
    if (paymentForm) {
        console.log("✅ Payment form detected.");
    } else {
        console.error("❌ Payment form not found! Check the form ID.");
    }

    // Ensure the next button exists before using it
    if (!nextButton) {
        console.error("❌ Next button not found! Ensure the correct selector.");
    }

    // Ensure required fields exist before using them
    if (!cardNumber) console.error("❌ Card number input not found!");
    if (!expiryDate) console.error("❌ Expiry date input not found!");
    if (!cvv) console.error("❌ CVV input not found!");
    if (!promoCodeInput) console.error("❌ Promo code input not found!");
    if (!promoMessage) console.error("❌ Promo message element not found!");
    if (!errorMessageBox) console.error("❌ Error message box not found!");

    console.log("✅ Element selection completed!");

    /* =======================================================
    SECTION 3: Reset Form on Page Reload
    ======================================================= */

    // Reset the registration form when the page reloads unless a success flag is present in the URL
    window.addEventListener("load", function () {
        const urlParams = new URLSearchParams(window.location.search);

        if (!urlParams.has("success")) {
            console.log("Resetting form on page reload...");
            if (registerForm) registerForm.reset();
        }
    });

    /* =======================================================
    SECTION 4: Hide Registration Form After Successful Submission & Auto-Clear Messages
    ======================================================= */

    // Check if the success message is visible and hide the form if submission was successful
    if (successMessage && successMessage.classList.contains("show")) {
        console.log("Registration successful! Hiding the form...");
        if (registerForm) {
            registerForm.style.display = "none";
        } else {
            console.warn("⚠ Registration form not found. Skipping hide.");
        }
    }

    // Wait 500ms before verifying if the registration form is still accessible
    setTimeout(() => {
        let registerForm = document.querySelector("form#registration-form");

        // Ensure the registration form exists before proceeding
        if (!registerForm) {
            console.error("❌ Registration form still not found! Ensure the correct ID is used.");
            return;
        } else {
            console.log("✅ Registration form detected.");
        }
    }, 500);

    /* =======================================================
    SECTION 5: Package Selection Handling
    ======================================================= */

    // Add click event listeners to each package option
    packages.forEach(package => {
        package.addEventListener("click", function () {
            console.log("✅ Package Clicked:", this.dataset.name);

            // Remove 'selected' class from all packages to ensure only one is highlighted
            packages.forEach(p => p.classList.remove("selected"));

            // Highlight the clicked package
            this.classList.add("selected");

            // Ensure selectedPlanInput exists before updating its value
            if (selectedPlanInput) {
                selectedPlanInput.value = `${this.dataset.name} - £${this.dataset.price}`;
                console.log("✅ Selected Plan Updated in Hidden Input:", selectedPlanInput.value);
            } else {
                console.error("❌ Error: selectedPlanInput element not found!");
            }

            // Ensure personalInfo section exists before making it visible
            if (personalInfo) {
                personalInfo.style.display = "block";

                // Apply a slight delay before adjusting opacity for smooth transition
                setTimeout(() => { personalInfo.style.opacity = 1; }, 100);

                // Scroll the personalInfo section into view smoothly
                personalInfo.scrollIntoView({ behavior: "smooth" });
            } else {
                console.error("❌ personalInfo element not found!");
            }
        });
    });

    /* =======================================================
    SECTION 6: Field Validation & Error Handling
    ======================================================= */

    // Display an error message for an input field and highlight it in red
    function showError(input, message) {
        let errorSpan = input.parentElement.querySelector(".error-message");

        // Create an error message element if it doesn't exist
        if (!errorSpan) {
            errorSpan = document.createElement("span");
            errorSpan.classList.add("error-message");
            errorSpan.style.color = "red";
            input.parentElement.appendChild(errorSpan);
        }

        // Set the error message and apply red border to indicate an issue
        errorSpan.innerText = message;
        input.style.border = "2px solid red";
    }

    // Remove all error messages and reset input field borders
    function clearErrors() {
        document.querySelectorAll(".error-message").forEach(el => el.remove());
        document.querySelectorAll("input").forEach(el => el.style.border = "");
    }

    /* =======================================================
SECTION 7: Step Navigation & Validation (Next Button)
======================================================= */

    // Navigate to the next step in the registration process with validation
    function nextStep(currentId, nextId) {
        let currentSection = document.getElementById(currentId);
        let nextSection = document.getElementById(nextId);

        // Ensure both current and next sections exist before proceeding
        if (!currentSection || !nextSection) {
            console.error("ERROR: Missing section IDs", currentId, nextId);
            return;
        }

        clearErrors();

        // Get all required fields in the current section
        let requiredFields = currentSection.querySelectorAll("input[required]");
        let emptyFields = Array.from(requiredFields).filter(input => input.value.trim() === "");

        // Check if a promo code is applied
        let isPromoApplied = promoCodeInput.value.trim() === "CI25MP3";

        // Validate required fields for each step
        if (currentId === "personal-info" || currentId === "payment-info") {
            if (isPromoApplied && currentId === "payment-info") {
                // Exclude payment fields from validation if promo is applied
                emptyFields = emptyFields.filter(input => !["card_number", "expiry_date", "cvv"].includes(input.name));
            }

            // Show error messages for empty fields and prevent navigation
            if (emptyFields.length > 0) {
                emptyFields.forEach(input => showError(input, "This field is required."));
                emptyFields[0].focus();
                return;
            }
        }

        console.log(`🚀 Moving from ${currentId} to ${nextId}`);

        // Hide current section and transition to the next step
        currentSection.style.opacity = 0;
        setTimeout(() => {
            currentSection.style.display = "none";
            nextSection.style.display = "block";
            setTimeout(() => { nextSection.style.opacity = 1; }, 100);
            nextSection.scrollIntoView({ behavior: "smooth" });
        }, 200);
    }

    // Make nextStep function globally accessible
    window.nextStep = nextStep;

    /* =======================================================
    SECTION 8: Expiry Date Validation
    ======================================================= */

    // Validate if the entered expiry date is in the correct format and not expired
    function validateExpiryDate(expiryDate) {
        let [month, year] = expiryDate.split("/").map(Number);

        // Check if the month and year are valid
        return !(isNaN(month) || isNaN(year) || month < 1 || month > 12 || year < 25 || (year === 25 && month < 3));
    }

    /* =======================================================
    SECTION 9: Payment Form Submission & Validation
    ======================================================= */

    // Handle payment form submission and validate required fields before proceeding
    paymentForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent form from submitting normally
        clearErrors(); // Clear previous error messages

        let isPromoApplied = promoCodeInput.value.trim() === "CI25MP3";

        // Validate payment fields only if a promo code is not applied
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

        // Proceed to the password setup section
        nextStep("payment-info", "password-info");
    });

    /* =======================================================
    SECTION 10: Promo Code Handling
    ======================================================= */

    // Apply the promo code and update the payment fields accordingly
    function applyPromoCode() {
        let promoCodeValue = promoCodeInput.value.trim();
        let isValidPromo = promoCodeValue === "CI25MP3";

        // Display appropriate message based on promo code validity
        promoMessage.innerText = isValidPromo ? "Promo applied! No payment required." : "Invalid promo code.";
        promoMessage.style.color = isValidPromo ? "green" : "red";

        // Disable payment fields if promo is valid, otherwise keep them enabled
        [cardNumber, expiryDate, cvv].forEach(field => {
            field.disabled = isValidPromo;
            field.style.backgroundColor = isValidPromo ? "#e9ecef" : "";
            field.value = isValidPromo ? "" : field.value;
        });

        // Enable the next button only if a valid promo is applied
        nextButton.disabled = !isValidPromo;
    }

    // Reset payment fields when promo code input is cleared
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

    // Attach event listener to the promo code apply button
    document.querySelector(".promo-code button")?.addEventListener("click", applyPromoCode);

    /* =======================================================
    SECTION 11: Email Availability Check (AJAX)
    ======================================================= */

    // Select the email input field
    const emailInput = document.querySelector('input[name="email"]');

    // Identify the Next button within the "Personal Info" section only
    const personalInfoSection = document.getElementById("personal-info");
    const nextButtonPersonalInfo = personalInfoSection ? personalInfoSection.querySelector(".next-btn") : null;

    // Ensure required elements exist before proceeding
    if (!emailInput || !registerForm || !nextButtonPersonalInfo) {
        console.error("❌ Missing email input, registration form, or Next button in Personal Info section.");
    } else {
        // Add event listener to check email availability on input change
        emailInput.addEventListener("input", function () {
            let emailValue = emailInput.value.trim();

            // Remove any previous error messages before checking
            let existingError = emailInput.parentElement.querySelector(".error-message");
            if (existingError) existingError.remove();

            // If email field is empty, reset styles and disable Next button
            if (emailValue === "") {
                emailInput.style.border = "";
                nextButtonPersonalInfo.disabled = true;
                return;
            }

            console.log(`📧 Checking email: ${emailValue}`);

            // Send AJAX request to check if email is already registered
            fetch("/register/check_email", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: emailValue })
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Server error.");
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("✅ Server Response:", data);

                    // Remove old error messages before adding a new one
                    let oldError = emailInput.parentElement.querySelector(".error-message");
                    if (oldError) oldError.remove();

                    // Create and display error message if email is already registered
                    let errorSpan = document.createElement("span");
                    errorSpan.classList.add("error-message");
                    errorSpan.style.color = "red";
                    errorSpan.innerHTML = `❌ This email is already registered. Try logging in instead.`;

                    if (data.exists) {
                        emailInput.style.border = "2px solid red";
                        emailInput.parentElement.appendChild(errorSpan);

                        // Disable only the "Next" button in the Personal Info section
                        nextButtonPersonalInfo.disabled = true;
                        registerForm.querySelector("button[type='submit']").disabled = true;
                    } else {
                        // Reset styles and enable the Next button if email is available
                        emailInput.style.border = "";
                        nextButtonPersonalInfo.disabled = false;
                        registerForm.querySelector("button[type='submit']").disabled = false;
                    }
                })
                .catch(error => {
                    console.error("❌ Error checking email:", error);

                    // Show an error message if the email check fails
                    let errorSpan = document.createElement("span");
                    errorSpan.classList.add("error-message");
                    errorSpan.style.color = "orange";
                    errorSpan.innerHTML = "⚠ Unable to check email. Please try again.";

                    emailInput.style.border = "2px solid orange";
                    emailInput.parentElement.appendChild(errorSpan);

                    // Keep Next button disabled in case of an error
                    nextButtonPersonalInfo.disabled = true;
                });
        });
    }

    /* =======================================================
    SECTION 12: EmailJS - Send Registration Confirmation
    ======================================================= */

    let emailSent = false; // Prevents duplicate emails from being sent

    // Send a confirmation email to the user after successful registration
    function sendConfirmationEmail(name, email, selectedPlan) {
        return new Promise((resolve, reject) => {
            console.log("📨 Preparing to send confirmation email...");

            // Ensure EmailJS is loaded before proceeding
            if (!emailjs || !emailjs.send) {
                console.error("❌ EmailJS is not loaded. Aborting email send.");
                reject(new Error("EmailJS is not available."));
                return;
            }

            // Ensure a recipient email is provided
            if (!email || email.trim() === "") {
                console.error("❌ No recipient email provided! Aborting EmailJS call.");
                reject(new Error("Missing email field."));
                return;
            }

            // Extract first and last name from the form (Modify based on actual form structure)
            let firstName = document.querySelector('input[name="first_name"]')?.value || "";
            let lastName = document.querySelector('input[name="last_name"]')?.value || "";
            let fullName = `${firstName} ${lastName}`.trim();

            // Set up parameters for the email template
            let emailParams = {
                first_name: firstName,
                to_name: fullName,
                from_email: email,
                selected_plan: selectedPlan || "No Plan Selected"
            };

            console.log("📧 Sending email with parameters:", emailParams);

            // Send email using EmailJS service and template
            emailjs.send("service_9fhnu4c", "template_0h7vmqw", emailParams)
                .then(response => {
                    console.log("✅ Email successfully sent!", response);
                    resolve(response);
                })
                .catch(error => {
                    console.error("❌ Email sending failed!", error);
                    console.error("🔎 Full Error Response:", error);
                    console.error("📨 Failed Email Parameters:", JSON.stringify(emailParams));
                    alert("⚠ Email sending failed. Check console for details.");
                    reject(error);
                });

        });
    }

    /* =======================================================
    SECTION 13: Handle Registration Form Submission
    ======================================================= */

    // Listen for the form submission event
    registerForm.addEventListener("submit", function (event) {
        event.preventDefault();

        // Prevent duplicate submissions by checking submission flag
        if (this.dataset.submitted === "true") {
            console.warn("⚠ Form already submitted. Preventing duplicate submission.");
            return;
        }

        // Mark the form as submitted to prevent multiple submissions
        this.dataset.submitted = "true";

        console.log("🚀 Proceeding with registration...");

        // Collect form data and convert it into an object
        const formData = new FormData(registerForm);
        const formObject = Object.fromEntries(formData);

        console.log("📌 Form Data to be sent:", formObject);

        // Send form data to the backend for registration
        fetch("/register/register", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams(formData).toString(),
        })
            .then(response => response.json())
            .then(jsonData => {
                if (jsonData.success) {
                    console.log("✅ User successfully registered in MongoDB!");

                    // Send confirmation email before redirecting to the success page
                    sendConfirmationEmail(formObject.first_name, formObject.email, formObject.selected_plan)
                        .then(() => {
                            window.location.href = "/register/register?success=true";
                        })
                        .catch(error => {
                            console.error("❌ Email sending failed:", error);
                            alert("⚠ Registration completed but confirmation email failed.");
                            window.location.href = "/register/register?success=true";
                        });

                } else {
                    console.error("❌ Registration failed:", jsonData.message);
                    alert(`⚠ Registration failed: ${jsonData.message}`);

                    // Reset submission flag in case of an error
                    this.dataset.submitted = "false";
                }
            })
            .catch(error => {
                console.error("❌ Unexpected error:", error);
                alert("⚠ Unexpected error. Please try again.");

                // Reset submission flag if an error occurs
                this.dataset.submitted = "false";
            });
    });

});