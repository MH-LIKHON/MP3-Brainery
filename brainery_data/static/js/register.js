document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded! Waiting for user interaction...");

    // ✅ Ensure EmailJS script is loaded before initializing
    if (!window.emailjs) {
        console.error("❌ EmailJS script not loaded. Make sure to include the script in your HTML.");
        return;
    }

    // ✅ Initialize EmailJS
    try {
        emailjs.init("W2YSRyqhhCt5N8kVj");
        console.log("✅ EmailJS Initialized Successfully!");
    } catch (error) {
        console.error("❌ EmailJS Initialization Failed!", error);
        alert("⚠ EmailJS failed to initialize. Check your API key.");
    }

    /* =======================================================
    SECTION 1: Element Selection
    ======================================================= */

    // ✅ Get all required elements safely
    let packages = document.querySelectorAll(".package");
    let selectedPlanInput = document.getElementById("selected_plan");  // Hidden input field for the selected plan
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

    if (!registerForm) {
        console.error("❌ Registration form not found! Ensure the correct ID is used.");
        return;  // Stop script execution if form is missing
    } else {
        console.log("✅ Registration form detected.");
    }

    // ✅ Ensure Submit Button exists before adding event listener
    let submitButton = document.querySelector("#password-info .submit-btn");

    if (submitButton) {
        submitButton.addEventListener("click", function () {
            console.log("✅ Submit button clicked!");
        });
    } else {
        console.error("❌ Submit button not found! Ensure correct selector.");
    }

    // ✅ Ensure Registration Form exists before using it
    if (!registerForm) {
        console.error("❌ Registration form not found! Ensure the correct ID is used.");
    } else {
        console.log("✅ Registration form detected.");
    }

    // ✅ Ensure Personal Info section exists before modifying it
    if (!personalInfo) {
        console.error("❌ Personal Info section not found!");
    }

    // ✅ Ensure Payment Form exists before adding event listener
    if (paymentForm) {
        console.log("✅ Payment form detected.");
    } else {
        console.error("❌ Payment form not found! Check the form ID.");
    }

    // ✅ Ensure Next Button exists before using it
    if (!nextButton) {
        console.error("❌ Next button not found! Ensure the correct selector.");
    }

    // ✅ Ensure required fields exist before using them
    if (!cardNumber) console.error("❌ Card number input not found!");
    if (!expiryDate) console.error("❌ Expiry date input not found!");
    if (!cvv) console.error("❌ CVV input not found!");
    if (!promoCodeInput) console.error("❌ Promo code input not found!");
    if (!promoMessage) console.error("❌ Promo message element not found!");
    if (!errorMessageBox) console.error("❌ Error message box not found!");

    console.log("✅ Element selection completed!");

    /* =======================================================
    SECTION 2: Reset Form on Page Reload
    ======================================================= */
    window.addEventListener("load", function () {
        const urlParams = new URLSearchParams(window.location.search);
        if (!urlParams.has("success")) {
            console.log("Resetting form on page reload...");
            if (registerForm) registerForm.reset();
        }
    });

    /* =======================================================
    SECTION 3: Hide Registration Form After Successful Submission & Auto-Clear Messages
    ======================================================= */
    if (successMessage && successMessage.classList.contains("show")) {
        console.log("Registration successful! Hiding the form...");
        if (registerForm) {
            registerForm.style.display = "none";  // ✅ Only hide if form exists
        } else {
            console.warn("⚠ Registration form not found. Skipping hide.");
        }
    }

    setTimeout(() => {
        let registerForm = document.querySelector("form#registration-form");

        if (!registerForm) {
            console.error("❌ Registration form still not found! Ensure the correct ID is used.");
            return;
        } else {
            console.log("✅ Registration form detected.");
        }
    }, 500);

    /* =======================================================
    SECTION 4: Package Selection Handling
    ======================================================= */
    packages.forEach(package => {
        package.addEventListener("click", function () {
            console.log("✅ Package Clicked:", this.dataset.name);

            // Remove 'selected' class from all packages
            packages.forEach(p => p.classList.remove("selected"));

            // Highlight the selected package
            this.classList.add("selected");

            // Ensure selectedPlanInput exists before setting value
            if (selectedPlanInput) {
                if (selectedPlanInput) {
                    selectedPlanInput.value = `${this.dataset.name} - £${this.dataset.price}`;
                    console.log("✅ Selected Plan Updated in Hidden Input:", selectedPlanInput.value);
                } else {
                    console.error("❌ Error: selectedPlanInput element not found!");
                }
                console.log("✅ Selected Plan Updated:", selectedPlanInput.value);
            } else {
                console.error("❌ Error: selectedPlanInput element not found!");
            }

            // Ensure personalInfo exists before displaying
            if (personalInfo) {
                personalInfo.style.display = "block";
                setTimeout(() => { personalInfo.style.opacity = 1; }, 100);
                personalInfo.scrollIntoView({ behavior: "smooth" });
            } else {
                console.error("❌ personalInfo element not found!");
            }
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

        // ✅ Ensure only required fields are checked at each step
        if (currentId === "personal-info" || currentId === "payment-info") {
            if (isPromoApplied && currentId === "payment-info") {
                emptyFields = emptyFields.filter(input => !["card_number", "expiry_date", "cvv"].includes(input.name));
            }

            if (emptyFields.length > 0) {
                emptyFields.forEach(input => showError(input, "This field is required."));
                emptyFields[0].focus();
                return;
            }
        }

        console.log(`🚀 Moving from ${currentId} to ${nextId}`);
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
    SECTION 10: Email Availability Check (AJAX)
    ======================================================= */
    const emailInput = document.querySelector('input[name="email"]');

    // Identify the Next button within the "Personal Info" section only
    const personalInfoSection = document.getElementById("personal-info");
    const nextButtonPersonalInfo = personalInfoSection ? personalInfoSection.querySelector(".next-btn") : null;

    if (!emailInput || !registerForm || !nextButtonPersonalInfo) {
        console.error("❌ Missing email input, registration form, or Next button in Personal Info section.");
    } else {
        emailInput.addEventListener("input", function () {
            let emailValue = emailInput.value.trim();

            // ✅ Remove previous error messages before checking
            let existingError = emailInput.parentElement.querySelector(".error-message");
            if (existingError) existingError.remove();

            if (emailValue === "") {
                emailInput.style.border = "";
                nextButtonPersonalInfo.disabled = true; // ✅ Disable only the Personal Info Next button when empty
                return;
            }

            console.log(`📧 Checking email: ${emailValue}`);

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

                    // ✅ Remove old error messages before adding a new one
                    let oldError = emailInput.parentElement.querySelector(".error-message");
                    if (oldError) oldError.remove();

                    let errorSpan = document.createElement("span");
                    errorSpan.classList.add("error-message");
                    errorSpan.style.color = "red";
                    errorSpan.innerHTML = `❌ This email is already registered. Try logging in instead.`;

                    if (data.exists) {
                        emailInput.style.border = "2px solid red";
                        emailInput.parentElement.appendChild(errorSpan);

                        // ✅ Disable only the "Next" button in the Personal Info section
                        nextButtonPersonalInfo.disabled = true;
                        registerForm.querySelector("button[type='submit']").disabled = true;
                    } else {
                        emailInput.style.border = "";
                        nextButtonPersonalInfo.disabled = false; // ✅ Enable Personal Info Next button when email is valid
                        registerForm.querySelector("button[type='submit']").disabled = false;
                    }
                })
                .catch(error => {
                    console.error("❌ Error checking email:", error);

                    let errorSpan = document.createElement("span");
                    errorSpan.classList.add("error-message");
                    errorSpan.style.color = "orange";
                    errorSpan.innerHTML = "⚠ Unable to check email. Please try again.";

                    emailInput.style.border = "2px solid orange";
                    emailInput.parentElement.appendChild(errorSpan);

                    nextButtonPersonalInfo.disabled = true; // ✅ Keep Next button disabled in case of an error
                });
        });
    }

    /* =======================================================
    SECTION 11: EmailJS - Send Registration Confirmation
    ======================================================= */

    let emailSent = false; // ✅ Prevents duplicate emails

    function sendConfirmationEmail(name, email, selectedPlan) {
        return new Promise((resolve, reject) => {
            console.log("📨 Preparing to send confirmation email...");

            if (!emailjs || !emailjs.send) {
                console.error("❌ EmailJS is not loaded. Aborting email send.");
                reject(new Error("EmailJS is not available."));
                return;
            }

            if (!email || email.trim() === "") {
                console.error("❌ No recipient email provided! Aborting EmailJS call.");
                reject(new Error("Missing email field."));
                return;
            }

            let emailParams = {
                name: name || "User",
                from_email: email,
                selected_plan: selectedPlan || "No Plan Selected"
            };

            console.log("📧 Sending email with parameters:", emailParams);

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
       SECTION 12: Handle Registration Form Submission
    ======================================================= */
    registerForm.addEventListener("submit", function (event) {
        event.preventDefault(); // ✅ Prevent default form submission

        if (this.dataset.submitted === "true") {
            console.warn("⚠ Form already submitted. Preventing duplicate submission.");
            return;
        }
        this.dataset.submitted = "true"; // ✅ Mark form as submitted

        console.log("🚀 Proceeding with registration...");

        const formData = new FormData(registerForm);
        const formObject = Object.fromEntries(formData);

        console.log("📌 Form Data to be sent:", formObject);

        fetch("/register/register", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams(formData).toString(),
        })
            .then(response => response.json())
            .then(jsonData => {
                if (jsonData.success) {
                    console.log("✅ User successfully registered in MongoDB!");

                    // Call EmailJS function **before redirecting**
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
                    this.dataset.submitted = "false"; // ✅ Reset submission flag if error
                }
            })
            .catch(error => {
                console.error("❌ Unexpected error:", error);
                alert("⚠ Unexpected error. Please try again.");
                this.dataset.submitted = "false"; // ✅ Reset submission flag if error
            });
    });

});