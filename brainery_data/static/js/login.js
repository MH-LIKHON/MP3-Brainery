/* =======================================================
SECTION 1: Element Selection
======================================================= */
// Select the necessary DOM elements for the login functionality
const email = document.querySelector('#email');
const pass = document.querySelector('#pass');
const btn = document.querySelector('#login-btn');
const form = document.querySelector('form');
const msg = document.querySelector('.msg');

// Select elements for reset password popup
const forgotPasswordLink = document.querySelector('#forgot-password-link');
const resetPopup = document.querySelector('#reset-password-popup');
const resetEmail = document.querySelector('#reset-email');
const resetNewPassword = document.querySelector('#reset-new-password');
const resetForm = document.querySelector('#reset-password-form');
const resetMessage = document.querySelector('#reset-message');
const closePopup = document.querySelector('#close-popup');

/* =======================================================
SECTION 2: Initial Button State Setup
======================================================= */
// Initially disable the login button
btn.disabled = true;

/* =======================================================
SECTION 3: Form Validation and Message Display
======================================================= */
// Function to check if both email and password are filled in
function showMsg() {
    // Check if either the email or password field is empty
    const isEmpty = email.value.trim() === '' || pass.value.trim() === '';

    // Toggle button appearance based on whether the fields are empty
    btn.classList.toggle('no-shift', !isEmpty);

    // If any field is empty, disable the button and show a message
    if (isEmpty) {
        btn.disabled = true;
        msg.style.color = 'rgb(218 49 49)';
        msg.innerText = 'Please fill in both fields before proceeding.';
    } else {
        // If both fields are filled, enable the button and show a success message
        msg.innerText = 'Great! Now you can proceed.';
        msg.style.color = '#20c997';
        btn.disabled = false;
    }
}

/* =======================================================
SECTION 4: Event Listener for Input Changes
======================================================= */
// Attach an event listener to the form to trigger showMsg on any input change
form.addEventListener('input', showMsg);

/* =======================================================
SECTION 5: Reset Password Functionality
======================================================= */

// Show the Reset Password Popup
forgotPasswordLink.addEventListener("click", function (event) {
    event.preventDefault();
    resetPopup.style.display = "block";
});

// Hide the Reset Password Popup
closePopup.addEventListener("click", function () {
    resetPopup.style.display = "none";
});

// Handle Reset Password Form Submission
resetForm.addEventListener("submit", function (event) {
    event.preventDefault();

    // Extract user inputs
    const emailValue = resetEmail.value.trim();
    const newPasswordValue = resetNewPassword.value.trim();

    // Validate inputs
    if (!emailValue || !newPasswordValue) {
        resetMessage.innerText = "❌ Please fill in all fields.";
        resetMessage.style.color = "red";
        return;
    }

    // Fetch CSRF token from meta tag
    const csrfToken = document.querySelector("meta[name='csrf-token']").getAttribute("content");

    // Send a request to the Flask backend to reset the user's password with CSRF protection
    fetch("/auth/reset_password", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ email: emailValue, new_password: newPasswordValue })
    })
        .then(response => {
            console.log("🔍 Response Status:", response.status);

            // Handle server response and check if the request was successful
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text); });
            }
            return response.json();
        })
        .then(data => {
            console.log("🔍 Response Data:", data);

            // Display success or error messages based on the response
            if (data.message) {
                resetMessage.innerText = "✅ " + data.message;
                resetMessage.style.color = "green";

                // Auto-close the reset popup after success
                setTimeout(() => { resetPopup.style.display = "none"; }, 2000);
            } else {
                resetMessage.innerText = "❌ " + (data.error || "Unknown error");
                resetMessage.style.color = "red";
            }
        })
        .catch(error => {
            console.error("❌ ERROR:", error);

            // Display an error message if CSRF validation fails
            resetMessage.innerText = "❌ CSRF error: Refresh the page and try again.";
            resetMessage.style.color = "red";
        });
});

/* =======================================================
SECTION 6: Auto-hide Flash Message
======================================================= */
document.addEventListener("DOMContentLoaded", function () {
    const flashMessages = document.querySelectorAll('.alert');

    // Show the flash message if it's not already shown
    flashMessages.forEach(msg => {

        // Time out function
        setTimeout(function () {
            msg.style.opacity = '0';

            // After the fade-out transition, hide the message
            setTimeout(function () {
                msg.style.display = 'none';
            }, 500);
        }, 2500);
    });
});