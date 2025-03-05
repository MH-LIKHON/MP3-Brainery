const uname = document.querySelector('#uname');
const pass = document.querySelector('#pass');
const btn = document.querySelector('#login-btn');
const form = document.querySelector('form');
const msg = document.querySelector('.msg');

btn.disabled = true;

function showMsg() {
    const isEmpty = uname.value === '' || pass.value === '';
    btn.classList.toggle('no-shift', !isEmpty);

    if (isEmpty) {
        btn.disabled = true;
        msg.style.color = 'rgb(218 49 49)';
        msg.innerText = 'Please fill in both fields before proceeding.';
    } else {
        msg.innerText = 'Great! Now you can proceed.';
        msg.style.color = '#20c997';
        btn.disabled = false;
    }
}

form.addEventListener('input', showMsg);