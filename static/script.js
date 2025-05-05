// Theme handling
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) toggleBtn.addEventListener('click', toggleTheme);
});

// Voice recognition
let recognition = null;
let isListening = false;

function initializeVoiceRecognition() {
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById("user-input").value = transcript;
        sendMessage();
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        isListening = false;
        updateMicButton();
    };

    recognition.onend = function() {
        isListening = false;
        updateMicButton();
    };
}

function toggleVoiceInput() {
    if (!recognition) {
        initializeVoiceRecognition();
    }

    if (isListening) {
        recognition.stop();
    } else {
        recognition.start();
        isListening = true;
    }
    updateMicButton();
}

function updateMicButton() {
    const micButton = document.getElementById("mic-button");
    if (!micButton) return;

    micButton.innerHTML = isListening
        ? `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="red" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>`
        : `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>`;

    micButton.classList.toggle("listening", isListening);
}

// Send message to backend
async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const message = input.value.trim();

    if (message !== "") {
        // User message
        const userMessage = document.createElement("div");
        userMessage.className = "message user";
        userMessage.textContent = message;
        chatBox.appendChild(userMessage);

        // Loading animation
        const loadingMessage = document.createElement("div");
        loadingMessage.className = "message bot loading";
        loadingMessage.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
        chatBox.appendChild(loadingMessage);
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            console.log('Sending message:', message);
            const response = await fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Response data:', data);

            // Remove loading message
            chatBox.removeChild(loadingMessage);

            // Create and append bot response
            const botMessage = document.createElement("div");
            botMessage.className = "message bot";
            
            // Check if the response contains weather data
            if (data.response && (data.response.includes('Temperature') || data.response.includes('Weather'))) {
                // Format weather response with line breaks
                botMessage.innerHTML = data.response.replace(/\n/g, '<br>');
            } else if (data.response) {
                botMessage.textContent = data.response;
            } else {
                throw new Error('No response data received');
            }
            
            chatBox.appendChild(botMessage);
        } catch (error) {
            console.error('Error:', error);
            // Remove loading message
            chatBox.removeChild(loadingMessage);

            // Create and append error message
            const errorMessage = document.createElement("div");
            errorMessage.className = "message bot error";
            errorMessage.textContent = `Error: ${error.message}. Please try again.`;
            chatBox.appendChild(errorMessage);
        }

        // Clear input and scroll to bottom
        input.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
