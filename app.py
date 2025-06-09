from flask import Flask, render_template, request, jsonify, url_for, flash, redirect,Blueprint
import json
from flask_mail import Mail, Message
from src.pipeline.responce_pipeline import jobMentorFunctionality
from src.utils import configure_genai_api,start_chat_session,extract_text_from_pdf,extract_text_from_pdf_with_pdfplumber
# from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import os
from src.utils import configure_genai_api, start_chat_session, extract_text_from_pdf
from src.logger import logging
from src.exception import CustomException
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

# Load the .env file

# Flask app initialization
app = Flask(__name__)


load_dotenv()
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

csrf = CSRFProtect(app)



app.secret_key = os.getenv("FLASK_SECRET_KEY", "80333abe149b7a41a8e08782af0fe7c5")

app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))  # Default port for TLS
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "True") == "True"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")





mail = Mail(app)

# Apply ProxyFix to handle headers
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route("/contact", methods=["GET", "POST"])
@csrf.exempt
def contact():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Form Validation
        if not name or not email or not message:
            flash("All fields are required!", "danger")
            return redirect(url_for("contact"))

        # Send an email
        try:
            # Create a message object
            msg = Message(
                subject=f"New Contact Message from {name}",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[app.config['MAIL_USERNAME']]
            )
            # Set message body
            msg.body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
            
            # Send email
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            # Log error and flash failure message
            print(f"Error: {e}")
            flash("Failed to send email. Please try again later.", "danger")

        return redirect(url_for("contact"))

    # Render the contact page
    return render_template("contact.html")


    







@app.route('/')
def index():
    return render_template('index.html')







@app.route('/about-us')
def about():
    return render_template('About.html')





@app.route('/cover-letter',methods=['GET'])
def cover_letter():
    return render_template('coverLetter.html')



@app.route('/cover-letter-generator-api',methods=['POST'])
@csrf.exempt
def cover_letter_generator_api():
    if request.method == 'POST':
        # Extract form data and uploaded resume file
        job_description = request.form['job_description']
        resume_file = request.files['resume']

        
        # Initialize the functionality and generate the updated resume
        letter = jobMentorFunctionality()


        # Call the function to update the resume
        responce = letter.cover_letter_generator(resume_pdf=resume_file, job_description=job_description)

        return jsonify(responce)
        
    







@app.route('/pricing')
def pricing():
    return render_template('pricing.html')



# resume Genrator

@app.route('/resume-generator', methods=['GET'])
def resume_generator():
    return render_template('UpdateResume.html')




@app.route('/resume-generator-api', methods=['POST'])
@csrf.exempt
def resume_generator_api():
    if request.method == 'POST':
        # Extract form data and uploaded resume file
        job_description = request.form['job_description']
        resume_file = request.files['resume']

        
        # Initialize the functionality and generate the updated resume
        resume = jobMentorFunctionality()


        # Call the function to update the resume
        responce = resume.resume_generator(resume_pdf=resume_file, job_description=job_description)

        return jsonify(responce)
        
        







@app.route('/terms-condition')
def termscondition():
    return render_template('TermsCondition.html')


@app.route('/privacy-policy')
def privacypolicy():
    return render_template('PrivacyPolicy.html')


@app.route('/disclaimer')
def disclaimer():
    return render_template('Disclaimer.html')































@app.route('/cold-mail', methods=["GET"])
def cold_mail():
    try:
        logging.info("Rendering coldMail.html page.")
        return render_template('coldMail.html')
    except Exception as e:
        logging.error(f"Error rendering coldMail.html: {str(e)}", exc_info=True)
        return jsonify({"error": "Something went wrong while loading the page."}), 500


