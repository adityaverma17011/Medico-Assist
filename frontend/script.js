// Handle Form Submission (Analyze)
document.getElementById("uploadForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const formData = new FormData(this);

  const response = await fetch("http://127.0.0.1:8000/analyze/", {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  const formatted = formatAsHTML(data.response || "No result.");

  // Display initial analysis in result section
//   document.getElementById("result").innerHTML = formatted;

  // Inject analysis into chat window
  appendChatMessage("LLM", data.response || "No result.");
});

function formatAsHTML(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n/g, "<br>");
}

// Append chat message to UI
function appendChatMessage(sender, message) {
  const chatContainer = document.getElementById("chatContainer");
  const msgDiv = document.createElement("div");
  msgDiv.className = "chat-message " + (sender === "user" ? "user-message" : "bot-message");
  msgDiv.innerHTML = formatAsHTML(message);
  chatContainer.appendChild(msgDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Handle Chat Submission
async function sendChat() {
  const input = document.getElementById("chatInput");
  const message = input.value.trim();
  if (!message) return;

  appendChatMessage("user", message);

  const formData = new FormData();
  formData.append("message", message);

  const response = await fetch("http://127.0.0.1:8000/chat/", {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  appendChatMessage("LLM", data.reply || "No reply.");

  input.value = "";
  input.style.height = "auto"; // Reset height after sending
}

// Auto-resize the textarea as user types
function autoResize(textarea) {
  textarea.style.height = "auto";
  textarea.style.height = textarea.scrollHeight + "px";
}

// Enable ChatGPT-style Enter/Shift+Enter
document.getElementById("chatInput").addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendChat();
  }
});


// Google Translate Initialization
function googleTranslateElementInit() {
  new google.translate.TranslateElement({
    pageLanguage: 'en',
    includedLanguages: 'en,hi,bn,gu,kn,ml,mr,pa,ta,te',
    layout: google.translate.TranslateElement.InlineLayout.SIMPLE
  }, 'google_translate_element');
}

// Load Translate script dynamically
(function loadGoogleTranslateScript() {
  const script = document.createElement('script');
  script.type = "text/javascript";
  script.src = "//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
  document.body.appendChild(script);
})();


