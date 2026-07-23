const ACCESS_TOKEN_KEY = "access_token";

let socket = null;
let socketConnecting = false;
let historyLoaded = false;
const pendingMessages = [];


function setJsonResult(elementId, data) {
    const element = document.getElementById(elementId);

    if (!element) return;

    element.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}


function setTextResult(elementId, message) {
    const element = document.getElementById(elementId);

    if (!element) return;

    element.textContent = message;
}


// ================= SIGNUP =================

async function signup() {

    const username = document.getElementById("signup_username").value;
    const email = document.getElementById("signup_email").value;
    const password = document.getElementById("signup_password").value;

    try {

        const response = await fetch("/signup", {
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

        const data = await response.json();
        setJsonResult("signup_message", data);

    } catch (error) {

        setTextResult("signup_message", "Error: " + error.message);
    }
}


// ================= LOGIN =================

async function login() {

    const email = document.getElementById("login_email").value;
    const password = document.getElementById("login_password").value;

    try {

        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();
        setJsonResult("login_message", data);

        if (response.ok && data.access_token) {

            localStorage.setItem(ACCESS_TOKEN_KEY, data.access_token);

            setTimeout(() => {
                window.location.href = "/static/chat.html";
            }, 600);
        }

    } catch (error) {

        setTextResult("login_message", "Error: " + error.message);
    }
}


// ================= GET USER =================

async function getUser() {

    const id = document.getElementById("user_id").value;

    try {

        const response = await fetch(`/users/${encodeURIComponent(id)}`);
        const data = await response.json();

        setJsonResult("user_result", data);

    } catch (error) {

        setTextResult("user_result", "Error: " + error.message);
    }
}


// ================= WEBSOCKET =================

function getChatBox() {
    return document.getElementById("chat-box");
}


function addMessage(message, sender) {

    const chatBox = document.getElementById("chat-box");

    if (!chatBox) return;

    let displayText = message;

    if (typeof message === "object") {

        displayText =
            message.response ||
            message.message ||
            message.answer ||
            message.content ||
            JSON.stringify(message, null, 2);

    }

    chatBox.innerHTML += `
        <div class="${sender}">
            <pre>${displayText}</pre>
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;
}

function renderHistory(messages) {

    const chatBox = getChatBox();

    if (!chatBox) return;

    const pendingText = pendingMessages
        .map((payload) => JSON.parse(payload).content)
        .filter(Boolean);

    chatBox.innerHTML = "";

    messages.forEach((message) => {
        const sender = message.role === "user" ? "user" : "bot";
        addMessage(message.content, sender);
    });

    pendingText.forEach((message) => {
        addMessage(message, "user");
    });
}


function getWebSocketUrl(token) {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    return `${protocol}//${window.location.host}/ws?token=${encodeURIComponent(token)}`;
}


function flushPendingMessages() {
    while (
        pendingMessages.length > 0 &&
        socket &&
        socket.readyState === WebSocket.OPEN
    ) {
        socket.send(pendingMessages.shift());
    }
}


function handleSocketMessage(rawData) {

    let data = null;

    try {
        data = JSON.parse(rawData);

    } catch (error) {
        addMessage(rawData, "bot");
        return;
    }


    console.log("BACKEND RESPONSE:", data);


    if (data.type === "history") {

        renderHistory(data.messages || []);

        historyLoaded = true;

        flushPendingMessages();

        return;
    }


    if (data.type === "message") {

        const sender = data.role === "user" ? "user" : "bot";


        let content = data.content;


        if (typeof content === "object") {

            content =
                content.response ||
                content.message ||
                content.answer ||
                JSON.stringify(content, null, 2);

        }


        addMessage(content || "No response", sender);

        return;
    }


    if (data.type === "error") {

        addMessage(
            data.content || "Something went wrong.",
            "bot"
        );

        return;
    }

    let fallback = data.content || rawData;


    if (typeof fallback === "object") {

        fallback = JSON.stringify(fallback, null, 2);

    }


    addMessage(fallback, "bot");
}


function connectSocket() {

    const chatBox = getChatBox();

    if (!chatBox) return;

    const token = localStorage.getItem(ACCESS_TOKEN_KEY);

    if (!token) {
        addMessage("Please log in first.", "bot");
        setTimeout(() => {
            window.location.href = "/";
        }, 800);
        return;
    }

    if (
        socket &&
        (
            socket.readyState === WebSocket.OPEN ||
            socket.readyState === WebSocket.CONNECTING
        )
    ) {
        return;
    }

    socketConnecting = true;
    historyLoaded = false;
    socket = new WebSocket(getWebSocketUrl(token));

    socket.onopen = function () {
        socketConnecting = false;
    };

    socket.onmessage = function (event) {
        handleSocketMessage(event.data);
    };

    socket.onclose = function (event) {
        socketConnecting = false;

        if (event.code === 1008) {
            localStorage.removeItem(ACCESS_TOKEN_KEY);
            addMessage("Your session expired. Please log in again.", "bot");
            setTimeout(() => {
                window.location.href = "/";
            }, 1000);
            return;
        }

        if (event.code !== 1000) {
            addMessage("Connection closed. Please refresh the page.", "bot");
        }
    };

    socket.onerror = function () {
        socketConnecting = false;
        addMessage("Connection error. Please try again.", "bot");
    };
}


function sendMessage() {

    const input = document.getElementById("ws_message");

    if (!input) return;

    const message = input.value.trim();

    if (message === "") return;

    input.value = "";
    addMessage(message, "user");

    const payload = JSON.stringify({
        type: "message",
        content: message
    });

    if (
        socket &&
        socket.readyState === WebSocket.OPEN &&
        historyLoaded
    ) {
        socket.send(payload);
        return;
    }

    pendingMessages.push(payload);

    if (!socketConnecting) {
        connectSocket();
    }
}


document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("ws_message");

    if (input) {
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                sendMessage();
            }
        });
    }

    if (getChatBox()) {
        connectSocket();
    }
});
