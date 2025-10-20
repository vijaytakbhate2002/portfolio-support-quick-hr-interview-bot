test_context = r"""
Vijay Takbhate is a Data Science and MLOps enthusiast skilled in Python, SQL, MLflow, Docker, and CI/CD.
He has built end-to-end ML projects focusing on model deployment and automation using Flask, AWS, and GitHub Actions.

Key Projects:
1. Medical Insurance Cost Prediction (SVR) – Deployed on AWS with Docker and MLflow tracking.
2. Jet Engine RUL Prediction (CNN + LSTM) – Implemented MLOps pipeline using AWS and Docker.

Experience:
- Risk Analyst at InCred: Automated policy verification using Python and CI/CD.
- Automation Engineer at Fox Solutions: Developed reproducible automation pipelines.

Education: B.Tech in Electronics & Telecommunication, 2024.
Certifications: Complete MLOps Bootcamp (Udemy).
"""



context = r"""
Vijay Takbhate is a Data Science and MLOps enthusiast skilled in Python, SQL, MLflow, Docker, and CI/CD.
He has worked on multiple end-to-end machine learning projects, focusing on model deployment and automation.

Projects include:
1. Medical Insurance Cost Prediction (SVR): Built a predictive system to estimate medical insurance charges
   using demographic and lifestyle factors like age, BMI, smoking status, and region. Improved R² from 0.72 to 0.86
   and reduced MAE from 0.099 to 0.034. Developed a Flask web application, containerized with Docker, and deployed on AWS EC2.
   Implemented MLOps best practices like MLflow tracking, GitHub Actions CI/CD, and Kubeflow pipelines.
   Repository: https://github.com/vijaytakbhate2002/medical-insurance-cost-prediction-SVR.git

2. Turbofan Jet Engine Lifecycle Prediction (CNN + LSTM): Developed a Remaining Useful Life (RUL) prediction
   system using NASA CMAPSS dataset. Built a hybrid CNN + LSTM model for temporal and spatial patterns.
   Implemented an MLOps pipeline with data processing, training, and deployment using AWS and Docker.
   Repository: https://github.com/vijaytakbhate2002/nasa_turbofan_engine_life_cycle_prediction.git

Other projects: https://github.com/vijaytakbhate2002

Experience:
- Risk Analyst (InCred Financial Services): Designed and deployed policies in Business Rule Engine,
  built a Python package 'Simulator' reducing policy verification time by 30%, integrated CI/CD workflows using GitHub Actions,
  and worked with Databricks, Metabase, SQL, and Excel.
- Automation Engineer (Fox Solutions): Built automation pipelines with monitoring and reproducibility focus
  using version control and PLC/SCADA tools.

Technical Skills:
Python, SQL, MLflow, DVC, DagsHub, Docker, GitHub Actions, Streamlit, Flask, Databricks, PySpark, AWS, GCP, Kubernetes.

Certifications:
- Complete MLOps Bootcamp with 10+ Projects (Udemy)
- MLOps Bootcamp: Mastering AI Operations (Udemy)

Education:
Bachelor of Technology in Electronics and Telecommunication, SVERI’s College of Engineering, 2024.
Diploma in Electronics and Telecommunication, 2021.

Blogging:
- "Supervised, Unsupervised, & Beyond: ML Techniques Simplified"
- "Comprehensive Docker Guide: Containerizing Flask Applications"

Soft Skills:
Critical Thinking, Problem Solving, Understanding Business Needs.
Languages: English, Marathi, Hindi.
"""


hr_questions = [
    # Personal / Background
    "Tell me about yourself.",
    "Walk me through your resume.",
    "What are your strengths and weaknesses?",
    "Why did you choose Data Science as a career?",
    "Where do you see yourself in 5 years?",
    "Why do you want to join our company?",
    "How do you handle stress or tight deadlines?",
    "Describe a time you faced a challenge and how you overcame it.",

    # Motivation & Behavioral
    "Why should we hire you?",
    "How do you keep yourself updated in the Data Science field?",
    "Describe a project where you made a significant impact.",
    "Give an example of a time you worked in a team.",
    "How do you prioritize tasks when handling multiple projects?",
    "Describe a situation when your solution failed — what did you learn?",

    # Project / Technical Experience
    "Explain a machine learning project you worked on end-to-end.",
    "What challenges did you face while deploying a model?",
    "How do you validate the performance of your models?",
    "Explain a time you automated a workflow or pipeline.",
    "How do you handle missing or inconsistent data?",
    "Describe your experience with ML frameworks (like scikit-learn, TensorFlow, PyTorch).",

    # Soft Skills / Teamwork
    "How do you handle conflicts in a team?",
    "Have you mentored or guided someone? How?",
    "Describe your approach to problem-solving.",
    "How do you explain technical concepts to non-technical stakeholders?",

    # HR Curveballs / Situational
    "Are you open to relocation or travel?",
    "What is your expected salary?",
    "How do you handle failure or criticism?",
    "Can you work under ambiguous or incomplete requirements?",
    "Why should we not hire another candidate over you?",
    "exit"
]
