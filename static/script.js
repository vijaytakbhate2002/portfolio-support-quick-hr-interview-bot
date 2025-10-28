
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

document.addEventListener("DOMContentLoaded", () => {
    const badges = [
        { file: "Code_Tagger.svg", title: "Code Tagger Badge", issuer: "Kaggle" },
        { file: "Code_Uploader.svg", title: "Code Uploader Badge", issuer: "Kaggle" },
        { file: "Community_competitor.svg", title: "Community Competitor Badge", issuer: "Kaggle" },
        { file: "Dataset_Contributor.svg", title: "Dataset Contributor Badge", issuer: "Kaggle" },
        { file: "Github_Coder.svg", title: "GitHub Coder Badge", issuer: "Kaggle" },
        { file: "Kaggle_Award.svg", title: "Kaggle Award Badge", issuer: "Kaggle" },
        { file: "Notebook_Modeler.svg", title: "Notebook Modeler Badge", issuer: "Kaggle" },
        { file: "Python_Coder.svg", title: "Python Coder Badge", issuer: "Kaggle" },
        { file: "Stylish.svg", title: "Stylish Badge", issuer: "Kaggle" }
    ];

    const certContainer = document.querySelector(".cert-container");

    badges.forEach(badge => {
        const certDiv = document.createElement("div");
        certDiv.classList.add("cert-item");

        certDiv.innerHTML = `
            <img src="static/kaggle_badges/${badge.file}" alt="${badge.title}" class="cert-thumb">
            <h3>${badge.title}</h3>
            <p>Issued by ${badge.issuer}</p>
            <a href="https://www.kaggle.com/vijay20213" target="_blank" class="view-cert">
                <i class="fas fa-external-link-alt"></i> Visit Profile
            </a>
        `;

        certContainer.appendChild(certDiv);
    });
});

const slider = document.getElementById('certSlider');
const slideLeft = document.getElementById('slideLeft');
const slideRight = document.getElementById('slideRight');

slideLeft.addEventListener('click', () => {
    slider.scrollBy({
        left: -300,
        behavior: 'smooth'
    });
});

slideRight.addEventListener('click', () => {
    slider.scrollBy({
        left: 300,
        behavior: 'smooth'
    });
});

document.addEventListener("DOMContentLoaded", function() {
  const closeBanner = document.getElementById("close-banner");
  const banner = document.getElementById("mobile-warning");

  if (closeBanner && banner) {
    closeBanner.addEventListener("click", function() {
      banner.style.display = "none";
    });
  }
});
