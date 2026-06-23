/* =======================
   SWIPER (your existing code)
======================= */
var swiper = new Swiper(".home", {
    spaceBetween: 30,
    centeredSlides: true,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});

/* =======================
   MENU TOGGLE
======================= */
let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navbar.classList.toggle('active');
};

window.onscroll = () => {
    menu.classList.remove('bx-x');
    navbar.classList.remove('active');
};

/* =======================
   REGISTER FUNCTION (NEW)
======================= */
const API_BASE_URL = "/api";

function register() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch(`${API_BASE_URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert("Registration successful!");
            window.location.href = "login.html";
        } else {
            alert(data.message || "Registration failed");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Server error");
    });
}

/* =======================
   LOGIN FUNCTION (NEW)
======================= */
function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert("Login successful!");
            localStorage.setItem("user_id", data.user_id);
            localStorage.setItem("username", data.username);
            window.location.href = "index.html";
        } else {
            alert("Invalid credentials");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Server error");
    });
}