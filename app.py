from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, flash, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import GPT_MODEL_NAME, TEMPERATURE
from src.output_structure import InterviewResponse, QuestionCategory
from src.prompts import question_category_prompt
from assistant import ResumeAssistant
from dotenv import load_dotenv
import os

load_dotenv()

sender_email = os.getenv("EMAIL_USER")
app_password = os.getenv("APP_PASS")

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
    
assitant = AIAssistant(
    model_name=GPT_MODEL_NAME,
    temperature=TEMPERATURE,
    conversation_structure=InterviewResponse,
    question_category_structure=QuestionCategory,
    question_category_prompt=question_category_prompt
)


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

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = sender_email
    msg['Subject'] = f"Portfolio Message from {name}"

    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, ["takbhatevijay@gmail.com"], msg.as_string())
        server.quit()
        flash("Message sent successfully!", "success")
    except Exception as e:
        flash("Failed to send message. Please try again.", "error")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
