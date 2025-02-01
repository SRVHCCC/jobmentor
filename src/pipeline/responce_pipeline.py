from src.logger import logging
from src.utils import configure_genai_api, start_chat_session, extract_text_from_pdf
from src.exception import CustomException
from src.components.atsScore import AtsScore
from src.components.coldMail import ColdMail
from src.components.questionGenration import InterviewQuestionGenerator
from src.components.updateResume import UpdateResumePrompt
from src.components.coverLetter import CoverLetterPrompt
import json

from src.components.dataClean import DATACLEAN
import os




class jobMentorFunctionality:
    def __init__(self):
        try:
            model = configure_genai_api()
            self.chat_session = start_chat_session(model)
            logging.info("Chat session initialized successfully.")
        except Exception as e:
            logging.error("Failed to initialize chat session.", exc_info=True)
            raise CustomException(f"Error during initialization: {e}")
        




    def ats_score(self, resume_pdf, job_description):
        try:
            logging.info("Extracting text from resume PDF.")
            resume_text = extract_text_from_pdf(resume_pdf)

            ats = AtsScore()
            input_text = ats.ats_score_prompt(resume_text=resume_text, job_description=job_description)
            response = self.chat_session.send_message(input_text)
            
            # Print the response to understand its structure
            
            
            # Now, access the correct attribute
            if hasattr(response, 'result'):
                generated_content = response.result.candidates[0].content.parts[0].text
            elif hasattr(response, '_result'):  # Checking for '_result' if 'result' doesn't exist
                generated_content = response._result.candidates[0].content.parts[0].text
            else:
                logging.error("Response object does not have expected structure.")
                raise CustomException("Unexpected response structure")

            response_data = json.loads(generated_content.strip('```json\n').strip('```'))
            
            logging.info("ATS score computed successfully.")
            return response_data

        except Exception as e:
            logging.error("Error while computing ATS score.", exc_info=True)
            raise CustomException(f"Error in ats_score: {e}")




    def cold_mail(self, resume_pdf, job_description):
        try:
            # Start logging for debugging
            logging.info("Starting the cold mail generation process.")



            
            # Step 1: Extract text from resume
            logging.info("Extracting text from the resume PDF.")
            resume_text = extract_text_from_pdf(resume_pdf)
            
            if not resume_text:
                raise CustomException("Resume text extraction failed or returned empty.")
            logging.debug(f"Extracted Resume Text: {resume_text[:100]}...")  # Log first 100 characters



            
            # Step 2: Generate the cold mail input text
            logging.info("Preparing the cold mail prompt using resume text and job description.")
            mail = ColdMail()
            input_text = mail.cold_mail_prompt(resume_text=resume_text, job_description=job_description)
            logging.debug(f"Generated Cold Mail Prompt: {input_text}")



            
            # Step 3: Send the generated input text to chat session
            logging.info("Sending the cold mail prompt to chat session.")
            response = self.chat_session.send_message(input_text)

            

            if hasattr(response, 'result'):
                generated_content = response.result.candidates[0].content.parts[0].text
            elif hasattr(response, '_result'):  # Checking for '_result' if 'result' doesn't exist
                generated_content = response._result.candidates[0].content.parts[0].text
            else:
                logging.error("Response object does not have expected structure.")
                raise CustomException("Unexpected response structure")

            response_data = json.loads(generated_content.strip('```json\n').strip('```'))
            
            
            return response_data

            

        
        

        
        except CustomException as ce:
            # Log custom exception and re-raise it
            logging.error(f"CustomException occurred: {ce}", exc_info=True)
            raise


        
        except Exception as e:
            # Log unexpected errors with traceback
            logging.error("An unexpected error occurred during cold mail generation.", exc_info=True)
            raise CustomException(f"Error in cold_mail: {e}")





    def interview_questions(self, resume_pdf, job_description):
        try:
            # Start logging for debugging
            logging.info("Starting the cold mail generation process.")



            
            # Step 1: Extract text from resume
            logging.info("Extracting text from the resume PDF.")
            resume_text = extract_text_from_pdf(resume_pdf)
            
            if not resume_text:
                raise CustomException("Resume text extraction failed or returned empty.")
            logging.debug(f"Extracted Resume Text: {resume_text[:100]}...")  # Log first 100 characters



            
            # Step 2: Generate the cold mail input text
            logging.info("Preparing the question genration prompt using resume text and job description.")
            question = InterviewQuestionGenerator()
            input_text = question.interview_questions_prompt(resume_text=resume_text, job_description=job_description)
            logging.debug(f"Generated question  Prompt: {input_text}")



            
            # Step 3: Send the generated input text to chat session
            logging.info("Sending the question genration prompt to chat session.")
            response = self.chat_session.send_message(input_text)

            

            if hasattr(response, 'result'):
                generated_content = response.result.candidates[0].content.parts[0].text
            elif hasattr(response, '_result'):  # Checking for '_result' if 'result' doesn't exist
                generated_content = response._result.candidates[0].content.parts[0].text
            else:
                logging.error("Response object does not have expected structure.")
                raise CustomException("Unexpected response structure")
            
            
            
            
            
            return generated_content

            

        
        

        
        except CustomException as ce:
            # Log custom exception and re-raise it
            logging.error(f"CustomException occurred: {ce}", exc_info=True)
            raise


        
        except Exception as e:
            # Log unexpected errors with traceback
            logging.error("An unexpected error occurred during question generation.", exc_info=True)
            raise CustomException(f"Error in interview_questions: {e}")




    
    


    def resume_generator(self, resume_pdf, job_description):
            try:
                # Start logging for debugging
                logging.info("Starting the cold mail generation process.")



                
                # Step 1: Extract text from resume
                logging.info("Extracting text from the resume PDF.")
                resume_text = extract_text_from_pdf(resume_pdf)
                
                if not resume_text:
                    raise CustomException("Resume text extraction failed or returned empty.")
                logging.debug(f"Extracted Resume Text: {resume_text[:100]}...")  # Log first 100 characters



                
                # Step 2: Generate the cold mail input text
                logging.info("Preparing the question genration prompt using resume text and job description.")
                question = UpdateResumePrompt()
                input_text = question.resume_prompt(resume_text=resume_text, job_description=job_description)
                logging.debug(f"Generated question  Prompt: {input_text}")



                
                # Step 3: Send the generated input text to chat session
                logging.info("Sending the question genration prompt to chat session.")
                response = self.chat_session.send_message(input_text)

                
                if hasattr(response, 'result'):
                    generated_content = response.result.candidates[0].content.parts[0].text
                elif hasattr(response, '_result'):  # Checking for '_result' if 'result' doesn't exist
                    generated_content = response._result.candidates[0].content.parts[0].text
                else:
                    logging.error("Response object does not have expected structure.")
                    raise CustomException("Unexpected response structure")
                

                if generated_content.startswith("```json"):
                    generated_content = generated_content[len("```json"):].strip()  # Remove the `'''json` prefix
                    
                if generated_content.endswith("```"):
                    generated_content = generated_content[:-len("```")].strip()  # Remove trailing `'''`
                    

                # # Step 2: Parse the JSON
                parsed_response = json.loads(generated_content)

                
                

                
                
                
                return parsed_response

            

        
        

        
            except CustomException as ce:
                # Log custom exception and re-raise it
                logging.error(f"CustomException occurred: {ce}", exc_info=True)
                raise


            
            except Exception as e:
                # Log unexpected errors with traceback
                logging.error("An unexpected error occurred during question generation.", exc_info=True)
                raise CustomException(f"Error in interview_questions: {e}")



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def cover_letter_generator(self, resume_pdf, job_description):
            try:
                # Start logging for debugging
                logging.info("Starting the cold mail generation process.")



                
                # Step 1: Extract text from resume
                logging.info("Extracting text from the resume PDF.")
                resume_text = extract_text_from_pdf(resume_pdf)
                
                if not resume_text:
                    raise CustomException("Resume text extraction failed or returned empty.")
                logging.debug(f"Extracted Resume Text: {resume_text[:100]}...")  # Log first 100 characters



                
                # Step 2: Generate the cold mail input text
                logging.info("Preparing the question genration prompt using resume text and job description.")
                letter = CoverLetterPrompt()
                input_text = letter.cover_letter_prompt(resume_text=resume_text, job_description=job_description)
                logging.debug(f"Generated question  Prompt: {input_text}")



                
                # Step 3: Send the generated input text to chat session
                logging.info("Sending the question genration prompt to chat session.")
                response = self.chat_session.send_message(input_text)

                
                
                if hasattr(response, 'result'):
                    generated_content = response.result.candidates[0].content.parts[0].text
                elif hasattr(response, '_result'):  # Checking for '_result' if 'result' doesn't exist
                    generated_content = response._result.candidates[0].content.parts[0].text
                else:
                    logging.error("Response object does not have expected structure.")
                    raise CustomException("Unexpected response structure")
                

                if generated_content.startswith("```json"):
                    generated_content = generated_content[len("```json"):].strip()  # Remove the `'''json` prefix
                    
                if generated_content.endswith("```"):
                    generated_content = generated_content[:-len("```")].strip()  # Remove trailing `'''`


                parsed_response = json.loads(generated_content)
                    

                # # Step 2: Parse the JSON
                

                
                

                
                
                
                return parsed_response

            

        
        

        
            except CustomException as ce:
                # Log custom exception and re-raise it
                logging.error(f"CustomException occurred: {ce}", exc_info=True)
                raise


            
            except Exception as e:
                # Log unexpected errors with traceback
                logging.error("An unexpected error occurred during question generation.", exc_info=True)
                raise CustomException(f"Error in interview_questions: {e}")






















    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def auto_update_resume(self, resume_pdf, job_description, output_pdf):
    #     """
    #     Automatically update the resume based on the job description.

    #     Args:
    #         resume_pdf: Path to the uploaded resume PDF.
    #         job_description: Text of the job description.
    #         output_pdf: Path to save the updated resume PDF.
    #     """
    #     try:
    #         logging.info("Extracting text from resume PDF.")
    #         # Step 1: Extract text from the uploaded resume PDF
    #         resume_text = extract_text_from_pdf(resume_pdf)

    #         # Step 2: Analyze the resume and job description for missing keywords
    #         analyzer = KeywordAnalyzer()
    #         logging.info("Analyzing keywords for the resume.")
    #         input_text = analyzer.analyze_keywords(resume_text, job_description)
    #         response = self.chat_session.send_message(input_text)

            

    #         # Handle the response structure
    #         if hasattr(response, 'result'):
    #             generated_content = response.result.candidates[0].content.parts[0].text
    #         elif hasattr(response, '_result'):
    #             generated_content = response._result.candidates[0].content.parts[0].text
    #         else:
    #             logging.error("Response object does not have the expected structure.")
    #             raise CustomException("Unexpected response structure")
            
    #         if generated_content.startswith("```json"):
    #             generated_content = generated_content[len("```json"):].strip()  # Remove the `'''json` prefix
                
    #         if generated_content.endswith("```"):
    #             generated_content = generated_content[:-len("```")].strip()  # Remove trailing `'''`
                
            
    #         generated_content = json.loads(generated_content)

    #         print(generated_content)

    #         print(type(generated_content))
            

    #         # response_data = json.loads(generated_content.strip('```json\n').strip('```'))

    #         # Extract missing keywords
    #         # Retrieve missing keywords
    #         missing_keywords = generated_content.get("MissingKeywords", [])
    #         if not isinstance(missing_keywords, list):
    #             missing_keywords = [missing_keywords]

    #         # Log the missing keywords
    #         logging.info(f"Missing keywords identified: {', '.join(missing_keywords)}")
    #         resume_text = resume_text.replace("\u2013", "-")  # Replace en dash with regular dash


    #         # Step 3: Update the resume text with missing keywords
    #         logging.info("Updating the resume with missing keywords.")
    #         updated_resume_text = analyzer.update_resume(resume_text, missing_keywords)

    #         # Step 4: Overwrite the original PDF with updated content
    #         logging.info(f"Overwriting the original resume PDF: {resume_pdf}")
    #         analyzer.create_pdf_from_text(updated_resume_text, resume_pdf)

    #         logging.info(f"Updated resume saved to {resume_pdf}")

    #         # Optionally save a separate updated copy
    #         if output_pdf:
    #             logging.info(f"Saving a copy of the updated resume to: {output_pdf}")
    #             analyzer.create_pdf_from_text(updated_resume_text, output_pdf)

    #         return resume_pdf

    #     except Exception as e:
    #         logging.error("Error while updating the resume.", exc_info=True)
    #         raise CustomException(f"Error in auto_update_resume: {e}")










