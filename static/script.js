
function formatText(text) {
    if (typeof text !== 'string') return text;

    text = text.replace(
        /(https?:\/\/[^\s]+|www\.[^\s]+)/g,
        url => {
            const href = url.startsWith('http') ? url : `https://${url}`;
            return `<a href="${href}" target="_blank" style="color:#007bff; text-decoration:none;">${url}</a>`;
        }
    );
    text = text.replace(/(\d+\.)\s/g, '<br>$1 '); 
    text = text.replace(/\n/g, '<br>');

    return text.trim();
}

function renderJSON(data, indent = 0) {
    let html = '';
    const indentSpace = '&nbsp;'.repeat(indent * 4);

    for (const key in data) {
        const value = data[key];

        if (Array.isArray(value)) {
            html += `${indentSpace}<strong>${key}:</strong><ul>`;
            value.forEach(item => {
                if (key.toLowerCase().includes('link')) {
                    const href = item.startsWith('http') ? item : `https://${item}`;
                    html += `<li><a href="${href}" target="_blank" style="color:#007bff; text-decoration:none;">${item}</a></li>`;
                } else {
                    html += `<li>${formatText(item)}</li>`;
                }
            });
            html += `</ul>`;
        } 
        else if (typeof value === 'object' && value !== null) {
            html += `${indentSpace}<strong>${key}:</strong><br>${renderJSON(value, indent + 1)}`;
        } 
        else {
            html += `${indentSpace}<strong>${key}:</strong> ${formatText(value)}<br>`;
        }
    }

    return html;
}



document.addEventListener('DOMContentLoaded', function () {
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
                console.log('Full JSON:', data);

                if (data.error) {
                    addMessage('Sorry, there was an error processing your message. Please try again.');
                } else {
                    const formatted = renderJSON(data);
                    addMessage(formatted);
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

    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    userInput.focus();
});
