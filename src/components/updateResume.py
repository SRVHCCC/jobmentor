
from src.exception import CustomException
from src.logger import logging



class UpdateResumePrompt:
    def __init__(self):
        pass
    
    def resume_prompt(self,resume_text, job_description):

        


        input_prompt = f"""
            Act as a professional resume editor. Based on the provided resume, job description, and project details, update the resume to make it highly ATS-friendly. The updated resume should:

            - Extract and highlight relevant **skills**, **experiences**, **projects**, and **keywords** from the job description and resume.
            - Reformat the resume sections using industry best practices to optimize for ATS (Applicant Tracking Systems).
            - Use concise, professional language that aligns with the tone and keywords of the job description while preserving the candidate's original accomplishments.
            - Emphasize core competencies, technical skills, and measurable achievements that match the job description requirements.
            - Ensure the resume is easy to scan and follows ATS-friendly guidelines (e.g., standard section titles, simple formatting, no tables or images).

            Here is the input data:

            - Resume: {resume_text}
            - Job Description: {job_description}
            

            ### Updated Resume Format:
            1. **Contact Information**: Include full name, phone number, professional email, LinkedIn URL, and location (city, state only).
            2. **Objective** (optional): A 1-2 line career statement tailored to align with the job description.
            3. **Skills**: A list of technical and soft skills extracted from the job description and candidate's profile.
            4. **Experience**: Focus on relevant professional experience, detailing job responsibilities and measurable achievements. Use bullet points to improve readability.
            5. **Projects** (if applicable): Highlight relevant projects, including tools, technologies used, and quantifiable outcomes.
            6. **Education**: List degrees, institutions, and graduation years in a concise format.
            7. **Certifications**: Include any relevant certifications or training aligned with the job requirements.

            ### Guidelines for ATS Optimization:
            - Use exact keywords and phrases from the job description.
            - Standard section titles: 'Experience', 'Education', 'Skills', etc.
            - Avoid fancy fonts, graphics, or complex formatting.

            ### Output:
            The updated resume should be provided in **json** ready for submission.
            """


        return input_prompt

