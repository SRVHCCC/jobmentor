import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.logger import logging
from src.exception import CustomException
from src.logger import logging

from PyPDF2 import PdfReader
import re

def load_env_variables():
    """Load environment variables from a .env file."""
    load_dotenv()

def configure_genai_api():
    """
    Configure the Google Generative AI (Gemini API).
    Returns the configured GenerativeModel instance or raises an exception.
    """
    # Load environment variables
    load_env_variables()

    # Retrieve API key from environment
    genai_api_key = os.getenv("GEMINI_API_KEY")
    if not genai_api_key:
        logging.error("API key for Google Generative AI is not set. Please check your .env file.")
        raise CustomException("GEMINI_API_KEY not found in environment variables")

    # Configure the GenAI API
    genai.configure(api_key=genai_api_key)

    # Define the generation configuration
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 1024,
        "response_mime_type": "text/plain",
    }

    try:
        # Create a GenerativeModel instance
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp", generation_config=generation_config
        )
        return model
    except Exception as e:
        logging.error(f"Failed to configure GenerativeModel: {str(e)}")
        raise CustomException(f"Failed to configure GenerativeModel: {str(e)}")
    



def start_chat_session(model):
    """
    Start a chat session with Google Generative AI.
    Returns the initialized chat session.
    """
    try:
        chat_session = model.start_chat(history=[])
        return chat_session
    except Exception as e:
        logging.error(f"Failed to initialize chat session: {str(e)}")
        raise CustomException(f"Failed to initialize chat session: {str(e)}")
    



def extract_text_from_pdf(uploaded_file):
    """
    Extract text from a PDF file.
    
    Args:
        uploaded_file: A file-like object containing the PDF file.
        
    Returns:
        A string containing the extracted text from the PDF. If extraction fails, raises an exception.
    """
    try:
        # Initialize a PDF reader
        reader = PdfReader(uploaded_file)
        
        # Accumulate text from all pages
        text = "".join(page.extract_text() or "" for page in reader.pages)
        
        # Return the extracted text, stripping leading and trailing spaces
        return text.strip()
    except Exception as e:
        logging.error(f"Failed to extract text from the PDF: {e}")
        raise CustomException(f"Failed to extract text from the PDF: {e}")
    




import pdfplumber

def extract_text_from_pdf_with_pdfplumber(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        clean_text = clean_extracted_text(text)

    return clean_text





def clean_extracted_text(raw_text):
    # Define section headers
    headers = [
        "Profile Summary", "Contact", "Academic Details", "Work Experience", 
        "Soft Skills", "Technical Skills", "Core Competencies", "Achievements", 
        "Academic Projects", "Personal Details"
    ]

    # Initialize a dictionary to hold sections
    sections = {}
    
    # Find and organize sections based on headers
    for i, header in enumerate(headers):
        start_idx = raw_text.find(header)
        if start_idx != -1:
            # Find the end of this section (next header or end of text)
            end_idx = min(
                [raw_text.find(h, start_idx + len(header)) for h in headers[i+1:] if raw_text.find(h, start_idx + len(header)) != -1] 
                + [len(raw_text)]
            )
            sections[header] = raw_text[start_idx:end_idx].strip()
    
    # Format the output
    formatted_output = "\n\n".join(f"{header}:\n{content}" for header, content in sections.items())
    return formatted_output

# Example usage




