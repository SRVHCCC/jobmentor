from src.utils import extract_text_from_pdf
import json
from src.exception import CustomException
from src.logger import logging

class AtsScore:
    def __init__(self):
        pass
    
    def ats_score_prompt(self,resume_text, job_description):

        

        """
        Use Google Generative AI to evaluate the resume against the job description.
        
        Args:
            resume_text: The extracted text from the resume.
            job_description: The text of the job description.
            
        Returns:
            A dictionary containing the evaluation results or an error message.
        """
        input_prompt = f"""
        Act like a skilled ATS (Application Tracking System) evaluator. Analyze the given resume
        and job description. Provide a percentage match and list missing keywords for improvement. 
        Make sure your response is clear and actionable for improving the resume. 
        
        resume: {resume_text}
        job description: {job_description}
        
        The response should be in the following structure:
        {{
            "JDMatch": "%", 
            "MissingKeywords": [list of missing keywords],
            "ProfileSummary": "Suggested profile summary"
        }}
        """

        return input_prompt
        
