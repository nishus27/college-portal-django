const form = document.getElementById("chatForm");
const chatArea = document.getElementById("chatArea");
const input = document.getElementById("chatInput");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const message = input.value.trim();
    if (!message) return;

    chatArea.innerHTML += `<div class="msg user">${message}</div>`;
    input.value = "";

    const res = await fetch("/chatbot/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        },
        body: JSON.stringify({ message })
    });

    const data = await res.json();
    chatArea.innerHTML += `<div class="msg bot">${data.reply}</div>`;
    chatArea.scrollTop = chatArea.scrollHeight;
});
 