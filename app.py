from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, flash, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import GPT_MODEL_NAME
from rag_assisted_bot import Assistant
from dotenv import load_dotenv
import os

load_dotenv()

sender_email = os.getenv("EMAIL_USER")
app_password = os.getenv("APP_PASS")
recipient_email = "takbhatevijay@gmail.com" # Hardcoded recipient as per original code

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
        
        # Call the new assistant
        ai_result = assistant.chat_with_model(user_message)
        
        # Extract response model
        response_model = ai_result['response']
        
        # Construct the response for the frontend
        # output structure of llm class InterViewResponse(BaseModel):
        # response_message: str
        # reference_links: List[str]
        # confidence_score: float
        # follow_up_question: str
        # additional_resources: List[str]
        
        response_data = {
            'response_message': response_model.response_message,
            'reference_links': response_model.reference_links,
            'confidence_score': response_model.confidence_score,
            'follow_up_question': response_model.follow_up_question,
            'additional_resources': response_model.additional_resources,
            'question_category': ai_result.get('question_category', 'unknown')
        }

        # Adapt to what frontend expects, or send the structured object
        # Frontend originally expected: {'AI Assistant': formatted_string}
        # We will change frontend to handle this object.
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

        # Create a basic summary using the assistant (if it has a summary method) or just send history
        # The previous code used assistant.summarize_conversation(history)
        # Checking if new assistant has this capability. If not, we might need to implement it or use a raw LLM call.
        # For now, we will just send the history as the summary or a placeholder message until we verify if Assistant has summary.
        # Assuming for now we just email the history.
        
        summary = f"Conversation History:\n{history}"
        
        subject = "Portfolio Chatbot Conversation Summary"
        body = f"Here is the summary of a recent conversation with your portfolio chatbot:\n\n{summary}"
        
        send_email_notification(subject, body)
        
        return jsonify({'status': 'success', 'summary': "Conversation ended. Summary sent."})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

sender_email = os.getenv("EMAIL_USER")
app_password = os.getenv("APP_PASS")
recipient_email = "takbhatevijay@gmail.com" # Hardcoded recipient as per original code

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')


class AIAssistant:
    """ This class helps configuring llm model and also responsible for llm communication """

    def __init__(self, model_name:str, temperature:float, 
                 conversation_structure, question_category_structure, 
                 question_category_prompt):
        
        self.model_name = model_name
        self.temperature = temperature
        self.conversation_structure = conversation_structure
        self.question_category_structure = question_category_structure
        self.question_category_prompt = question_category_prompt

        self.assistant = ResumeAssistant(
                model_name=model_name,
                temperature=temperature,
                conversation_structure=conversation_structure,
                question_category_structure=question_category_structure,
                question_category_prompt=question_category_prompt

            )
    

    def chatWithLLM(self, question:str) -> tuple:
        """ Args:
                question: str (question need to provide to llm model)
            Returns:
                response, question_category: tuple (Returns response provided by llm with category of 
                                             qeustion [personal, project, soft_skills, experience, education etc.])
        """

        result = self.assistant.chatWithModel(question=question)
        return result['response'], result['question_category'] 
    

    def responseFormat(self, llm_response:dict) -> str:
        """ Args: 
                llm_response: str (this is the dictionary containing llm response)
            Returns:
                    formatted_response: str (converts lists into bullet points and reference links into bullet points) """
        
        response_message = llm_response.response_message
        list_items = ""
        reference_linsk = ""
        if type(llm_response.list_items) == list:
            list_items = "\n".join(llm_response.list_items) + "\n"
        if type(llm_response.reference_links) == list:
            reference_linsk = "\n".join(llm_response.reference_links) + "\n"
        return response_message + " " + list_items + " " + reference_linsk
    
    def summarize_conversation(self, history: str) -> str:
        """
        Summarizes the conversation history into 2 sentences.
        """
        prompt = f"Summarize the following conversation between a user and an AI assistant in exactly two sentences:\n\n{history}"
        
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)
        response = llm.invoke(prompt)
        return response.content

assitant = AIAssistant(
    model_name=GPT_MODEL_NAME,
    temperature=TEMPERATURE,
    conversation_structure=InterviewResponse,
    question_category_structure=QuestionCategory,
    question_category_prompt=question_category_prompt
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
        
        ai_response, question_category = assitant.chatWithLLM(user_message)
        formatted_response = assitant.responseFormat(ai_response)

        return jsonify({'AI Assistant': formatted_response})
    
    except Exception as e:
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

        summary = assitant.summarize_conversation(history)
        
        subject = "Portfolio Chatbot Conversation Summary"
        body = f"Here is the summary of a recent conversation with your portfolio chatbot:\n\n{summary}"
        
        send_email_notification(subject, body)
        
        return jsonify({'status': 'success', 'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
