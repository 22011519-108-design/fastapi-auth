// ================= SIGNUP =================

async function signup() {

    let username = document.getElementById("signup_username").value;
    let email = document.getElementById("signup_email").value;
    let password = document.getElementById("signup_password").value;

    try {

        let response = await fetch("http://127.0.0.1:8000/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });

        let data = await response.json();

        document.getElementById("signup_message").innerHTML =
            `<pre>${JSON.stringify(data, null, 2)}</pre>`;

    } catch (error) {

        document.getElementById("signup_message").innerHTML =
            "❌ Error: " + error.message;
    }
}


// ================= LOGIN =================

async function login() {

    let email = document.getElementById("login_email").value;
    let password = document.getElementById("login_password").value;

    try {

        let response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        let data = await response.json();

        document.getElementById("login_message").innerHTML =
            `<pre>${JSON.stringify(data, null, 2)}</pre>`;

        // Save JWT token
        if (data.access_token) {

            localStorage.setItem("access_token", data.access_token);

            setTimeout(() => {
                window.location.href = "/static/chat.html";
            }, 1000);

        }

    } catch (error) {

        document.getElementById("login_message").innerHTML =
            "❌ Error: " + error.message;
    }

}


// ================= GET USER =================

async function getUser() {

    let id = document.getElementById("user_id").value;

    try {

        let response = await fetch(
            `http://127.0.0.1:8000/users/${id}`
        );

        let data = await response.json();

        document.getElementById("user_result").innerHTML =
            `<pre>${JSON.stringify(data, null, 2)}</pre>`;

    } catch (error) {

        document.getElementById("user_result").innerHTML =
            "❌ Error: " + error.message;
    }

}


// ================= WEBSOCKET =================

let socket = null;

function addMessage(text, sender) {

    const chatBox = document.getElementById("chat-box");

    const message = document.createElement("div");
    message.className = `message ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerText = text;

    message.appendChild(bubble);
    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;
}

function connectSocket() {

    const token = localStorage.getItem("access_token");

    socket = new WebSocket(
        `ws://127.0.0.1:8000/ws?token=${token}`
    );

    socket.onopen = function () {

        addMessage("Connected ✅", "bot");

    };

    socket.onmessage = function (event) {

        addMessage(event.data, "bot");

    };

    socket.onclose = function () {

        addMessage("Connection Closed ❌", "bot");

    };

    socket.onerror = function () {

        addMessage("Connection Error ❌", "bot");

    };

}

function sendMessage() {

    const input = document.getElementById("ws_message");
    const message = input.value.trim();

    if (message === "") return;

    if (!socket || socket.readyState !== WebSocket.OPEN) {

        connectSocket();

        socket.onopen = function () {

            addMessage("Connected ✅", "bot");

            socket.send(message);

            addMessage(message, "user");

        };

    } else {

        socket.send(message);

        addMessage(message, "user");

    }

    input.value = "";

}

document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("ws_message");

    input.addEventListener("keypress", function (e) {

        if (e.key === "Enter") {

            sendMessage();

        }

    });

});