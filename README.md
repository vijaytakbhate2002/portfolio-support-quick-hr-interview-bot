# 🤖 AI-Powered Portfolio & Resume Assistant for HR Interview

[![Python](https://img.shields.io/badge/Python-3.x-blue)]()
[![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey)]()
[![LangChain](https://img.shields.io/badge/LangChain-Integrated-orange)]()
[![ChromaDB](https://img.shields.io/badge/ChromaDB-RAG-purple)]()
[![Docker](https://img.shields.io/badge/Docker-Containerized-brightgreen)]()
[![GitHub Actions](https://img.shields.io/badge/CI-CD-blue)]()
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-informational)]()
[![AWS EC2](https://img.shields.io/badge/AWS-EC2-yellow)]()

---

## 🚀 Project Overview

**Portfolio Support Quick HR Interview Bot** is an intelligent **AI-powered assistant** that integrates seamlessly with a personal portfolio website to conduct **pre-screening HR interviews**. This system leverages cutting-edge **Retrieval-Augmented Generation (RAG)** technology powered by **LangChain** and **GPT-5-mini** to provide context-aware, accurate answers to HR questions.

### 🎯 Key Purpose

- **Automate HR Pre-Screening:** Enable recruiters to quickly assess candidate fit through an interactive AI chatbot
- **Save Time:** Conduct preliminary interviews 24/7 without human intervention
- **Contextual Answers:** Leverage RAG to provide accurate, sourced answers from GitHub repositories and knowledge bases
- **Track Quality:** Validate LLM responses with a dedicated judge model and MLflow monitoring
- **Portfolio Integration:** Embed the assistant directly into a personal portfolio website for seamless candidate engagement

🔗 **Live Demo:**  
👉 [http://ec2-52-21-78-219.compute-1.amazonaws.com:5000/](http://ec2-52-21-78-219.compute-1.amazonaws.com:5000/)

---

## 🏗️ Architecture & Workflow

### **System Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│              (Portfolio Website + Chatbot Modal)                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ↓
         ┌───────────────────────────────┐
         │   Flask Backend (app.py)      │
         │  - Route Handler: /chat       │
         │  - Email Notifications        │
         │  - Static File Server         │
         └───────────┬───────────────────┘
                     │
                     ↓
         ┌───────────────────────────────┐
         │  GithubAssistant (RAG Engine) │
         │  - Question Categorization    │
         │  - Vector DB Retrieval        │
         │  - LLM Response Generation    │
         └───────────┬───────────────────┘
                     │
         ┌───────────┴──────────┐
         ↓                      ↓
   ┌─────────────┐      ┌───────────────┐
   │  LangChain  │      │  ChromaDB     │
   │ + GPT-5-mini│      │  Vector Store │
   └─────────────┘      └───────────────┘
                              ↑
                              │
                    GitHub Data Processing
                    (Document Chunking)
                              │
         ┌────────────────────┴────────────────────┐
         │      MLflow Tracking (AWS EC2)          │
         │   - Response Validation Metrics         │
         │   - Model Performance Dashboard         │
         └─────────────────────────────────────────┘
```

### **1. Data Pipeline: GitHub Knowledge Base Creation**

The system automatically builds a searchable knowledge base from GitHub repositories:

```
GitHub Repos → [GithubScrapper] → README Files & Metadata
               ↓
         [Document Loader] → Documents
               ↓
    [Chunking Strategy] → Text Chunks (with Metadata)
               ↓
  [Embedding Model: all-MiniLM-L6-v2] → Vector Embeddings
               ↓
           [ChromaDB] → Vector Database (Persistent)
```

**Components:**

- **GitHub Scrapper:** Extracts repository README files and metadata (language, stars, topics, etc.)
- **Document Processing:**
  - Loads documents from saved README files
  - Splits large documents into semantic chunks (preserves context)
  - Attaches rich metadata (repo name, language, URL, etc.)
- **Embedding Generation:** Converts text chunks to 384-dimensional vectors using MiniLM model
- **Vector Storage:** Stores embeddings in ChromaDB with full-text search capabilities

**Key Files Involved:**

- `setup_knowledge_base.py` - Orchestrates the entire pipeline
- `rag_assisted_bots/ask_github/github_scrapper.py` - GitHub data extraction
- `rag_assisted_bots/ask_github/build_vectordb.py` - Vector database creation
- `vector_db/` - ChromaDB persistent storage

### **2. Conversation Flow: Question to Answer**

When a user submits a question, the system follows this intelligent pipeline:

```
User Question
     ↓
┌────────────────────────────────────────────┐
│ STEP 1: Question Categorization            │
│ - Uses LLM to classify question type       │
│ - Categories: project, experience,         │
│   education, personal, soft_skills, other  │
└────────────────┬─────────────────────────┘
                 ↓
┌────────────────────────────────────────────┐
│ STEP 2: Context Retrieval (RAG)            │
│ - Query ChromaDB for similar chunks        │
│ - Retrieve top-k most relevant docs        │
│ - Extract metadata (references)            │
└────────────────┬─────────────────────────┘
                 ↓
┌────────────────────────────────────────────┐
│ STEP 3: Response Generation                │
│ - Combine question + context               │
│ - Include conversation history             │
│ - Invoke GPT-5-mini with LLM chain         │
│ - Generate structured response             │
└────────────────┬─────────────────────────┘
                 ↓
         Response Object:
         {
           "response_message": "AI generated answer",
           "reference_links": ["URL1", "URL2"],
           "rag_relevance": "yes/no",
           "metadatas": [{"repo_name": "...", ...}]
         }
```

**Detailed Process:**

**Step 1: Question Categorization**

- Input: User question
- Uses `QuestionCategory` Pydantic model with structured output
- LLM classifies into: `project`, `experience`, `education`, `personal`, `soft_skills`, or `other`
- Example: "Tell me about your ML projects" → classified as "project"

**Step 2: Context Retrieval (RAG)**

- Embeds the user question using the same MiniLM model
- Searches ChromaDB for semantically similar document chunks
- Returns top-k documents with their metadata
- Deduplicates metadata to avoid redundant information
- Constructs retrieval context combining all relevant chunks

**Step 3: LLM Response Generation**

- Uses `conversation_model` with LangChain's chat interface
- Maintains conversation history for context-aware responses
- Includes:
  - System prompt defining the assistant's role
  - Retrieved context chunks
  - Conversation history (last 4 messages)
  - User's current question
- Generates response as `InterviewResponse` structured output:
  ```python
  {
    "response_message": str,      # Main answer text
    "reference_links": List[str], # Source URLs
    "confidence_score": float     # 0-1 confidence metric
  }
  ```

**Step 4: Response Formatting**

- Extracts unique metadata to provide reference sources
- Determines RAG relevance flag
- Formats JSON response for frontend consumption
- Returns metadata with repo names, topics, and documentation links

### **3. Response Validation Pipeline**

For quality assurance, responses can be validated:

```
Generated Response
     ↓
┌──────────────────────────────────────┐
│ Judge Model Evaluation (JudgeLLM)    │
│ - Accuracy scoring (0-10)            │
│ - Relevance scoring (0-10)           │
│ - Completeness scoring (0-10)        │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│ MLflow Tracking & Logging            │
│ - Store metrics in database          │
│ - Log parameters and tags            │
│ - Create experiments for testing     │
└──────────────────────────────────────┘
```

**Validation Components:**

- **JudgeLLM:** Evaluates response quality against ground truth
- **ValidationScores:** Pydantic model storing accuracy, relevance, completeness
- **MLflow Integration:** Logs all experiments to AWS EC2 tracking server
- **Automated Testing:** GitHub Actions run validation pipeline on commits

### **4. Monitoring & Analytics**

```
Real-time Metrics Collection
     ↓
┌─────────────────────────────────────┐
│ MLflow Tracking Server              │
│ (AWS EC2: 54-89-99-141)             │
│ - Experiment Dashboard              │
│ - Model Performance Metrics          │
│ - Response Quality Tracking          │
│ - Historical Analytics              │
└─────────────────────────────────────┘
     ↓
Available at: http://ec2-54-89-99-141.compute-1.amazonaws.com:5000/
```

**Tracked Metrics:**

- Response accuracy vs. ground truth
- Relevance of RAG context
- Model confidence scores
- Question categorization accuracy
- User satisfaction (if collected)

### **5. Frontend Integration**

The AI assistant is embedded in the portfolio with real-time chat:

```
Flask Backend Routes:
├── GET  /           → Return index.html (portfolio)
├── POST /chat       → Process user question, return AI response
├── POST /send_message → Handle "Get in Touch" form
├── POST /track_download → Log resume downloads
├── POST /end_chat   → Finalize chat & send summary email
└── GET  /static/<file> → Serve CSS, JS, images
```

**Frontend Features:**

- Chatbot modal with message history
- Real-time response streaming capability
- Reference link display
- Metadata/source information
- Email notifications on chat completion
- Resume download tracking

---

## 🧩 Tech Stack

| Layer                    | Technology                      | Purpose                                 |
| ------------------------ | ------------------------------- | --------------------------------------- |
| **LLM & RAG**            | LangChain, GPT-5-mini (OpenAI)  | Core AI reasoning and generation        |
| **Vector DB**            | ChromaDB, Sentence Transformers | Semantic search and document retrieval  |
| **Embeddings**           | all-MiniLM-L6-v2                | Text-to-vector encoding                 |
| **Web Framework**        | Flask 3.x                       | HTTP routing and request handling       |
| **Backend Language**     | Python 3.x                      | All server-side logic                   |
| **Frontend**             | HTML5, CSS3, JavaScript         | User interface and interactions         |
| **Monitoring**           | MLflow                          | Experiment tracking and metrics logging |
| **CI/CD**                | GitHub Actions                  | Automated testing and validation        |
| **Containerization**     | Docker                          | Application packaging and deployment    |
| **Cloud Infrastructure** | AWS EC2 (Ubuntu)                | Production hosting (24/7 runtime)       |
| **Email Service**        | SMTP (Gmail)                    | User notifications and alerts           |
| **Data Format**          | JSON                            | API communication                       |

---

## 📁 Project Structure

```
portfolio-support-quick-hr-interview-bot/
├── app.py                          # Flask application & routing
├── assistant.py                    # ResumeAssistant class (legacy)
├── main.py                         # Entry point
├── setup_knowledge_base.py         # Vector DB initialization
├── validation_pipeline.py          # Response quality validation
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker configuration
├── README.md                       # This file
│
├── src/                            # Core application modules
│   ├── __init__.py
│   ├── config.py                  # Configuration constants
│   ├── prompts.py                 # LLM prompt templates
│   ├── output_structure.py        # Pydantic response models
│   ├── reference_data.py          # Resume knowledge base
│   ├── conversation_management.py # Message history handling
│   ├── llm_judge.py              # Response evaluation model
│   └── __pycache__/
│
├── github_data/                    # GitHub scraping results
│   ├── metadata.json              # Repository metadata
│   ├── metadata_updated.json      # Processed metadata
│   ├── chunks_docs.json           # Document chunks info
│   └── readme_files/              # Downloaded README files
│
├── vector_db/                      # ChromaDB storage
│   ├── chroma.sqlite3            # Vector database file
│   └── <collection-id>/           # Vector collection data
│
├── static/                         # Frontend assets
│   ├── script.js                 # Chat functionality & events
│   ├── style.css                 # Styling
│   ├── articles_images/          # Article images
│   ├── kaggle_badges/            # Kaggle credential images
│   ├── kaggle_notebooks/         # Kaggle project files
│   └── profile_photos/           # Profile images
│
├── templates/                      # HTML templates
│   ├── index.html               # Main portfolio page
│   ├── hero_section.html        # Header/hero section
│   ├── about_section.html       # About me section
│   ├── experience_section.html  # Work experience
│   ├── project_section.html     # Projects showcase
│   ├── publications_section.html # Publications/articles
│   ├── cert_section.html        # Certifications
│   ├── contact_section.html     # Contact form
│   └── chatbot_modal.html       # AI chatbot interface
│
├── test_code/                      # Testing & debugging
│   ├── test_llm_workflow.py      # LLM pipeline testing
│   └── __pycache__/
│
└── __pycache__/                    # Python bytecode cache
```

---

## ⚙️ Setup & Installation

### **Prerequisites**

- Python 3.8+
- OpenAI API key (GPT-5-mini access)
- Gmail account (for email notifications)
- GitHub token (for repository scraping, optional)
- Docker (optional, for containerized deployment)

### **1. Clone Repository**

```bash
git clone https://github.com/vijaytakbhate2002/portfolio-support-quick-hr-interview-bot.git
cd portfolio-support-quick-hr-interview-bot
```

### **2. Create Virtual Environment**

```bash
# Using Python venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Create `.env` Configuration File**

Create a `.env` file in the root directory with the following variables:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-actual-api-key-here

# Email Configuration (Gmail)
EMAIL_USER=your-email@gmail.com
APP_PASS=your-gmail-app-specific-password

# GitHub Configuration (Optional, for scraping)
TOKEN_GITHUB=ghp_your-github-token-here

# Session Configuration
SESSION_SECRET=your-random-secret-key
```

**Note:** For Gmail, use an **App Password** (not your regular password):

1. Enable 2-Factor Authentication on your Google Account
2. Generate an App Password at https://myaccount.google.com/apppasswords
3. Select "Mail" and "Windows Computer" (or your OS)
4. Copy the generated 16-character password to `APP_PASS`

### **5. Initialize Knowledge Base**

Before running the app first time, build the vector database:

```bash
python setup_knowledge_base.py
```

This will:

- Scrape GitHub repositories
- Download README files
- Create vector embeddings
- Store in ChromaDB
- Generate metadata files

### **6. Run Locally**

```bash
python app.py
```

The application will start at:
👉 `http://localhost:5000`

Visit this URL in your browser to see the portfolio and interact with the chatbot.

---

## 🐳 Docker Deployment

### **Build Docker Image Locally**

```bash
docker build -t your-username/portfolio-chatbot:latest .
```

### **Run Docker Container**

```bash
docker run -d \
  --name portfolio-bot \
  -p 5000:5000 \
  -e OPENAI_API_KEY=sk-your-key \
  -e EMAIL_USER=your-email@gmail.com \
  -e APP_PASS=your-app-password \
  -e SESSION_SECRET=your-secret \
  -v $(pwd)/vector_db:/app/vector_db \
  your-username/portfolio-chatbot:latest
```

### **Pull Pre-built Image**

```bash
docker pull vijaytakbhate1/portfolio-support-quick-hr-interview-bot:latest

docker run -d \
  -p 5000:5000 \
  -e OPENAI_API_KEY=sk-... \
  -e EMAIL_USER=... \
  -e APP_PASS=... \
  vijaytakbhate1/portfolio-support-quick-hr-interview-bot:latest
```

### **Docker Compose (Optional)**

Create a `docker-compose.yml` for easier orchestration:

```yaml
version: "3.8"

services:
  portfolio-bot:
    image: vijaytakbhate1/portfolio-support-quick-hr-interview-bot:latest
    ports:
      - "5000:5000"
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      EMAIL_USER: ${EMAIL_USER}
      APP_PASS: ${APP_PASS}
      SESSION_SECRET: ${SESSION_SECRET}
    volumes:
      - ./vector_db:/app/vector_db
    restart: unless-stopped
```

---

## 🔌 API Endpoints

### **1. Chat Endpoint** (Core AI Interaction)

**Request:**

```bash
POST /chat
Content-Type: application/json

{
  "message": "Tell me about your machine learning projects"
}
```

**Response:**

```json
{
  "response_message": "I have worked on several ML projects including...",
  "reference_links": ["https://github.com/vijaytakbhate2002/ml-project-1"],
  "rag_relevance": "--on",
  "metadatas": [
    {
      "repo_name": "vijaytakbhate2002/ml-project-1",
      "topics": ["machine-learning", "python"],
      "language": "Python",
      "stars": 15
    }
  ]
}
```

**Status Codes:**

- `200 OK` - Success
- `400 Bad Request` - No message provided
- `500 Internal Server Error` - Processing error

---

### **2. Portfolio Index** (Main Page)

**Request:**

```bash
GET /
```

**Response:**

- Returns `templates/index.html`
- Contains full portfolio + embedded chatbot modal

---

### **3. Contact Form** (Send Message)

**Request:**

```bash
POST /send_message
Content-Type: application/x-www-form-urlencoded

name=John Doe&email=john@example.com&message=Great portfolio!
```

**Response:**

- Sends email notification
- Redirects to home page with success/error flash message

---

### **4. Resume Download Tracking**

**Request:**

```bash
POST /track_download
```

**Response:**

```json
{
  "status": "success"
}
```

- Logs download event
- Sends notification email

---

### **5. End Chat Session**

**Request:**

```bash
POST /end_chat
Content-Type: application/json

{
  "history": "Q: Are you interested in ML?\nA: Yes, I'm passionate about..."
}
```

**Response:**

```json
{
  "status": "success",
  "summary": "Conversation ended. Summary sent."
}
```

- Sends conversation summary via email
- Logs session metrics

---

## 🧪 Testing & Validation

### **Run Validation Pipeline**

The project includes an automated validation system using a judge model:

```bash
python validation_pipeline.py
```

This will:

1. Run predefined test questions
2. Generate responses using the assistant
3. Evaluate response quality with JudgeLLM
4. Log metrics to MLflow
5. Display validation scores

**Validation Metrics:**

- **Accuracy:** How correct is the answer? (0-10)
- **Relevance:** How relevant to the question? (0-10)
- **Completeness:** Does it cover all aspects? (0-10)

### **GitHub Actions CI/CD**

Automated testing on every commit:

```yaml
# .github/workflows/test.yml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run validation pipeline
        run: |
          pip install -r requirements.txt
          python validation_pipeline.py
```

---

## 📊 Configuration

### **Main Configuration** (`src/config.py`)

```python
GPT_MODEL_NAME = 'gpt-5-mini'  # LLM model to use
TEMPERATURE = 0.7              # Response creativity (0-1)
MLFLOW_TRACKING_URI = "http://ec2-54-89-99-141.compute-1.amazonaws.com:5000/"
```

### **RAG Configuration** (`app.py`)

```python
VECTORDB_PATH = "./vector_db"        # ChromaDB storage location
COLLECTION_NAME = "my_embeddings"    # Vector collection name
```

### **Knowledge Base** (`setup_knowledge_base.py`)

```python
USERNAME = 'vijaytakbhate2002'        # GitHub username
EMBEDDING_MODEL = "all-MiniLM-L6-v2" # Embedding model
COLLECTION_NAME = "my_embeddings"
```

### **Email Configuration** (`.env`)

```env
EMAIL_USER=your-email@gmail.com
APP_PASS=your-app-password
```

---

## 🎯 Key Features

### ✨ **Smart Question Categorization**

- Automatically classifies HR questions into relevant categories
- Ensures appropriate context retrieval from knowledge base
- Improves answer relevance and accuracy

### 📚 **Retrieval-Augmented Generation (RAG)**

- Pulls context from GitHub repositories and markdown files
- Provides cited answers with source references
- Ensures factually accurate responses grounded in actual projects

### 💬 **Conversational Memory**

- Maintains conversation history for context-aware responses
- Supports multi-turn interactions
- Remembers previous answers in the same session

### ✅ **Quality Validation**

- Dedicated judge model evaluates response quality
- Automated testing pipeline with GitHub Actions
- MLflow tracking for performance monitoring

### 📧 **Email Integration**

- Sends notifications on events (downloads, messages, chat summaries)
- SMTP support for Gmail integration
- Customizable email templates

### 🔒 **Environment-based Configuration**

- Secure API key management via `.env`
- No hardcoded secrets in codebase
- Production-ready security practices

### ⚡ **Performance Optimized**

- Vector database for fast semantic search
- Efficient document chunking strategy
- Minimal API call latency

---

## 📈 Monitoring & Analytics

### **MLflow Dashboard**

Access real-time metrics at:
👉 [http://ec2-54-89-99-141.compute-1.amazonaws.com:5000/](http://ec2-54-89-99-141.compute-1.amazonaws.com:5000/)

**Available Metrics:**

- Response accuracy and relevance
- Model performance over time
- Experiment history and comparison
- Parameter tracking
- Custom metrics and tags

### **Local MLflow Tracking**

You can also run MLflow locally:

```bash
# Install MLflow (included in requirements.txt)
mlflow ui

# Access at http://localhost:5000
```

---

## 🚀 Deployment on AWS EC2

### **1. EC2 Instance Setup**

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io -y
sudo usermod -aG docker ubuntu
```

### **2. Deploy Application**

```bash
# Pull Docker image
docker pull vijaytakbhate1/portfolio-support-quick-hr-interview-bot:latest

# Run container with persistent storage
docker run -d \
  --name portfolio-bot \
  -p 5000:5000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e EMAIL_USER=$EMAIL_USER \
  -e APP_PASS=$APP_PASS \
  -v /home/ubuntu/vector_db:/app/vector_db \
  -v /home/ubuntu/logs:/app/logs \
  --restart unless-stopped \
  vijaytakbhate1/portfolio-support-quick-hr-interview-bot:latest
```

### **3. Enable HTTPS with Nginx + Let's Encrypt**

```bash
# Install Nginx
sudo apt install nginx -y

# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Setup SSL certificate
sudo certbot --nginx -d yourdomain.com

# Nginx config to proxy to Flask
# /etc/nginx/sites-available/default
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **4. Monitor Application**

```bash
# View logs
docker logs -f portfolio-bot

# Check resource usage
docker stats portfolio-bot

# Monitor with top
top
```

---

## 🛠️ Development Guide

### **Adding New Features**

1. **New Chat Functionality:**
   - Add new route in `app.py`
   - Implement logic using `GithubAssistant.chat_with_model()`
   - Update frontend in `templates/`

2. **Customize Knowledge Base:**
   - Edit `setup_knowledge_base.py`
   - Modify GitHub scraping parameters
   - Adjust document chunking strategy
   - Rebuild vector database

3. **Fine-tune Response Quality:**
   - Adjust `TEMPERATURE` in `src/config.py`
   - Modify prompts in `src/prompts.py`
   - Update validation criteria in `src/llm_judge.py`

4. **Extend Frontend:**
   - Edit HTML templates in `templates/`
   - Update styles in `static/style.css`
   - Add interactivity in `static/script.js`

### **Best Practices**

- Always test changes locally before deployment
- Run validation pipeline to check quality
- Use `.env` for sensitive configuration
- Document API changes and new parameters
- Version Docker images appropriately
- Monitor MLflow for performance degradation

---

## 🌟 Future Enhancements

- 📊 **Real-time Analytics Dashboard:** Integrate Grafana + Prometheus for server metrics visualization
- 🧠 **Extended Context Memory:** Implement multi-session conversation persistence
- 🔄 **Fine-tuned Models:** Train custom models on your specific domain
- 🔐 **Advanced Authentication:** Add user login and conversation history storage
- 📱 **Mobile App:** Native mobile application for iOS/Android
- 🌐 **Multi-language Support:** Translate responses to multiple languages
- 🎯 **Skill Assessment:** Score candidate responses for specific competencies
- 📈 **Predictive Analytics:** Estimate interview success rate based on responses
- 🔗 **Slack Integration:** Receive notifications in Slack
- 🤝 **Collaborative Features:** Share interview summaries with team members

---

## 🐛 Troubleshooting

### **Issue: Empty Response from AI**

```
Solution:
1. Check OPENAI_API_KEY is valid
2. Verify vector database exists: vector_db/chroma.sqlite3
3. Run setup_knowledge_base.py to rebuild database
4. Check API quota on OpenAI dashboard
```

### **Issue: Email Not Sending**

```
Solution:
1. Verify EMAIL_USER and APP_PASS in .env
2. Ensure Gmail "Allow less secure apps" is enabled (if applicable)
3. Use Gmail App Password (not regular password)
4. Check SMTP config: smtp.gmail.com:587
5. Verify firewall allows SMTP connections (port 587)
```

### **Issue: Slow Response Time**

```
Solution:
1. Reduce number of documents returned from RAG (k parameter)
2. Decrease context window size
3. Use faster embedding model
4. Increase server resources (EC2 instance type)
5. Enable response caching
```

### **Issue: Docker Container Not Starting**

```
Solution:
1. Check logs: docker logs container-name
2. Verify environment variables are set
3. Ensure ports are not in use: lsof -i :5000
4. Check Docker image exists: docker image ls
5. Rebuild image: docker build -t your-image .
```

---

## 📬 Support & Contact

😊 **Have Questions or Feedback?**

💼 **Portfolio:** [http://ec2-52-21-78-219.compute-1.amazonaws.com:5000/](http://ec2-52-21-78-219.compute-1.amazonaws.com:5000/)  
📧 **Email:** [vijaytakbhate20@gmail.com](mailto:vijaytakbhate20@gmail.com)  
🐙 **GitHub:** [@vijaytakbhate2002](https://github.com/vijaytakbhate2002)  
💼 **LinkedIn:** [Vijay Takbhate](https://www.linkedin.com/in/vijay-takbhate-b9231a236/)  
🔗 **Portfolio Email Contact:** [vijaytakbhateportfolio@gmail.com](mailto:vijaytakbhateportfolio@gmail.com)

---

## 📜 License

This project is open-source and available for educational and portfolio purposes.

---

## 🙌 Acknowledgments

- **LangChain Community:** For excellent RAG and LLM orchestration tools
- **OpenAI:** For GPT-5-mini model and API
- **Chroma:** For lightweight vector database solution
- **Flask Community:** For lightweight web framework
- **MLflow Community:** For experiment tracking and monitoring

---

> 💡 _"AI won't replace recruiters — but recruiters who use AI will replace those who don't."_
>
> ~ Vijay Takbhate

---

**Last Updated:** March 1, 2026  
**Version:** 2.0 (Enhanced Documentation & Features)
