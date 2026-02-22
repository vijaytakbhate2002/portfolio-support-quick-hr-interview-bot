from dotenv import load_dotenv
import os

load_dotenv()

sender_email = os.getenv("EMAIL_USER")
app_password = os.getenv("APP_PASS")
recipient_email = "takbhatevijay@gmail.com" # Hardcoded recipient as per original code
TOKEN_GITHUB = os.getenv("TOKEN_GITHUB")

from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, flash, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import GPT_MODEL_NAME
from rag_assisted_bot import Assistant

# RAG Configuration
VECTORDB_PATH = "./vector_db"
COLLECTION_NAME = "my_embeddings"

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

# Initialize the new RAG Assistant
assistant = Assistant(
    gpt_model_name=GPT_MODEL_NAME,
    vectordb_path=VECTORDB_PATH,
    collection_name=COLLECTION_NAME,
    temperature=0.7,
    rag_activated=True
)

def send_email_notification(subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, [recipient_email], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

@app.route('/')
def index():
    """ Defalut page visibility """
    return render_template('index.html')


def metadata_selector(metadatas:list) -> list:
    """ This function will fetch unique metadata dictionaries and return a list of unique metadata dictionaries. 
        This is to avoid sending duplicate metadata information to frontend.
        format: [{}, {}]
        """
    
    unique_repo_names = []
    unique_metadata = []
    for metadata in metadatas:
        if metadata['repo_name'].strip() not in unique_repo_names:
            unique_repo_names.append(metadata['repo_name'].strip())
            unique_metadata.append(metadata)

    return unique_metadata


@app.route('/chat', methods=['POST'])
def chat():
    """ 
        Get's user input text, provide it to llm, take the response, format the response and return with Jsonify \
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        ai_result = assistant.chat_with_model(user_message)
        # unique_meatadas = metadata_selector(ai_result['metadatas'][0])
        metadatas = ai_result.get('metadatas', [])
        unique_metadatas = []
        if metadatas and isinstance(metadatas, list):
            unique_metadatas = metadata_selector(metadatas[0])
        response_model = ai_result['response']
        response_data = {
            'response_message': response_model.response_message,
            'reference_links': response_model.reference_links,
            'question_category': ai_result.get('question_category', 'Uncategorized'),
            'rag_activation': "--on" if ai_result.get('rag_activation', '').lower() == "yes" else "--off",
            'metadatas': unique_metadatas
        }

        return jsonify(response_data)
    
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/static/<path:filename>')
def serve_static(filename):
    """ 
        Responsible to serve all static infromation, images to frontend 
    """
    return send_from_directory('static', filename)


@app.route("/send_message", methods=["POST"])
def send_message():
    """ 
    Serves as backend for get in touch section (direct email from protfoilo)
    """
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    subject = f"Portfolio Message from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    
    if send_email_notification(subject, body):
        flash("Message sent successfully!", "success")
    else:
        flash("Failed to send message. Please try again.", "error")

    return redirect(url_for('index'))

@app.route("/track_download", methods=["POST"])
def track_download():
    """
    Tracks resume downloads and sends an email notification.
    """
    try:
        subject = "Resume Download Notification"
        body = "Someone has downloaded your resume from the portfolio."
        send_email_notification(subject, body)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/end_chat", methods=["POST"])
def end_chat():
    """
    Summarizes the conversation and sends an email.
    """
    try:
        data = request.get_json()
        history = data.get('history', '')
        
        if not history:
            return jsonify({'error': 'No history provided'}), 400
        
        summary = f"Conversation History:\n{history}"
        
        subject = "Portfolio Chatbot Conversation Summary"
        body = f"Here is the summary of a recent conversation with your portfolio chatbot:\n\n{summary}"
        
        send_email_notification(subject, body)
        
        return jsonify({'status': 'success', 'summary': "Conversation ended. Summary sent."})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

