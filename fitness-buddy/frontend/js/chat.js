/**
 * chat.js – AI chat panel logic.
 */

const Chat = (() => {
  let _messagesEl, _inputEl, _sendBtn;

  function init(messagesId, inputId, sendBtnId) {
    _messagesEl = document.getElementById(messagesId);
    _inputEl    = document.getElementById(inputId);
    _sendBtn    = document.getElementById(sendBtnId);

    if (!_messagesEl || !_inputEl || !_sendBtn) return;

    _sendBtn.addEventListener("click", sendMessage);
    _inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    });

    // Suggestion chip clicks
    document.querySelectorAll(".chat-suggestion-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        _inputEl.value = btn.dataset.msg || btn.textContent;
        sendMessage();
      });
    });

    appendBotMessage("👋 Hi! I'm Fitness Buddy, your AI wellness companion. Ask me for a workout, meal ideas, or motivation!");
  }

  function appendUserMessage(text) {
    const div = document.createElement("div");
    div.className = "chat-msg user";
    div.textContent = text;
    _messagesEl.appendChild(div);
    _messagesEl.scrollTop = _messagesEl.scrollHeight;
  }

  function appendBotMessage(text) {
    const div = document.createElement("div");
    div.className = "chat-msg bot";
    div.textContent = text;
    _messagesEl.appendChild(div);
    _messagesEl.scrollTop = _messagesEl.scrollHeight;
    return div;
  }

  function showLoading() {
    const div = document.createElement("div");
    div.className = "chat-msg bot loading";
    div.id = "chat-loading";
    div.innerHTML = '<span class="spinner"></span> Thinking…';
    _messagesEl.appendChild(div);
    _messagesEl.scrollTop = _messagesEl.scrollHeight;
  }

  function hideLoading() {
    const el = document.getElementById("chat-loading");
    if (el) el.remove();
  }

  async function sendMessage() {
    const text = _inputEl.value.trim();
    if (!text) return;

    _inputEl.value = "";
    _sendBtn.disabled = true;
    appendUserMessage(text);
    showLoading();

    try {
      const profile = Profile.get();
      const data = await API.chat({ message: text, profile });
      hideLoading();
      appendBotMessage(data.reply);
    } catch (err) {
      hideLoading();
      appendBotMessage("⚠️ Sorry, I couldn't connect to the AI. Please check your connection and try again.");
      console.error("Chat error:", err);
    } finally {
      _sendBtn.disabled = false;
      _inputEl.focus();
    }
  }

  return { init };
})();
