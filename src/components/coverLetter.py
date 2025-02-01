

class CoverLetterPrompt:
    def __init__(self):
        pass

    def cover_letter_prompt(self,resume_text , job_description):

        input_prompt = f"""
            Act as an experienced HR professional and cover letter coach. Based on the given resume and job description, 
            generate a personalized cover letter that effectively showcases the candidate's qualifications, skills, and experiences 
            relevant to the job. The cover letter should highlight the following key elements:

            1. A strong opening paragraph introducing the candidate and stating their interest in the position.
            2. A middle section that demonstrates the candidate's qualifications, achievements, and technical skills related to the job description.
            3. A closing paragraph that reaffirms the candidate's enthusiasm for the role, mentions their potential contribution to the company, 
            and expresses a desire for further discussion.

            The cover letter should be tailored to the job description, and the tone should be professional, confident, and polite.

            resume: {resume_text}
            job description: {job_description}

            The response should be in the following JSON structure:
            {{
                "cover_letter": {{
                    "opening": "Opening paragraph content here.",
                    "middle": "Middle section content here.",
                    "closing": "Closing paragraph content here."
                }}
            }}
            """


        return input_prompt
