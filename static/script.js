const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const voiceBtn = document.getElementById('voiceBtn');
const clearBtn = document.getElementById('clearBtn');
const voiceOutput = document.getElementById('voiceOutput');
const status = document.getElementById('status');

const sessionId = 'session_' + Date.now();
let isListening = false;
let recognition = null;
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        isListening = true;
        voiceBtn.classList.add('listening');
        status.textContent = 'Listening...';
        status.className = 'status listening';
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        messageInput.value = transcript;
        sendMessage();
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        status.textContent = 'Voice recognition error. Please try again.';
        status.className = 'status error';
        stopListening();
    };

    recognition.onend = () => stopListening();
} else {
    voiceBtn.style.display = 'none';
    status.textContent = 'Voice input not supported in this browser';
}

function stopListening() {
    isListening = false;
    voiceBtn.classList.remove('listening');
    if (status.textContent === 'Listening...') {
        status.textContent = '';
        status.className = 'status';
    }
}

function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'lisa-message'}`;
    messageDiv.innerHTML = `<div class="message-content">${content}</div>`;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'message lisa-message';
    indicator.id = 'typingIndicator';
    indicator.innerHTML = `
        <div class="message-content typing-indicator">
            <span></span><span></span><span></span>
        </div>`;
    chatContainer.appendChild(indicator);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}
function speak(text) {
    if (!voiceOutput.checked || !text) return;

    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1;
        utterance.pitch = 1;
        utterance.volume = 1;

        const voices = window.speechSynthesis.getVoices();
        const femaleVoice = voices.find(v =>
            v.name.toLowerCase().includes('female') ||
            v.name.toLowerCase().includes('samantha') ||
            v.name.toLowerCase().includes('victoria') ||
            v.name.toLowerCase().includes('zira') ||
            v.name.toLowerCase().includes('karen')
        );
        if (femaleVoice) utterance.voice = femaleVoice;

        window.speechSynthesis.speak(utterance);
    }
}


async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    addMessage(message, true);
    messageInput.value = '';
    showTypingIndicator();
    status.textContent = 'Lisa is thinking...';
    status.className = 'status';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, session_id: sessionId })
        });

        const data = await response.json();
        removeTypingIndicator();

        if (data.error) {
            status.textContent = data.error;
            status.className = 'status error';
            return;
        }

        addMessage(data.response);
        speak(data.response);
        status.textContent = '';
    } catch (error) {
        removeTypingIndicator();
        status.textContent = 'Failed to connect. Please try again.';
        status.className = 'status error';
        console.error('Error:', error);
    }
}


async function clearChat() {
    try {
        await fetch('/api/clear', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId })
        });

        chatContainer.innerHTML = '';
        addMessage("Chat cleared! How can I help you?");
        status.textContent = 'Conversation cleared';
        setTimeout(() => { status.textContent = ''; }, 2000);
    } catch (error) {
        console.error('Error:', error);
    }
}

voiceBtn.addEventListener('click', () => {
    if (!recognition) return;

    if (isListening) recognition.stop();
    else recognition.start();
});

sendBtn.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

clearBtn.addEventListener('click', clearChat);
if ('speechSynthesis' in window) window.speechSynthesis.getVoices();
