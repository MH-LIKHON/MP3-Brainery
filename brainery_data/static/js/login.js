/* =======================================================
SECTION 1: Element Selection
======================================================= */
// Select the necessary DOM elements for the login functionality
const uname = document.querySelector('#uname');        // Username input field
const pass = document.querySelector('#pass');          // Password input field
const btn = document.querySelector('#login-btn');      // Login button
const form = document.querySelector('form');           // The form element
const msg = document.querySelector('.msg');            // Message element to display validation messages

/* =======================================================
SECTION 2: Initial Button State Setup
======================================================= */
// Initially disable the login button
btn.disabled = true;

/* =======================================================
SECTION 3: Form Validation and Message Display
======================================================= */
// Function to check if both username and password are filled in
function showMsg() {
    // Check if either the username or password field is empty
    const isEmpty = uname.value === '' || pass.value === '';

    // Toggle button appearance based on whether the fields are empty
    btn.classList.toggle('no-shift', !isEmpty);

    // If any field is empty, disable the button and show a message
    if (isEmpty) {
        btn.disabled = true;  // Disable the button
        msg.style.color = 'rgb(218 49 49)'; // Red color for the message
        msg.innerText = 'Please fill in both fields before proceeding.'; // Display error message
    } else {
        // If both fields are filled, enable the button and show a success message
        msg.innerText = 'Great! Now you can proceed.';  // Display success message
        msg.style.color = '#20c997';                    // Green color for the message
        btn.disabled = false;                           // Enable the button
    }
}

/* =======================================================
SECTION 4: Event Listener for Input Changes
======================================================= */
// Attach an event listener to the form to trigger showMsg on any input change
form.addEventListener('input', showMsg);