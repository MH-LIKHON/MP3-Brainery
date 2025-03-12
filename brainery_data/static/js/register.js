document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded! Waiting for user interaction...");

    // ✅ Initialize EmailJS
    if (typeof emailjs !== "undefined" && emailjs.init) {
        try {
            emailjs.init("W2YSRyqhhCt5N8kVj");
            console.log("✅ EmailJS Initialized Successfully!");
        } catch (error) {
            console.error("❌ EmailJS Initialization Failed!", error);
            alert("⚠ EmailJS failed to initialize. Check your API key.");
        }
    } else {
        console.error("❌ EmailJS is not loaded or undefined!");
    }

    /* =======================================================
    SECTION 1: Element Selection
    ======================================================= */
    let packages = document.querySelectorAll(".package");
    let selectedPlanInput = document.getElementById("selected_plan");  // Hidden input field for the selected plan
    let personalInfo = document.getElementById("personal-info");
    let paymentForm = document.getElementById("payment-info");
    let passwordInfo = document.getElementById("password-info");
    let submitButton = document.querySelector("#password-info .submit-btn");
    let successMessage = document.getElementById("success-message");

    // Get the registration form correctly
    let registerForm = document.getElementById("registration-form");

    if (!registerForm) {
        console.error("❌ Registration form not found! Ensure the correct ID is used.");
    } else {
        console.log("✅ Registration form detected.");
    }

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
        if (!email || email.trim() === "") {
            console.error("❌ No recipient email provided! Aborting EmailJS call.");
            return Promise.reject(new Error("Missing email field."));
        }

        let emailParams = {
            name: name || "User",
            from_email: email,  // ✅ Ensure correct email key
            selected_plan: selectedPlan || "No Plan Selected"
        };

        console.log("📧 Sending email with:", JSON.stringify(emailParams));

        return emailjs.send("service_9fhnu4c", "template_0h7vmqw", emailParams)
            .then(response => {
                console.log("✅ Email successfully sent!", response);
                return response;
            })
            .catch(error => {
                console.error("❌ Email sending failed!", error);
                return Promise.reject(error);
            });
    }

    /* =======================================================
    SECTION 11: Handle Registration Form Submission
    ======================================================= */
    registerForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(registerForm);
        const formObject = Object.fromEntries(formData);

        // Ensure email exists
        let emailField = document.querySelector('input[name="email"]');
        let emailValue = emailField ? emailField.value.trim() : "";

        if (!emailValue) {
            console.error("❌ Email field is missing or empty!");
            alert("⚠ Please enter a valid email address.");
            return;
        }

        // ✅ Get Full Name (First + Last Name)
        let firstName = formObject.first_name || "";
        let lastName = formObject.last_name || "";
        let fullName = `${firstName} ${lastName}`.trim();

        // ✅ Ensure Selected Plan is Captured
        let selectedPlan = selectedPlanInput && selectedPlanInput.value.trim() !== ""
            ? selectedPlanInput.value
            : "No Plan Selected";

        console.log("📧 Captured Email:", emailValue);
        console.log("👤 Captured Name:", fullName);
        console.log("📝 Captured Selected Plan:", selectedPlan);

        // ✅ EmailJS Parameters
        let emailParams = {
            name: fullName,  // ✅ Full name instead of just first name
            from_email: emailValue,  // ✅ Ensure correct email
            selected_plan: selectedPlan  // ✅ Ensure correct plan is passed
        };

        console.log("📨 EmailJS Params:", emailParams);

        // ✅ Send Email using EmailJS
        sendConfirmationEmail(fullName, emailValue, selectedPlan)
            .then(() => {
                console.log("✅ Email sent successfully!");
                window.location.href = "/register/register?success=true"; // ✅ Redirect with success flag
            })
            .catch((error) => {
                console.error("❌ Email sending failed!", error);
                alert("⚠ Email failed, but registration will proceed.");
                window.location.href = "/register/register?success=true"; // ✅ Redirect regardless of email success
            });
    });

});