const API_BASE_URL = "http://127.0.0.1:8000";
const SESSION_ID = "demo-session";

const messageList = document.querySelector("#messageList");
const chatForm = document.querySelector("#chatForm");
const messageInput = document.querySelector("#messageInput");
const summaryButton = document.querySelector("#summaryButton");
const connectionStatus = document.querySelector("#connectionStatus");
const summaryPanel = document.querySelector("#summaryPanel");
const summaryTitle = document.querySelector("#summaryTitle");
const summaryText = document.querySelector("#summaryText");
const summaryStatus = document.querySelector("#summaryStatus");

const messages = [];

function appendMessage(role, text) {
  const item = document.createElement("article");
  item.className = `message ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "我" : "A";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  item.append(avatar, bubble);
  messageList.appendChild(item);
  messageList.scrollTop = messageList.scrollHeight;
}

function setBusy(isBusy) {
  messageInput.disabled = isBusy;
  chatForm.querySelector("button[type='submit']").disabled = isBusy;
  summaryButton.disabled = isBusy;
}

function setStatus(text, isOk = true) {
  connectionStatus.textContent = text;
  connectionStatus.dataset.state = isOk ? "ok" : "error";
}

async function postJson(path, payload) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json();
}

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = messageInput.value.trim();
  if (!message) {
    return;
  }

  appendMessage("user", message);
  messages.push({ role: "user", content: message });
  messageInput.value = "";
  setBusy(true);

  try {
    const data = await postJson("/chat", {
      session_id: SESSION_ID,
      message,
    });

    appendMessage("agent", data.reply);
    messages.push({ role: "agent", content: data.reply, stage: data.stage });
    setStatus("后端已连接");
  } catch (error) {
    appendMessage("agent", "后端暂时无法连接，请确认 FastAPI 服务已启动。");
    setStatus("后端连接失败", false);
  } finally {
    setBusy(false);
    messageInput.focus();
  }
});

summaryButton.addEventListener("click", async () => {
  setBusy(true);

  try {
    const data = await postJson("/summary", {
      session_id: SESSION_ID,
      messages,
    });

    summaryTitle.textContent = data.title;
    summaryText.textContent = data.summary;
    summaryStatus.textContent = data.status;
    summaryPanel.hidden = false;
    setStatus("后端已连接");
  } catch (error) {
    appendMessage("agent", "工单摘要生成失败，请确认后端服务已启动。");
    setStatus("后端连接失败", false);
  } finally {
    setBusy(false);
  }
});
