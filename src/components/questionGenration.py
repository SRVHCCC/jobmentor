from src.utils import extract_text_from_pdf
from src.exception import CustomException
from src.logger import logging


class InterviewQuestionGenerator:
    def __init__(self):
        self

    def interview_questions_prompt(self, resume_text, job_description):

       


        """
        Generate a list of potential interview questions using Google Generative AI.
        
        Args:
            resume_text: Extracted text from the resume.
            job_description: Text of the job description.
            
        Returns:
            A dictionary containing categorized interview questions or an error message.
        """
        input_prompt = f"""
        Act as an experienced HR professional and interview coach. Based on the given resume and job description, 
        generate a list of 20 potential interview questions. These questions should focus on the candidate’s skills, 
        experiences, and achievements mentioned in the resume, as well as the requirements and responsibilities 
        outlined in the job description.

        The questions should be categorized as follows:
        1. Technical Skills: Questions related to technical abilities mentioned in the resume or required in the job description.
        2. Behavioral: Questions assessing the candidate's soft skills, problem-solving abilities, teamwork, leadership, and decision-making.
        3. Situational: Hypothetical scenarios related to the job responsibilities to evaluate how the candidate might handle specific challenges.
        4. Job Fit: Questions related to the candidate's motivation, alignment with the company’s values, and long-term career goals.

        resume: {resume_text}
        job description: {job_description}

        The response should be in the following structure:
        {{
            "Technical Questions": [
                "Question 1",
                "Question 2",
                ...
            ],
            "Behavioral Questions": [
                "Question 1",
                "Question 2",
                ...
            ],
            "Situational Questions": [
                "Question 1",
                "Question 2",
                ...
            ],
            "Job Fit Questions": [
                "Question 1",
                "Question 2",
                ...
            ]
        }}
        """
        
        return input_prompt
