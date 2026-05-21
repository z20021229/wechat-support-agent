const API_BASE_URL = "http://127.0.0.1:8000";

const messageList = document.querySelector("#messageList");
const chatForm = document.querySelector("#chatForm");
const messageInput = document.querySelector("#messageInput");
const summaryButton = document.querySelector("#summaryButton");
const clearButton = document.querySelector("#clearButton");
const connectionStatus = document.querySelector("#connectionStatus");
const summaryPanel = document.querySelector("#summaryPanel");
const summaryContent = document.querySelector("#summaryContent");
const sessionStatePanel = document.querySelector("#sessionStatePanel");
const collectedInfoList = document.querySelector("#collectedInfoList");
const missingInfoList = document.querySelector("#missingInfoList");

const messages = [];
const welcomeText = "你好，我是技术支持 Agent。请描述你遇到的问题，我会先收集必要信息。";
let sessionId = createSessionId();

function createSessionId() {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID();
  }

  return `session-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function appendMessage(role, text, metaText = "") {
  const item = document.createElement("article");
  item.className = `message ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "我" : "A";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  if (metaText) {
    const meta = document.createElement("div");
    meta.className = "message-meta";
    meta.textContent = metaText;
    bubble.appendChild(meta);
  }

  item.append(avatar, bubble);
  messageList.appendChild(item);
  messageList.scrollTop = messageList.scrollHeight;
}

function setBusy(isBusy) {
  messageInput.disabled = isBusy;
  chatForm.querySelector("button[type='submit']").disabled = isBusy;
  summaryButton.disabled = isBusy;
  clearButton.disabled = isBusy;
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

function createList(items = []) {
  const list = document.createElement("ul");
  list.className = "summary-list";

  const safeItems = Array.isArray(items) && items.length > 0 ? items : ["待补充"];
  safeItems.forEach((item) => {
    const listItem = document.createElement("li");
    listItem.textContent = item;
    list.appendChild(listItem);
  });

  return list;
}

function renderStateList(listElement, items = [], emptyText) {
  listElement.replaceChildren();

  const safeItems = Array.isArray(items) && items.length > 0 ? items : [emptyText];
  safeItems.forEach((item) => {
    const listItem = document.createElement("li");
    listItem.textContent = item;
    listElement.appendChild(listItem);
  });
}

function renderSessionState(sessionState) {
  if (!sessionState) {
    sessionStatePanel.hidden = true;
    collectedInfoList.replaceChildren();
    missingInfoList.replaceChildren();
    return;
  }

  renderStateList(collectedInfoList, sessionState.collected_info, "暂无已收集信息");
  renderStateList(missingInfoList, sessionState.missing_info, "暂无待补充信息");
  sessionStatePanel.hidden = false;
}

function appendSummarySection(label, value) {
  const section = document.createElement("section");
  section.className = "summary-section";

  const heading = document.createElement("h2");
  heading.textContent = label;
  section.appendChild(heading);

  if (Array.isArray(value)) {
    section.appendChild(createList(value));
  } else {
    const text = document.createElement("p");
    text.textContent = value || "待补充";
    section.appendChild(text);
  }

  summaryContent.appendChild(section);
}

function renderSummary(data) {
  summaryContent.replaceChildren();

  appendSummarySection("标题", data.title);
  appendSummarySection("分类", `${data.label || "未分类"} / ${data.category || "unknown"}`);
  appendSummarySection("问题现象", data.problem_description);
  appendSummarySection("已收集信息", data.collected_info);
  appendSummarySection("可能原因", data.possible_causes);
  appendSummarySection("建议排查步骤", data.suggested_steps);
  appendSummarySection("状态", data.status);
  appendSummarySection("后续跟进", data.follow_up);

  summaryPanel.hidden = false;
}

async function resetConversation() {
  const previousSessionId = sessionId;
  sessionId = createSessionId();
  messages.length = 0;
  summaryContent.replaceChildren();
  summaryPanel.hidden = true;
  renderSessionState(null);
  messageList.replaceChildren();
  appendMessage("agent", welcomeText);
  messageInput.value = "";
  messageInput.focus();

  try {
    await postJson("/session/reset", {
      session_id: previousSessionId,
    });
  } catch (error) {
    // A fresh session_id is already active, so the UI must not reuse stale state.
  }
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
      session_id: sessionId,
      message,
    });

    const categoryLabel = data.classification?.label
      ? `分类：${data.classification.label}`
      : "";

    appendMessage("agent", data.reply, categoryLabel);
    messages.push({ role: "agent", content: data.reply, stage: data.stage });
    renderSessionState(data.session_state);
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
      session_id: sessionId,
      messages,
    });

    renderSummary(data);
    setStatus("后端已连接");
  } catch (error) {
    appendMessage("agent", "工单摘要生成失败，请确认后端服务已启动。");
    setStatus("后端连接失败", false);
  } finally {
    setBusy(false);
  }
});

clearButton.addEventListener("click", resetConversation);
