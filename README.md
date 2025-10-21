
# 🤖 AI-Powered Resume Assistant for HR

## 🚀 Project Overview
This project is an **AI chatbot** designed to assist HR professionals in interacting with my resume and conducting **quick virtual interviews**.  
It contains all my professional details — contact info, projects, experience, education, and soft skills — making it a **pre-screening tool** for HR to evaluate my fit for **Data Science** or **MLOps roles** before direct contact.

---

## 🛠 Key Features
- **Instant Question Categorization:** Classifies HR questions into:
```

["project", "personal", "experience", "education", "soft_skills", "others"]

````
- **Intelligent Answer Generation:** Uses GPT-5-mini to generate structured responses from my resume:
```python
response_message: str  # AI's answer
list_items: Optional[Union[str, list[str]]] = None  # Additional details if needed
reference_links: Optional[Union[str, list[str]]] = None  # Related references
````

* **Automated Response Validation:** Third LLM acts as a judge to score responses on:

  * ✅ Relevancy
  * 🛡 Faithfulness
  * 🎯 Correctness
    Scores are tracked in **MLflow** on an **AWS EC2 instance** for remote monitoring.

---

## 🔄 Workflow

1. **HR initiates conversation** with a greeting or a question.
2. **Question Classification:** First LLM identifies the category.
3. **Response Generation:** Second LLM (GPT-5-mini) crafts a structured response.
4. **Validation:** Third LLM evaluates the response and generates scoring metrics.
5. **Score Tracking:** MLflow stores scores for each interaction, enabling **analytics and monitoring**.

---

## ✅ Current Status

* Multi-LLM architecture implemented
* Response scoring & MLflow tracking functional
* AWS EC2 setup complete for remote monitoring

---

## 🌟 Future Plans

* Integrate **Grafana & Prometheus** for real-time monitoring 📊
* Build a **Docker image** for easy sharing 🐳
* Create a personal **portfolio website** 🌐
* Deploy the application fully on **AWS** ☁️

---

## 🧰 Tech Stack

* **Python**
* **GPT-5-mini** (via LangChain)
* **MLflow**, **AWS EC2**
* (Planned) **Grafana**, **Prometheus**, **Docker**

---

## 🎯 Why This Project?

This project demonstrates a **smart, automated way for HR to pre-screen candidates**, saving time and providing **accurate insights** into skills, experience, and projects — all **before a live interview**.

---
