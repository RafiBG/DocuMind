
// Conversation ID
let conversationId = sessionStorage.getItem(
    "documind_conversation_id"
);

if (!conversationId) {
    conversationId = crypto.randomUUID();

    sessionStorage.setItem(
        "documind_conversation_id",
        conversationId
    );
}


// DOM elements
const uploadInput = document.getElementById("pdf-upload");
const uploadStatus = document.getElementById("upload-status");
const documentList = document.getElementById("document-list");

const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");


// Upload PDF
uploadInput.addEventListener("change", async () => {
    const file = uploadInput.files[0];

    if (!file) {
        return;
    }

    uploadStatus.textContent = `Uploading ${file.name}...`;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/api/documents/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Upload failed.");
        }

        uploadStatus.textContent =
            `Processed ${result.filename}: ${result.pages} pages, ${result.chunks} chunks.`;

        addDocument(result.filename);

    } catch (error) {
        uploadStatus.textContent = error.message;

    } finally {
        uploadInput.value = "";
    }
});


// Add uploaded document to sidebar
function addDocument(filename) {
    const emptyMessage = document.querySelector(".empty-documents");

    if (emptyMessage) {
        emptyMessage.remove();
    }

    // Avoid duplicate names in the sidebar
    const existingDocuments = Array.from(
        documentList.querySelectorAll(".document-item")
    );

    const existing = existingDocuments.find(
        item => item.dataset.filename === filename
    );

    if (existing) {
        return;
    }

    const item = document.createElement("div");
    item.className = "document-item";
    item.dataset.filename = filename;

    const icon = document.createElement("span");
    icon.className = "document-icon";
    icon.textContent = "📄";

    const name = document.createElement("span");
    name.textContent = filename;

    item.append(icon, name);
    documentList.appendChild(item);
}


// Send question
chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    addMessage("user", question);

    questionInput.value = "";
    questionInput.style.height = "auto";

    sendButton.disabled = true;

    const loading = addLoadingMessage();

    try {
        const response = await fetch("/api/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question,
                conversation_id: conversationId
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Chat request failed.");
        }

        loading.remove();

        addMessage(
            "assistant",
            result.answer,
            result.sources
        );

    } catch (error) {
        loading.remove();

        addMessage(
            "assistant",
            `Error: ${error.message}`
        );

    } finally {
        sendButton.disabled = false;
        questionInput.focus();
    }
});


// Create chat message
function addMessage(role, content, sources = []) {
    const welcome = document.querySelector(".welcome-message");

    if (welcome) {
        welcome.remove();
    }

    const message = document.createElement("div");
    message.className = `message ${role}-message`;

    const header = document.createElement("div");
    header.className = "message-header";
    header.textContent = role === "user" ? "You" : "DocuMind";

    const body = document.createElement("div");
    body.className = "message-content";
    body.textContent = content;

    message.append(header, body);

    if (role === "assistant" && sources.length > 0) {
        const sourceContainer = document.createElement("div");
        sourceContainer.className = "sources";

        const sourceTitle = document.createElement("h3");
        sourceTitle.textContent = "Sources";

        sourceContainer.appendChild(sourceTitle);

        for (const source of sources) {
            const sourceItem = document.createElement("div");
            sourceItem.className = "source-item";

            const page = document.createElement("span");
            page.className = "source-page";
            page.textContent = `Page ${source.page}`;

            const filename = document.createElement("span");
            filename.textContent = source.source;

            sourceItem.append(page, filename);
            sourceContainer.appendChild(sourceItem);
        }

        message.appendChild(sourceContainer);
    }

    chatMessages.appendChild(message);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// Loading indicator
function addLoadingMessage() {
    const message = document.createElement("div");
    message.className = "loading-message";
    message.textContent = "DocuMind is searching the documents...";

    chatMessages.appendChild(message);

    chatMessages.scrollTop = chatMessages.scrollHeight;

    return message;
}


// Enter sends message, Shift+Enter creates new line
questionInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        chatForm.requestSubmit();
    }
});


// Automatically resize input
questionInput.addEventListener("input", () => {
    questionInput.style.height = "auto";

    questionInput.style.height =
        `${questionInput.scrollHeight}px`;
});
