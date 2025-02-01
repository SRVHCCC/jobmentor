import json
from src.logger import logging
from src.exception import CustomException


class DATACLEAN:
    """
    A class for cleaning and extracting data from response objects.
    """

    def clean_data(self, response: object) -> dict:
        """
        Cleans and extracts specific fields from the provided response object.

        Args:
            response (object): The response object containing JSON text to be cleaned.

        Returns:
            dict: Extracted data including subject, introduction, alignment, interest,
                  call to action, and closing.

        Raises:
            CustomException: If an error occurs during the cleaning process.
        """
        try:
            # Log the start of the data cleaning process
            logging.info("Starting data cleaning process...")

            # Validate response structure
            if not response or not hasattr(response, "result"):
                raise CustomException("Invalid or missing 'result' in response object")

            # Extract JSON text from response
            try:
                generated_content = response.result.candidates[0].content.parts[0].text
            except AttributeError:
                logging.error("Response object does not have the expected structure.")
                raise CustomException("Unexpected response structure")

            # Clean and parse the JSON string
            json_text = generated_content.strip("```json\n").strip("```")
            try:
                parsed_data = json.loads(json_text)
            except json.JSONDecodeError as e:
                raise CustomException(f"Error parsing JSON: {str(e)}")

            # Extract fields
            subject = parsed_data.get("subject", "Subject not found")
            body = parsed_data.get("body", {})
            introduction = body.get("introduction", "Introduction not found")
            alignment = body.get("alignment", "Alignment not found")
            interest = body.get("interest", "Interest not found")
            call_to_action = body.get("call_to_action", "Call to action not found")
            closing = body.get("closing", "Closing not found")

            # Return extracted data
            return {
                "subject": subject,
                "introduction": introduction,
                "alignment": alignment,
                "interest": interest,
                "call_to_action": call_to_action,
                "closing": closing,
            }

        except CustomException as e:
            logging.error(f"Custom error occurred: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}")
            raise CustomException(f"Unexpected error: {str(e)}")
