document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');

    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (isUser) {
            messageContent.innerHTML = `<strong>You:</strong> ${content}`;
        } else {
            messageContent.innerHTML = `<strong>AI Assistant:</strong> ${content}`;
        }
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function sendMessage() {
        const message = userInput.value.trim();
        
        if (!message) {
            return;
        }
        
        addMessage(message, true);
        
        userInput.value = '';
        userInput.disabled = true;
        sendBtn.disabled = true;
        
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                addMessage(data.response);
            } else if (data.error) {
                addMessage('Sorry, there was an error processing your message. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Sorry, I encountered a connection error. Please try again.');
        })
        .finally(() => {
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        });
    }

    sendBtn.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    userInput.focus();
});
