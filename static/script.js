document.addEventListener("DOMContentLoaded", function () {
  // --- Mobile Menu Toggle ---
  const menuToggle = document.getElementById("mobile-menu");
  const navMenu = document.querySelector(".nav-menu");

  if (menuToggle) {
    menuToggle.addEventListener("click", () => {
      navMenu.classList.toggle("active");
      const icon = menuToggle.querySelector("i");
      if (navMenu.classList.contains("active")) {
        icon.classList.remove("fa-bars");
        icon.classList.add("fa-times");
      } else {
        icon.classList.remove("fa-times");
        icon.classList.add("fa-bars");
      }
    });
  }

  // --- Scroll Animations ---
  const observerOptions = {
    threshold: 0.1,
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  }, observerOptions);

  // Select elements to animate
  const animatedElements = document.querySelectorAll(
    ".section-title, .project-card, .timeline-item, .skill-card, .pub-card",
  );
  animatedElements.forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(30px)";
    el.style.transition = "all 0.6s ease-out";
    observer.observe(el);
  });

  // --- Chatbot Logic ---
  const chatMessages = document.getElementById("chatMessages");
  const userInput = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");

  // Modal Elements
  const chatbotModal = document.getElementById("chatbotModal");
  const closeChatBtn = document.getElementById("closeChatBtn");
  const chatFab = document.getElementById("chatFab");
  const heroChatBtn = document.getElementById("heroChatBtn");

  // Open Modal
  function openModal() {
    if (chatbotModal) chatbotModal.style.display = "flex";
  }

  // Close Modal
  function closeModal() {
    if (chatbotModal) chatbotModal.style.display = "none";
  }

  if (chatFab) chatFab.addEventListener("click", openModal);
  if (heroChatBtn) heroChatBtn.addEventListener("click", openModal);
  if (closeChatBtn) closeChatBtn.addEventListener("click", closeModal);

  // Close on outside click
  window.addEventListener("click", (e) => {
    if (e.target === chatbotModal) closeModal();
  });

  function formatText(text) {
    if (typeof text !== "string") return text;
    text = text.replace(/(https?:\/\/[^\s]+|www\.[^\s]+)/g, (url) => {
      const href = url.startsWith("http") ? url : `https://${url}`;
      return `<a href="${href}" target="_blank" style="color:#00f2ea; text-decoration:underline;">${url}</a>`;
    });
    text = text.replace(/(\d+\.)\s/g, "<br>$1 ");
    text = text.replace(/\n/g, "<br>");
    return text.trim();
  }

  function renderJSON(data, indent = 0) {
    let html = "";
    const indentSpace = "&nbsp;".repeat(indent * 4);

    for (const key in data) {
      const value = data[key];
      if (Array.isArray(value)) {
        html += `${indentSpace}<strong>${key}:</strong><ul>`;
        value.forEach((item) => {
          if (key.toLowerCase().includes("link")) {
            const href = item.startsWith("http") ? item : `https://${item}`;
            html += `<li><a href="${href}" target="_blank" style="color:#00f2ea;">${item}</a></li>`;
          } else {
            html += `<li>${formatText(item)}</li>`;
          }
        });
        html += `</ul>`;
      } else if (typeof value === "object" && value !== null) {
        html += `${indentSpace}<strong>${key}:</strong><br>${renderJSON(value, indent + 1)}`;
      } else {
        html += `${indentSpace}<strong>${key}:</strong> ${formatText(value)}<br>`;
      }
    }
    return html;
  }

  function addMessage(content, isUser = false) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${isUser ? "user-message" : "ai-message"}`;
    messageDiv.innerHTML = isUser ? content : `<strong></strong> ${content}`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, true);
    userInput.value = "";
    userInput.disabled = true;
    sendBtn.disabled = true;

    // Show loader
    // const loadingDiv = document.createElement("div");
    // loadingDiv.className = "message ai-message";
    // loadingDiv.innerHTML = '<span class="loader"></span>';
    // chatMessages.appendChild(loadingDiv);
    // chatMessages.scrollTop = chatMessages.scrollHeight;

    // Show animated typing indicator
    const loadingDiv = document.createElement("div");
    loadingDiv.className = "message ai-message typing-indicator";
    loadingDiv.innerHTML = `
      <div class="typing-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    `;
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message }),
    })
      .then((response) => response.json())
      .then((data) => {
        chatMessages.removeChild(loadingDiv);
        if (data.error) {
          addMessage("Sorry, something went wrong. Please try again.");
        } else {
          // Handle structured RAG response
          let content = "";

          if (data.response_message) {
            content += formatText(data.response_message);
          } else if (data["AI Assistant"]) {
            // Fallback for backward compatibility if needed, or if error structure differs
            content += renderJSON(data);
          }

          // Append Reference Links if available
          if (
            data.reference_links &&
            Array.isArray(data.reference_links) &&
            data.reference_links.length > 0
          ) {
            content +=
              '<div class="reference-section" style="margin-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 5px;">';
            content +=
              '<strong style="display:block; margin-bottom: 5px; font-size: 0.9em; color: #a0a0a0;">References:</strong>';
            content +=
              '<ul style="padding-left: 20px; list-style-type: disc; font-size: 0.85em;">';
            data.reference_links.forEach((link) => {
              const href = link.startsWith("http") ? link : `https://${link}`;
              // Try to make a readable label from the URL if possible, or just show the URL
              let label = link.split("/").pop() || link;
              if (label.length > 30) label = label.substring(0, 27) + "...";

              content += `<li style="margin-bottom: 3px;"><a href="${href}" target="_blank" style="color:#00f2ea; text-decoration:none;">${link}</a></li>`;
            });
            content += "</ul></div>";
          }

          addMessage(content);
        }
      })
      .catch((error) => {
        chatMessages.removeChild(loadingDiv);
        console.error("Error:", error);
        addMessage("Connection error. Please check your internet.");
      })
      .finally(() => {
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
      });
  }

  if (sendBtn && userInput) {
    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", function (e) {
      if (e.key === "Enter") sendMessage();
    });
  }

  // --- Resume Download Tracking ---
  window.downloadResume = function (event) {
    fetch("/track_download", {
      method: "POST",
    })
      .then((response) => {
        console.log("Download tracked");
      })
      .catch((error) => {
        console.error("Error tracking download:", error);
      });
  };

  // --- End Chat Logic ---
  const endChatBtn = document.getElementById("endChatBtnModal");
  if (endChatBtn) {
    endChatBtn.addEventListener("click", () => {
      if (
        confirm(
          "Are you sure you want to end the interview? I'll send a summary to Vijay.",
        )
      ) {
        // Gather history
        let history = "";
        const messages = chatMessages.querySelectorAll(".message");
        messages.forEach((msg) => {
          const isUser = msg.classList.contains("user-message");
          // Simple text extraction, might need refinement based on HTML structure
          const text = msg.innerText
            .replace("AI Assistant:", "")
            .replace("You:", "")
            .trim();
          if (text && text !== "Typing...") {
            history += `${isUser ? "User" : "AI"}: ${text}\n`;
          }
        });

        if (!history.trim()) {
          alert("No conversation to summarize yet.");
          return;
        }

        // Disable button
        endChatBtn.disabled = true;
        endChatBtn.innerText = "Ending...";

        fetch("/end_chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ history: history }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "success") {
              alert("Interview ended. Summary sent successfully!");
              addMessage("<em>Interview ended. Summary sent to Vijay.</em>");
            } else {
              alert("Failed to send summary.");
              endChatBtn.disabled = false;
              endChatBtn.innerText = "End Interview";
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("Error ending interview.");
            endChatBtn.disabled = false;
            endChatBtn.innerText = "End Interview";
          });
      }
    });
  }

  // --- Kaggle Badges Injection ---
  const badges = [
    { file: "Code_Tagger.svg", title: "Code Tagger", issuer: "Kaggle" },
    { file: "Code_Uploader.svg", title: "Code Uploader", issuer: "Kaggle" },
    {
      file: "Community_competitor.svg",
      title: "Community Competitor",
      issuer: "Kaggle",
    },
    {
      file: "Dataset_Contributor.svg",
      title: "Dataset Contributor",
      issuer: "Kaggle",
    },
    { file: "Github_Coder.svg", title: "GitHub Coder", issuer: "Kaggle" },
    { file: "Kaggle_Award.svg", title: "Kaggle Award", issuer: "Kaggle" },
    {
      file: "Notebook_Modeler.svg",
      title: "Notebook Modeler",
      issuer: "Kaggle",
    },
    { file: "Python_Coder.svg", title: "Python Coder", issuer: "Kaggle" },
    { file: "Stylish.svg", title: "Stylish Badge", issuer: "Kaggle" },
  ];

  const certContainer = document.getElementById("certSlider");
  if (certContainer) {
    badges.forEach((badge) => {
      const certDiv = document.createElement("div");
      certDiv.className = "cert-item";
      certDiv.innerHTML = `
                <img src="static/kaggle_badges/${badge.file}" alt="${badge.title}" class="cert-thumb">
                <h3>${badge.title}</h3>
                <p style="font-size:0.8rem; color:#a0a0a0;">${badge.issuer}</p>
            `;
      certContainer.appendChild(certDiv);
    });
  }

  // Slider Controls
  const slideLeft = document.getElementById("slideLeft");
  const slideRight = document.getElementById("slideRight");

  if (slideLeft && slideRight && certContainer) {
    slideLeft.addEventListener("click", () => {
      certContainer.scrollBy({ left: -300, behavior: "smooth" });
    });
    slideRight.addEventListener("click", () => {
      certContainer.scrollBy({ left: 300, behavior: "smooth" });
    });
  }
});
