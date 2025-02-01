from src.utils import extract_text_from_pdf
from src.exception import CustomException
from src.logger import logging

class ColdMail:
    def __init__(self):
        pass
    
    def cold_mail_prompt(self,resume_text, job_description):

        

        input_prompt = f"""
            Act like a professional career consultant. Based on the given resume and job description, 
            compose a personalized cold email that highlights the candidate's skills, aligns their experience 
            with the job requirements, and conveys genuine interest in the role. Ensure the email is concise, 
            professional, and compelling to grab the recruiter's attention.

            resume: {resume_text}
            job description: {job_description}

            The response should be structured in JSON format as follows:
            {{
                "subject": "[A catchy and professional email subject line]",
                "body": {{
                    "introduction": "Briefly introduce the candidate.",
                    "alignment": "Explain how the candidate’s skills and experience match the job description.",
                    "interest": "Express enthusiasm for the role and the company.",
                    "call_to_action": "Politely request a meeting, an interview, or a chance to discuss further.",
                    "closing": "End the email professionally with a warm closing."
                }}
            }}
            Ensure the JSON response is valid and properly formatted.
            """

        return input_prompt
        
