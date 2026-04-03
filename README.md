# 🤖 AI-Powered Portfolio & Resume Assistant for HR Interview

[![Python](https://img.shields.io/badge/Python-3.x-blue)]()
[![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey)]()
[![LangChain](https://img.shields.io/badge/LangChain-Integrated-orange)]()
[![ChromaDB](https://img.shields.io/badge/ChromaDB-RAG-purple)]()
[![Docker](https://img.shields.io/badge/Docker-Containerized-brightgreen)]()
[![GitHub Actions](https://img.shields.io/badge/CI-CD-blue)]()
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
         │  - Vector DB Retrieval        │
         │  - Similarity Validation      │
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

- **GitHub Scrapper:** Extracts repository README files and comprehensive metadata from GitHub API
- **Metadata Enrichment:** Each document chunk includes:
  - Repository information (URL, name, description, language)
  - Timestamps (created, updated, pushed dates)
  - Repository size and privacy settings
  - Direct download URLs for seamless GitHub access
- **Document Processing:**
  - Loads documents from saved README files
  - Splits large documents into semantic chunks (preserves context)
  - Attaches rich metadata to each chunk for direct GitHub exploration
- **Embedding Generation:** Converts text chunks to 384-dimensional vectors using MiniLM model
- **Vector Storage:** Stores embeddings in ChromaDB with full-text search and metadata filtering

**Key Files Involved:**

- `setup_knowledge_base.py` - Orchestrates the entire pipeline
- `rag_assisted_bots/ask_github/github_scrapper.py` - GitHub data extraction
- `rag_assisted_bots/ask_github/build_vectordb.py` - Vector database creation
- `vector_db/` - ChromaDB persistent storage

### **2. Metadata Structure**

Each document chunk in the vector database is enriched with comprehensive GitHub metadata:

```json
{
  "download_url": "https://raw.githubusercontent.com/vijaytakbhate2002/basic-personality-detection-project-with-dvc-mlflow-dagshub-git/main/README.md",
  "repository_url": "https://github.com/vijaytakbhate2002/basic-personality-detection-project-with-dvc-mlflow-dagshub-git",
  "repo_name": "basic-personality-detection-project-with-dvc-mlflow-dagshub-git",
  "full_name": "vijaytakbhate2002/basic-personality-detection-project-with-dvc-mlflow-dagshub-git",
  "description": "This project helped me understand the need of data version control (dvc) plus code version control (git) and how mlflow helps us to work in remote community",
  "language": "Python",
  "size": 3544,
  "created_at": "2025-06-07T11:16:10Z",
  "updated_at": "2025-06-07T12:01:29Z",
  "pushed_at": "2025-06-07T12:01:26Z",
  "private": false
}
```

**Metadata Purpose:**

- Users can directly visit GitHub projects from the chat interface
- Download and explore project READMEs directly
- Understand project context and timelines
- Access source code repositories instantly

### **3. Conversation Flow: Question to Answer**

When a user submits a question, the system follows this intelligent RAG pipeline:

```
User Question
     ↓
┌────────────────────────────────────────────────────┐
│ STEP 1: Semantic Search & Retrieval (RAG)          │
│ - Embed question using MiniLM model               │
│ - Query ChromaDB for similar chunks               │
│ - Retrieve top-k most relevant docs with metadata │
│ - Return search results with full metadata        │
└────────────────┬─────────────────────────────────┘
                 ↓
┌────────────────────────────────────────────────────┐
│ STEP 2: Similarity Validation (LLM)               │
│ - LLM evaluates: Is question related to chunks?  │
│ - Check if retrieved content addresses question   │
│ - Determine confidence of RAG relevance           │
└────────────────┬──────────────┬───────────────────┘
                 │              │
        YES (Similar)    NO (Dissimilar)
                 │              │
                 ↓              ↓
    ┌─────────────────┐  ┌──────────────────────┐
    │ STEP 3A:        │  │ STEP 3B:             │
    │ Generate Answer │  │ Ask for Clarification│
    │                 │  │ - Suggest keywords   │
    │ - Use LLM to    │  │ - Request refinement │
    │   generate      │  │ - Guide user         │
    │   response      │  └──────────────────────┘
    │ - Include       │           ↓
    │   metadata      │  User Provides Refined
    │ - Format refs   │  Question with more
    └────────┬────────┘  details/skills
             │                │
             │                └────→ Return to STEP 1
             ↓
    ┌─────────────────────────────────────┐
    │ STEP 4: Format & Send Response      │
    │ - response_message: AI-generated ans│
    │ - reference_links: GitHub URLs      │
    │ - rag_relevance: "yes" or "no"      │
    │ - metadatas: Full GitHub metadata   │
    │ - Return JSON to frontend           │
    └─────────────────────────────────────┘
```

**Detailed Process:**

**Step 1: Semantic Search & Retrieval (RAG)**

- Embeds the user question using the same MiniLM model (384-dimensional vectors)
- Searches ChromaDB for semantically similar document chunks
- Returns top-k most relevant documents with their complete metadata
- Each result includes GitHub repo info, URLs, timestamps, and description
- Constructs retrieval context combining all relevant chunks

**Step 2: Similarity Validation**

- LLM evaluates if the retrieved content actually addresses the question
- Checks semantic coherence between the question and retrieved chunks
- Determines if the RAG context is sufficient and relevant
- Two possible outcomes based on validation:
  - **YES (Similar):** Proceed to answer generation using the retrieved facts
  - **NO (Dissimilar):** Ask user to refine their question with more details

**Step 3A: Answer Generation (If Similar)**

- Uses LangChain's chat interface with structured output
- Maintains conversation history for context-aware multi-turn interactions
- Includes:
  - System prompt defining the assistant's role and behavior
  - Retrieved context chunks with full metadata
  - Conversation history (previous messages in session)
  - User's current question
- Generates response grounded in the factual retrieved content
- Response structure:
  ```python
  {
    "response_message": str,      # AI-generated answer based on facts
    "reference_links": List[str], # Direct GitHub URLs from metadata
    "rag_relevance": "yes",        # Validation passed
    "metadatas": List[dict]       # Full GitHub metadata for traceability
  }
  ```

**Step 3B: Clarification Request (If Dissimilar)**

- LLM identifies why the retrieved content doesn't match the question
- Asks user for more specific details or context
- Suggests relevant skills, keywords, or refinements
- Guides user on how to reformulate their question
- Response format:
  ```python
  {
    "response_message": "Could you please provide more details about...",
    "rag_relevance": "no",
    "suggestions": ["skill1", "skill2", ...],
    "clarification_hints": ["Try mentioning...", "Include details about..."]
  }
  ```
- User can then ask a refined question with additional context (loops back to Step 1)

**Step 4: Response Formatting & Delivery**

- Deduplicates metadata to avoid sending redundant GitHub references
- Extracts direct repository URLs for user exploration
- Formats complete JSON response for frontend
- Returns full GitHub metadata with each source chunk
- Enables users to:
  - Click links to visit GitHub repositories directly
  - Download README files from provided download URLs
  - Understand project context from descriptions and timestamps
  - Access source code for deeper exploration

### **4. Response Validation Pipeline**

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

### **6. Monitoring & Analytics**

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

## 📊 Metadata & GitHub Integration

### **Metadata Collection During Vector DB Creation**

When the vector database is built via `setup_knowledge_base.py`, the system enriches each document chunk with comprehensive GitHub metadata:

```
GitHub API Query
     ↓
Extract Repository Information:
├── Basic Info: name, full_name, description
├── URLs: repository_url, download_url (for README)
├── Timestamps: created_at, updated_at, pushed_at
├── Technical Details: language, size, private status
└── Additional Stats: stars, forks, watchers (if available)
     ↓
Attach Metadata to Each Chunk
     ↓
Store in ChromaDB with Embeddings
```

### **Metadata Fields Explained**

| Field            | Purpose                      | Example                                                           |
| ---------------- | ---------------------------- | ----------------------------------------------------------------- |
| `repo_name`      | Repository identifier        | `basic-personality-detection-project-with-dvc-mlflow-dagshub-git` |
| `full_name`      | GitHub path                  | `vijaytakbhate2002/basic-personality-detection-...`               |
| `repository_url` | Direct GitHub link           | `https://github.com/vijaytakbhate2002/...`                        |
| `download_url`   | Raw README file URL          | `https://raw.githubusercontent.com/.../main/README.md`            |
| `description`    | Project purpose              | `"This project helped me understand DVC + MLflow..."`             |
| `language`       | Primary programming language | `Python`, `JavaScript`, etc.                                      |
| `size`           | Repository size in KB        | `3544`                                                            |
| `created_at`     | Repository creation date     | `2025-06-07T11:16:10Z`                                            |
| `updated_at`     | Last update date             | `2025-06-07T12:01:29Z`                                            |
| `pushed_at`      | Last push/commit date        | `2025-06-07T12:01:26Z`                                            |
| `private`        | Access status                | `false` (public) or `true` (private)                              |

### **Metadata Usage in Chat**

When the AI responds to a user query:

1. **Retrieved chunks include metadata** - Each document chunk returned by vector search includes all GitHub metadata
2. **Front-end presentation** - Metadata is passed to the frontend for display:
   - Users see clickable GitHub repository links
   - Can download README files directly
   - Access project source code
   - Understand project context and recent activity
3. **Quality assurance** - Metadata enables users to:
   - Verify response accuracy by exploring source projects
   - Access live code and implementation details
   - Provide feedback on relevance

### **Example: Complete Chat Flow with Metadata**

```
User Question: "Tell me about your ML projects"
                ↓
Vector Search returns top-k chunks with metadata
                ↓
LLM validates similarity: "YES - chunks are relevant"
                ↓
LLM generates answer using facts from chunks
                ↓
System formats response:
{
  "response_message": "I have worked on ...",
  "reference_links": [
    "https://raw.githubusercontent.com/vijaytakbhate2002/.../README.md",
    "https://github.com/vijaytakbhate2002/..."
  ],
  "rag_relevance": "--on",
  "metadatas": [                    ← Full GitHub metadata
    {
      "repo_name": "...",
      "repository_url": "...",
      "download_url": "...",        ← User can click to explore
      "description": "...",
      "language": "Python",
      "created_at": "...",
      ...
    }
  ]
}
                ↓
Frontend displays:
- Formatted answer text
- Clickable GitHub repository links
- Project descriptions and metadata
- Direct access to README and source code
```

---

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

## API Endpoints

### **1. Chat Endpoint** (Core AI Interaction)

**Request:**

```bash
POST /chat
Content-Type: application/json

{
  "message": "Tell me about your machine learning projects"
}
```

**Response (When Similar - RAG Activated):**

```json
{
  "response_message": "I have worked on several ML projects including:\n1. Medical Insurance Cost Prediction - Using regression models to predict insurance costs based on various factors\n2. Personality Detection - DVC + MLflow based project for data versioning and experiment tracking",
  "reference_links": [
    "https://raw.githubusercontent.com/vijaytakbhate2002/basic-personality-detection-project-with-dvc-mlflow-dagshub-git/main/README.md",
    "https://github.com/vijaytakbhate2002/basic-personality-detection-project-with-dvc-mlflow-dagshub-git"
  ],
  "rag_relevance": "--on",
  "metadatas": [
    {
      "download_url": "https://raw.githubusercontent.com/vijaytakbhate2002/basic-personality-detection-project-with-dvc-mlflow-dagshub-git/main/README.md",
      "repository_url": "https://github.com/vijaytakbhate2002/basic-personality-detection-project-with-dvc-mlflow-dagshub-git",
      "repo_name": "basic-personality-detection-project-with-dvc-mlflow-dagshub-git",
      "full_name": "vijaytakbhate2002/basic-personality-detection-project-with-dvc-mlflow-dagshub-git",
      "description": "This project helped me understand the need of data version control (dvc) plus code version control (git) and how mlflow helps us to work in remote community",
      "language": "Python",
      "size": 3544,
      "created_at": "2025-06-07T11:16:10Z",
      "updated_at": "2025-06-07T12:01:29Z",
      "pushed_at": "2025-06-07T12:01:26Z",
      "private": false
    }
  ]
}
```

**Response (When Dissimilar - RAG Validation Failed):**

```json
{
  "response_message": "I don't have specific information about that in my knowledge base. Could you please provide more details? For example:\n- Are you asking about a specific technology or skill?\n- Which area interests you (ML, web development, data engineering)?\n- Do you want to know about projects using particular tools or frameworks?",
  "reference_links": [],
  "rag_relevance": "--off",
  "metadatas": [],
  "clarification_hints": [
    "Try mentioning specific technologies (Python, TensorFlow, PyTorch)",
    "Include project types (classification, regression, NLP)",
    "Add context about application domain (healthcare, finance, etc.)"
  ]
}
```

**Status Codes:**

- `200 OK` - Success (both similar and dissimilar cases)
- `400 Bad Request` - No message provided
- `500 Internal Server Error` - Processing error in RAG pipeline

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
GPT_MODEL_NAME = 'gpt-5-mini'              # LLM model for generation and validation
TEMPERATURE = 0.7                          # Response creativity (0-1, lower = more factual)
```

### **RAG Configuration** (`app.py`)

```python
VECTORDB_PATH = "./vector_db"              # ChromaDB storage location
COLLECTION_NAME = "my_embeddings"          # Vector collection name
```

These settings control:

- Vector storage and retrieval
- Similarity validation thresholds
- Metadata formatting and delivery

### **Knowledge Base Setup** (`setup_knowledge_base.py`)

```python
USERNAME = 'vijaytakbhate2002'             # GitHub username for scraping
EMBEDDING_MODEL = "all-MiniLM-L6-v2"       # Sentence transformer model
COLLECTION_NAME = "my_embeddings"          # ChromaDB collection
VECTORDB_PATH = "./vector_db"              # Vector store location
```

This script:

- Scrapes GitHub repositories
- Extracts metadata from GitHub API
- Creates semantic embeddings
- Builds ChromaDB vector database
- Generates metadata JSON files

### **Email & Notifications** (`.env`)

```env
EMAIL_USER=your-email@gmail.com            # Sender email address
APP_PASS=your-app-password                 # Gmail App Password (16 chars)
OPENAI_API_KEY=sk-...                      # OpenAI API key for GPT-5-mini
SESSION_SECRET=your-random-secret          # Flask session encryption key
```

### **RAG Pipeline Tuning**

```python
# In GithubAssistant initialization (app.py)
assistant = GithubAssistant(
    gpt_model_name='gpt-5-mini',
    vectordb_path='./vector_db',
    collection_name='my_embeddings',
    temperature=0.7,                        # Lower = factual, Higher = creative
    rag_activated=True                      # Enable RAG validation
)
```

**Key Parameters:**

- `temperature`: Controls response randomness (0.0-1.0)
  - 0.0-0.3: Factual and deterministic
  - 0.5-0.7: Balanced (recommended)
  - 0.8-1.0: Creative and variable
- `rag_activated`: Enable/disable similarity validation

---

## 🎯 Key Features

### ✨ **Smart Semantic Retrieval**

- Automatically retrieves relevant GitHub projects and information using semantic search
- Uses vector embeddings for accurate context matching
- Direct access to GitHub repositories from chat responses

### 🔗 **Rich GitHub Metadata Integration**

- Each response includes complete GitHub project metadata
- Users can directly access:
  - Repository links and README files
  - Project descriptions and timelines
  - Source code and implementation details
  - Download URLs for direct GitHub access
- Enables research-driven learning from real projects

### 📚 **Retrieval-Augmented Generation (RAG)**

- Pulls context from actual GitHub repositories and markdown files
- Provides fact-grounded answers based on real projects
- Includes source references for verification
- Ensures responses are accurate and traceable

### 💬 **Conversational Memory & Multi-turn Dialogue**

- Maintains conversation history for context-aware responses
- Supports multi-turn interactions with intelligent questioning
- Remembers previous answers within the same session
- Allows iterative refinement of questions for better results

### ✅ **Intelligent Similarity Validation**

- LLM validates if retrieved content matches the user's question
- Automatically asks for clarification if content is dissimilar
- Suggests keywords and refinements to improve search results
- Ensures high-quality, relevant answers only

### 📧 **Email Integration & Notifications**

- Sends notifications on events (downloads, messages, chat summaries)
- SMTP support for Gmail integration with App Passwords
- Customizable email templates for events

### 🔒 **Secure Configuration & Privacy**

- Secure API key management via `.env` file
- No hardcoded secrets in codebase
- Production-ready security practices
- Environmental variable isolation

### ⚡ **Performance Optimized**

- Vector database for fast semantic similarity search
- Efficient document chunking with relevance preservation
- Minimal API latency for real-time responses
- Caching mechanisms for repeated queries

---

## 📈 Monitoring & Analytics

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

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv -y

# Clone repository and setup
git clone https://github.com/vijaytakbhate2002/portfolio-support-quick-hr-interview-bot.git
cd portfolio-support-quick-hr-interview-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **2. Configure Environment Variables**

```bash
# Create .env file on EC2 with your credentials
nano .env

# Add the following:
OPENAI_API_KEY=sk-your-key
EMAIL_USER=your-email@gmail.com
APP_PASS=your-app-password
SESSION_SECRET=your-random-secret
```

### **3. Initialize Vector Database**

```bash
# Build the vector database
python3 setup_knowledge_base.py
```

### **4. Deploy Application**

```bash
# Run Flask app in background
nohup python3 app.py > app.log 2>&1 &

# Or use a process manager like systemd for production
```

### **5. Enable HTTPS with Nginx + Let's Encrypt**

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

### **6. Monitor Application**

```bash
# View application logs
tail -f app.log

# Check running processes
ps aux | grep "python3 app.py"

# Monitor system resources
top

# Check port 5000 is listening
lsof -i :5000
```

---

## 🛠️ Development Guide

### **Understanding the RAG Pipeline**

The new workflow removes question categorization and focuses on:

1. **Semantic Retrieval:** Find relevant GitHub projects
2. **Similarity Validation:** Verify question-content match
3. **Conditional Response:** Answer if similar, ask for clarification if not

### **Adding New Features**

1. **Customize Similarity Validation:**
   - Edit validation logic in `GithubAssistant`
   - Adjust thresholds for content-question matching
   - Add custom validation rules for specific domains

2. **Enhance Metadata Usage:**
   - Modify metadata fields collected in `setup_knowledge_base.py`
   - Add custom fields from GitHub API responses
   - Update metadata display in frontend

3. **New Chat Functionality:**
   - Add new routes in `app.py`
   - Implement logic using `GithubAssistant.chat_with_model()`
   - Return structured responses with metadata
   - Update frontend in `templates/`

4. **Customize Knowledge Base:**
   - Edit `setup_knowledge_base.py` for different repositories
   - Modify metadata extraction from GitHub
   - Adjust document chunking strategy
   - Rebuild vector database: `python setup_knowledge_base.py`

5. **Fine-tune Response Quality:**
   - Adjust `TEMPERATURE` in `src/config.py` (lower = more factual)
   - Modify system prompts in `src/prompts.py`
   - Update validation criteria in assistant logic
   - Test with `validation_pipeline.py`

6. **Extend Frontend:**
   - Edit HTML templates in `templates/`
   - Update styles in `static/style.css`
   - Enhance interactivity in `static/script.js`
   - Display metadata in chat UI

### **Testing the RAG Pipeline**

```bash
# Test with predefined questions
python validation_pipeline.py

# Test with custom question
python test_code/test_llm_workflow.py
```

### **Debugging Tips**

```python
# Check what's being retrieved from vector DB
# Add this to app.py for debugging:
print(f"Retrieved chunks: {ai_result.get('retrieved_chunks', [])}")
print(f"RAG relevance: {ai_result.get('rag_relevance', '')}")
print(f"Metadata: {ai_result.get('metadatas', [])}")

# Monitor similarity validation
# Check if LLM is correctly validating question-content match
print(f"Similarity score: {ai_result.get('similarity_score', '')}")
```

### **Best Practices**

- Always test changes locally before deployment
- Run validation pipeline to check quality metrics
- Use `.env` for sensitive configuration
- Document API changes and new parameters
- Version Docker images appropriately
- Monitor MLflow for performance degradation
- Keep metadata updated in vector DB (periodically rebuild)
- Test clarification requests with edge cases
- Ensure GitHub metadata is current and accurate

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

## � Clarification & Iterative Refinement

### **When RAG Similarity Validation Fails**

If the LLM determines that retrieved chunks don't match the user's question:

1. **System Identifies Mismatch**
   - Retrieval succeeded (found chunks)
   - LLM validated they don't answer the question
   - Returns `rag_relevance: "--off"`

2. **Helpful Guidance Provided**
   - AI explains why the retrieved content doesn't match
   - Suggests keywords or skills to mention
   - GUIdes user on better phrasing
   - Example response:

   ```
   "I don't have specific information about that. Could you provide more context?
   For example:
   - Are you asking about a specific framework or tool?
   - Which domain interests you (data engineering, ML, etc.)?
   - Try mentioning specific technologies you're interested in."
   ```

3. **User Refines Question**
   - Adds more details, keywords, or context
   - Asks with improved phrasing
   - Can include specific technologies or domains
   - System loops back to Step 1 (semantic search)

### **Example Conversation Flow**

```
User: "Tell me about your backend projects"
      (Retrieved content: ML projects, frontend projects, data analysis)
      LLM Validation: "No, these don't address backend work"
      ↓
Assistant: "I don't see specific backend projects in my current knowledge base.
Could you clarify?
- Are you interested in a specific technology? (Node.js, Django, Spring Boot)
- What backend domain? (APIs, databases, microservices)
- Any particular language? (Python, Java, Go)"
      ↓
User: "Do you have experience with Node.js and REST APIs?"
      (Retrieved content: backend API projects, Node.js repos)
      LLM Validation: "Yes, these are relevant backend projects!"
      ↓
Assistant: "Yes! I've worked on several REST API projects using Node.js including...
[Provides detailed answer with GitHub repository links]"
```

### **Benefits of This Approach**

✅ **Prevents False Positives:** Won't give irrelevant answers  
✅ **Improves User Understanding:** Guides users on what information exists  
✅ **Iterative Learning:** Users refine questions naturally  
✅ **Quality Assurance:** All answers are fact-grounded in actual projects  
✅ **Transparency:** Users see why answers are or aren't available

### **Best Practices for Users**

When asking questions:

- Be **specific** about technologies, domains, or tools
- **Include context** (is this for web, data science, ML?)
- Mention **frameworks or languages** if relevant
- Ask about **specific skills or experiences**
- If no answer is found, try a **different angle or more details**

---

## 🐛 Troubleshooting

### **Issue: Always Getting "Ask for Clarification" Responses**

```
Solution (RAG Similarity Validation Failing):
1. Check if vector database is properly initialized
   - Verify vector_db/chroma.sqlite3 exists
   - Confirm README files were downloaded
   - Run: python setup_knowledge_base.py

2. Ensure questions are specific enough
   - Add more keywords or context
   - Mention specific technologies or domains
   - Instead of: "Tell me about projects"
   - Try: "Do you have ML projects using Python TensorFlow?"

3. Verify metadata is being indexed
   - Check github_data/metadata.json has entries
   - Verify metadata_updated.json exists
   - Review chunks_docs.json for chunk count

4. Adjust LLM validation threshold
   - Lower TEMPERATURE in config.py for stricter matching
   - Review similarity validation logic in assistant
   - Test with known relevant queries
```

### **Issue: Missing GitHub Metadata in Responses**

```
Solution:
1. Rebuild vector database with complete metadata
   - Run: python setup_knowledge_base.py
   - Ensure GitHub API is accessible
   - Check network connectivity

2. Verify metadata files exist
   - Check github_data/metadata_updated.json
   - Should have all required fields
   - Validate JSON structure

3. Check metadata attachment to chunks
   - Review build_vectordb.py implementation
   - Ensure metadata passed to ChromaDB
   - Verify ChromaDB collection has metadata

4. Test metadata retrieval
   - Query ChromaDB directly
   - Confirm metadata in search results
```

### **Issue: Empty Response from AI**

```
Solution:
1. Validate OpenAI API Key
   - Check OPENAI_API_KEY in .env
   - Verify key format (starts with sk-)
   - Test API access: curl -H "Authorization: Bearer YOUR_KEY" https://api.openai.com/v1/models

2. Verify vector database exists
   - Confirm vector_db/chroma.sqlite3 file exists
   - Check file size (should be > 1MB)
   - Run setup_knowledge_base.py to rebuild if needed

3. Check OpenAI API quota
   - Visit platform.openai.com/account/usage
   - Ensure positive balance
   - Check rate limits haven't been exceeded
```

### **Issue: Email Not Sending**

```
Solution:
1. Setup Gmail App Password correctly
   - Enable 2-Factor Authentication first
   - Go to myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Use 16-character app password (remove spaces)

2. Verify .env configuration
   - EMAIL_USER: your-email@gmail.com
   - APP_PASS: 16 character app password
   - Do NOT use your regular Gmail password

3. Check SMTP Configuration
   - Server: smtp.gmail.com
   - Port: 587
   - Security: STARTTLS (not SSL)

4. Verify network connectivity
   - Ensure port 587 is open outbound
   - Check firewall settings
   - Test connection: telnet smtp.gmail.com 587
```

### **Issue: Slow Response Time**

```
Solution:
1. Reduce RAG search scope
   - Lower k parameter (top-k chunks)
   - Example: k=3 instead of k=10
   - Reduces embedding search time

2. Optimize context window
   - Use fewer chunks in LLM context
   - Reduces token processing
   - Faster completion

3. Use faster embedding model
   - Current: all-MiniLM-L6-v2 (384-dim)
   - Consider: DistilBERT (smaller size)
   - Trade-off: speed vs accuracy

4. Scale infrastructure
   - Upgrade EC2 instance type
   - Add more CPU cores
   - Increase available RAM

5. Implement caching
   - Cache frequent queries
   - Store popular responses
   - Reduce recomputation
```

### **Issue: Application Not Starting**

```
Solution:
1. Check application logs
   - tail -f app.log
   - Look for exception stack traces
   - Check initialization errors

2. Verify all environment variables in .env
   - OPENAI_API_KEY set correctly
   - EMAIL_USER set
   - APP_PASS set
   - SESSION_SECRET set

3. Check port availability
   - lsof -i :5000
   - Kill conflicting process: kill -9 PID
   - Or use different port in app.py

4. Verify vector database exists
   - Check vector_db/chroma.sqlite3
   - Run setup_knowledge_base.py if missing

5. Check Python environment
   - source venv/bin/activate
   - pip install -r requirements.txt
   - python3 app.py
```

### **Issue: RAG Validation Too Strict (No Answers)**

```
Solution:
1. Adjust validation thresholds
   - Review similarity_score calculation
   - Use softer matching criteria
   - Allow partial matches

2. Relax LLM validation
   - Increase TEMPERATURE (0.7 → 0.9)
   - Modify validation prompt
   - Add more context to validation

3. Improve chunk quality
   - Increase chunk size
   - Better overlap between chunks
   - Preserve more context

4. Test with broader queries
   - Use general keywords first
   - Progressively narrow down
   - Identify what IS indexed
```

### **Issue: Metadata Not Displaying in Frontend**

```
Solution:
1. Verify API response structure
   - Check /chat endpoint returns metadatas array
   - Validate JSON format
   - Log response in app.py

2. Check frontend JavaScript
   - Verify script.js handles metadata
   - Check console for errors
   - Ensure metadata is extracted from response

3. Validate HTML/CSS
   - Check templates for metadata display elements
   - Verify CSS classes applied
   - Test in browser dev tools

4. Debug response format
   - Print ai_result in app.py
   - Verify metadatas populated
   - Check all expected fields present
```

### **Issue: Vector Database Corruption**

```
Solution:
1. Backup current database
   - cp -r vector_db vector_db.backup

2. Rebuild from scratch
   - rm -rf vector_db
   - python setup_knowledge_base.py
   - Wait for completion

3. Verify rebuilt database
   - Check vector_db/chroma.sqlite3 exists
   - Confirm file size reasonable
   - Test with known queries
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