@app.route('/cold-mail-api/', methods=['POST'])
@app.route('/cold-mail-api', methods=['POST'])
@csrf.exempt
def cold_mail_api():
    try:
        if request.method == "POST":
            logging.info("POST request received for /cold-mail-api endpoint.")

            # Fetch form data
            job_description = request.form.get('job_description', None)
            resume_file = request.files.get('resume', None)

            # Validate input
            if not job_description:
                logging.warning("Job description is missing in the request.")
                return jsonify({"error": "Job description is required."}), 400
            if not resume_file:
                logging.warning("Resume file is missing in the request.")
                return jsonify({"error": "Resume file is required."}), 400

            logging.info("Job description and resume file received successfully.")

            
            c_mail = jobMentorFunctionality()
            responce = c_mail.cold_mail(resume_pdf=resume_file, job_description=job_description)
            
        
            # Access individual fields
            subject = responce["subject"]
            introduction = responce["body"]["introduction"]
            alignment = responce["body"]["alignment"]
            interest = responce["body"]["interest"]
            call_to_action = responce["body"]["call_to_action"]
            closing = responce["body"]["closing"]

            # Example: Sending response to frontend
            response = {
                "subject": subject,
                "email_body": {
                    "introduction": introduction,
                    "alignment": alignment,
                    "interest": interest,
                    "call_to_action": call_to_action,
                    "closing": closing
                }
            }

            logging.info("Cold mail generated successfully.")
            return jsonify(response)


        
    except Exception as e:
        logging.error(f"Error occurred in /cold-mail-api: {str(e)}", exc_info=True)
        return jsonify({"error": "An internal error occurred while processing your request."}), 500














@app.route('/generate-questions', methods=["GET"])
def generate_questions():
    try:
        logging.info("Rendering questionGenration.html page.")

        return render_template('questionGenration.html')
    
    except Exception as e:

        logging.error(f"Error rendering coldMail.html: {str(e)}", exc_info=True)

        return jsonify({"error": "Something went wrong while loading the page."}), 500
    


@app.route('/generate-questions-api', methods=['POST'])
@csrf.exempt
def generate_questions_api():

    try:
        if request.method == "POST":
            logging.info("POST request received for /generate-questions-api endpoint.")

            # Fetch form data
            job_description = request.form.get('job_description',None)
            resume_file = request.files.get('resume', None)

            # Validate input
            if not job_description:
                logging.warning("Job description is missing in the request.")
                return jsonify({"error": "Job description is required."}), 400
            if not resume_file:
                logging.warning("Resume file is missing in the request.")
                return jsonify({"error": "Resume file is required."}), 400

            logging.info("Job description and resume file received successfully.")

            
            question = jobMentorFunctionality()
            response = question.interview_questions(resume_pdf=resume_file, job_description=job_description)
            

            
            if response.startswith("```json"):
                response = response[len("```json"):].strip() 
                logging.info("if run succssfully")
                 # Remove the `'''json` prefix
                
            if response.endswith("```"):
                response = response[:-len("```")].strip()  # Remove trailing `'''`
                logging.info("if run succssfully")
                
            
            parsed_response = json.loads(response)
            logging.info("convert the json ")

            return jsonify(parsed_response)

            
    except Exception as e:
        # logging.error(f"Error occurred in /generate-questions-api: {str(e)}", exc_info=True)
        return jsonify({"error": "An internal error occurred while processing your request."}), 500

    

        
@app.route('/ats-score', methods=['GET'])
@csrf.exempt  # This line disables CSRF protection for this route
def ats_score():
    return render_template('AtsScore.html')


# Disable CSRF Protection for specific routes (e.g., '/check-ats-score')
@app.route('/check-ats-score', methods=['POST'])
@csrf.exempt  # This line disables CSRF protection for this route
def ats_scores():
    if request.method == 'POST':
        # Handle POST request (form submission logic)
        job_description = request.form['job_description']
        resume_file = request.files['resume']
        
        # Your logic for checking ATS score, resume parsing, etc.
        a = jobMentorFunctionality()

        response_data = a.ats_score(resume_pdf = resume_file,job_description = job_description)

        percentage_str = response_data.get('JDMatch', '')
        missing_keywords = response_data.get('MissingKeywords', [])
        profile_summary = response_data.get('ProfileSummary', '')

        ats_score = int(percentage_str[:-1])
        # ats_score = 80  # Placeholder score
        # missing_keywords = ['Python', 'Data Science', 'Himanshu Chaurasiya']  # Example missing keywords
        # profile_summary = resume_text # Example summary
        
        # Return the result as JSON
        return jsonify({
            'success': True,
            'ats_score': ats_score,
            'missing_keywords': missing_keywords,
            'profile_summary': profile_summary,
            'updated_resume_url': '/path/to/updated_resume.pdf'  # Link to updated resume if applicable
        })

    # If GET request, return the form or page (can be used to display the form initially)
    return render_template('AtsScore.html')








if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

