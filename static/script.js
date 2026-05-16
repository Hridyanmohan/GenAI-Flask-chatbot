const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const historyList = document.getElementById('historyList');
const newChatBtn = document.getElementById('newChatBtn');

let currentThreadId = null; // Tracks the currently active conversation thread

// Fetch and display threads when the page loads
async function loadThreads() {
    const response = await fetch('/threads');
    const threads = await response.json();
    historyList.innerHTML = '';
    
    threads.forEach(t => {
        const item = document.createElement('div');
        item.className = `history-item ${t.id === currentThreadId ? 'active' : ''}`;
        item.innerHTML = `
            <span class="history-title" onclick="switchThread('${t.id}')">${escapeHtml(t.title)}</span>
            <button class="delete-btn" onclick="deleteThread(event, '${t.id}')">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
            </button>
        `;
        historyList.appendChild(item);
    });
}

// Switch view context to load selected thread records
async function switchThread(id) {
    currentThreadId = id;
    document.getElementById('welcomeScreen').style.display = 'none';
    const response = await fetch(`/threads/${id}/messages`);
    const messages = await response.json();
    
    const container = document.getElementById('messagesContainer');
    container.innerHTML = '';
    
    messages.forEach(m => {
        const div = document.createElement('div');
        div.className = `message ${m.role === 'user' ? 'user-message-style' : 'ai-message-style'}`;
        div.innerHTML = `<div class="message-text">${m.role === 'user' ? escapeHtml(m.content) : marked.parse(m.content)}</div>`;
        container.appendChild(div);
    });
    
    loadThreads();
    document.getElementById('messagesEnd').scrollIntoView({ behavior: 'smooth' });
}

// Delete a single conversation thread
async function deleteThread(event, id) {
    event.stopPropagation(); // Prevents clicking the thread while trying to delete it
    await fetch(`/threads/${id}`, { method: 'DELETE' });
    if (currentThreadId === id) {
        startNewChat();
    } else {
        loadThreads();
    }
}

function startNewChat() {
    currentThreadId = null;
    document.getElementById('messagesContainer').innerHTML = '';
    document.getElementById('welcomeScreen').style.display = 'block';
    loadThreads();
}

newChatBtn.addEventListener('click', startNewChat);

// Submit form on Enter key press
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.requestSubmit();
    }
});

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = messageInput.value.trim();
    const model = document.getElementById('modelSelect').value;
    if (!message) return;

    document.getElementById('welcomeScreen').style.display = 'none';

    // Render User Message Bubble
    const container = document.getElementById('messagesContainer');
    const userDiv = document.createElement('div');
    userDiv.className = 'message user-message-style';
    userDiv.innerHTML = `<div class="message-text">${escapeHtml(message)}</div>`;
    container.appendChild(userDiv);
    
    messageInput.value = '';
    document.getElementById('messagesEnd').scrollIntoView({ behavior: 'smooth' });
    document.getElementById('loadingIndicator').style.display = 'block';

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, model, thread_id: currentThreadId })
        });
        
        const data = await response.json();
        document.getElementById('loadingIndicator').style.display = 'none';

        if (response.ok) {
            currentThreadId = data.thread_id; // Keep tracking the active thread ID
            const aiDiv = document.createElement('div');
            aiDiv.className = 'message ai-message-style';
            aiDiv.innerHTML = `<div class="message-text">${marked.parse(data.response_text)}</div>`;
            container.appendChild(aiDiv);
            
            loadThreads(); // Refresh the sidebar titles list
        }
        document.getElementById('messagesEnd').scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
        document.getElementById('loadingIndicator').style.display = 'none';
    }
});

function escapeHtml(t) { return t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

// Initialize threads on page load
loadThreads();