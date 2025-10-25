
# 🤖 AI-Powered Portfolio & Resume Assistant for HR

[![Python](https://img.shields.io/badge/Python-3.x-blue)]()
[![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)]()
[![LangChain](https://img.shields.io/badge/LangChain-Integrated-orange)]()
[![Docker](https://img.shields.io/badge/Docker-ready-brightgreen)]()
[![GitHub Actions](https://img.shields.io/badge/CI-CD-blue)]()
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-informational)]()
[![AWS EC2](https://img.shields.io/badge/AWS-EC2-yellow)]()

---

## 🚀 Project Overview

This project is an **AI-powered interactive portfolio** integrated with a **smart HR assistant**.  
It allows HR professionals to **interview me virtually** — the AI can understand, categorize, and answer HR questions directly from my resume using **LangChain + GPT-5-mini**.

The system is designed to **save recruiters’ time** by conducting quick **pre-screening interviews**, analyzing answers for accuracy and relevance, and providing metrics for each response.

🔗 **Live Demo:**  
👉 [http://ec2-54-167-49-203.compute-1.amazonaws.com:5000/](http://ec2-54-167-49-203.compute-1.amazonaws.com:5000/)

---

## 🧠 Workflow & Architecture

1. **Question Categorization (LLM 1)**  
   - The first LLM predicts which part of the resume is relevant:  
     ```
     ["project", "experience", "personal", "education", "soft_skills", "others"]
     ```

2. **Context-Aware Answering (LLM 2)**  
   - Based on the predicted category, the assistant extracts **only that section** of the resume and combines it with the HR’s question.
   - This **smart prompting** reduces token usage and cost while maintaining contextually correct answers.

3. **Response Validation (LLM 3)**  
   - A third LLM validates each generated answer using **MLflow** metrics:
     - ✅ **Relevancy**
     - 🛡 **Faithfulness**
     - 🎯 **Correctness**

4. **Tracking & Monitoring**
   - All metrics are logged in **MLflow**, hosted on an **AWS EC2 instance** for live tracking and analytics.

5. **Portfolio Integration**
   - The AI chatbot is embedded directly into my personal **one-page portfolio website**, allowing HR to chat and review my details seamlessly.

6. **Automation & Deployment**
   - Used **GitHub Actions** for LLM testing automation.
   - Dockerized the app for easy deployment and portability.
   - Hosted on **AWS EC2**, running continuously 24×7.

---

## 🧩 Tech Stack

| Layer | Technologies Used |
|-------|-------------------|
| 💬 AI Assistant | LangChain, GPT-5-mini |
| 🧠 Backend | Python, Flask |
| 📈 Tracking | MLflow, AWS EC2 |
| 🧰 CI/CD | GitHub Actions |
| 🐳 Containerization | Docker |
| ☁️ Deployment | AWS EC2 (Ubuntu) |
| 🔒 Communication | SMTP (Email integration) |

---

## ⚙️ Setup Instructions

### **1️⃣ Clone Repository**
```bash
git clone https://github.com/vijaytakbhate2002/portfolio-support-quick-hr-interview-bot.git
cd portfolio-support-quick-hr-interview-bot
````

### **2️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3️⃣ Create `.env` File**

Create a `.env` file in the root directory and add:

```
OPENAI_API_KEY=sk-dummyapikey
EMAIL_USER=vijaytakbhateportfolio@gmail.com
APP_PASS=dummypassword
```

### **4️⃣ Run the Application**

```bash
python app.py
```

Visit:
👉 `http://localhost:5000`

---

## 🐳 Run with Docker

### **Pull the Image**

```bash
docker pull vijaytakbhate1/portfolio-support-quick-hr-interview-bot:latest
```

### **Run the Container**

```bash
docker run -d \
  -p 5000:5000 \
  -e OPENAI_API_KEY=sk-dummyapikey \
  -e EMAIL_USER=vijaytakbhateportfolio@gmail.com \
  -e APP_PASS=dummypassword \
  vijaytakbhate1/portfolio-support-quick-hr-interview-bot:latest
```

Visit your app at:
👉 `http://localhost:5000`

---

## 🧰 GitHub Actions

Integrated **GitHub Actions** to automatically test LLM responses and maintain model accuracy before deployment.

---

## 🌟 Future Plans

* Integrate **Grafana & Prometheus** for real-time metrics 📊
* Develop a **dashboard for HR analytics**
* Expand AI memory for longer, context-aware interviews 🧠
* Enhance Docker orchestration with **Kubernetes**
* Deploy a multi-service pipeline via **Kubeflow**

---

## 🎥 Application Demo

<p align="center">
  <img src="https://github.com/user-attachments/assets/b0b9b959-a181-404f-9c85-bfc13d0ed817" width="49%" />
  <img src="https://github.com/user-attachments/assets/b387f6be-3b1c-47c0-95ab-96eb9e33c5da" width="49%" />
</p>

---

## 🙌 About This Project

This AI-powered assistant showcases how **AI can simplify HR workflows** — enabling recruiters to understand a candidate’s fit before an actual interview.

It’s more than just a chatbot — it’s an intelligent **AI-driven hiring assistant** integrated into a personal portfolio.

---

## 📬 Get in Touch

💼 **Portfolio:** [Visit My Portfolio](http://ec2-54-167-49-203.compute-1.amazonaws.com:5000/)
📧 **Email:** [vijaytakbhateportfolio@gmail.com](mailto:vijaytakbhate20@gmail.com)
🐙 **GitHub:** [vijaytakbhate2002](https://github.com/vijaytakbhate2002)
🐙 **LinkedIn:** [My Linkedin](https://www.linkedin.com/in/vijay-takbhate-b9231a236/)

---
## 🌟 Future Plans

- 📊 **Integrate Prometheus & Grafana** for real-time server performance monitoring and visualization.  
- 🧠 Expand AI capabilities for **longer, context-aware conversations** across multiple HR sessions.  
- ☁️ Implement **Kubernetes (K8s)** orchestration for better scalability and fault tolerance.  
- 🔒 Strengthen application security with HTTPS, authentication layers, and environment isolation.  

---

> 💡 *“AI won’t replace recruiters — but recruiters who use AI will replace those who don’t.”*
> — Vijay Takbhate




