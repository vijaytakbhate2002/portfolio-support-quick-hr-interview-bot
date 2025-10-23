from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, flash, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

sender_email = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

TEMPLATE_RESPONSES = {
    "hello": "Hello! I'm the AI HR Assistant for this portfolio. I can help you learn about the candidate's AI and MLOps experience. What would you like to know?",
    "skills": "This candidate has expertise in Python, Machine Learning, MLOps tools like MLflow and Airflow, containerization with Docker, and LLM operations. They also work with frameworks like TensorFlow, PyTorch, and cloud platforms.",
    "projects": "The portfolio showcases three main projects: Medical Insurance Cost Prediction, Turbofan Jet Engine Lifecycle Prediction, and other ML/LLM projects. Would you like details about any specific project?",
    "experience": "The candidate has experience in AI/ML model development, MLOps pipeline automation, model monitoring, and deployment. They work with the full ML lifecycle from data processing to production deployment.",
    "contact": "You can download the resume from the Resume section below, or use the Contact section to connect directly for the next round of interviews!",
    "default": "That's an interesting question! As a demo chatbot, I'm using template responses right now. The full AI integration is coming soon. Meanwhile, you can explore the portfolio sections below to learn more about the candidate's projects and skills!"
}

def get_template_response(user_message):
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
        return TEMPLATE_RESPONSES["hello"]
    elif any(word in message_lower for word in ["skill", "technology", "tech stack", "tools"]):
        return TEMPLATE_RESPONSES["skills"]
    elif any(word in message_lower for word in ["project", "work", "portfolio"]):
        return TEMPLATE_RESPONSES["projects"]
    elif any(word in message_lower for word in ["experience", "background", "expertise"]):
        return TEMPLATE_RESPONSES["experience"]
    elif any(word in message_lower for word in ["contact", "resume", "cv", "hire"]):
        return TEMPLATE_RESPONSES["contact"]
    else:
        return TEMPLATE_RESPONSES["default"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        ai_response = get_template_response(user_message)
        
        return jsonify({'response': ai_response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route("/send_message", methods=["POST"])
def send_message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = sender_email
    msg['Subject'] = f"Portfolio Message from {name}"

    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, [sender_email, "vijaytakbhate45@gmail.com"], msg.as_string())
        server.quit()
        flash("Message sent successfully!", "success")
    except Exception as e:
        print(e)
        flash("Failed to send message. Please try again.", "error")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
