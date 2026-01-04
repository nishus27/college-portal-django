async function sendMessage() {
  const input = document.getElementById("chat-input");
  const message = input.value.trim();
  if (!message) return;

  addUserMessage(message);
  input.value = "";

  const response = await fetch("/chatbot/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken()
    },
    body: JSON.stringify({ message })
  });

  const data = await response.json();
  addBotMessage(data.reply);
}
 