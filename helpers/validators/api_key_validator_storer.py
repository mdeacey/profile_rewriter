import logging
from flask import session
from helpers.requestors.openai_api_requestor import make_api_request

log = logging.getLogger(__name__)

def validate_store_api_key(api_key):
    log.info("Validating API key...")

    if session.get('api_key_validated') and api_key == session.get('api_key'):
        log.info("API key already validated and stored in the session. No revalidation required.")
        return None

    from helpers.validators.form_validator import validate_api_key_format
    error_message = validate_api_key_format(api_key)
    if error_message:
        log.error(f"API key format validation failed: {error_message}")
        return error_message

    try:
        validate_openai(api_key)
        check_model_access(api_key)
        session['api_key'] = api_key
        session['api_key_validated'] = True
        log.info("API key stored in session and marked as validated.")
        return None
    except Exception as e:
        error_message = f"{str(e)}"
        log.error(f"API key validation failed: {error_message}")
        return error_message

def validate_openai(api_key):
    log.info("Validating API key with OpenAI...")
    make_api_request("https://api.openai.com/v1/models", api_key)
    log.info("API key validated successfully.")

def check_model_access(api_key):
    log.info("Checking access to GPT-4 model...")
    make_api_request("https://api.openai.com/v1/models/gpt-4", api_key)
    log.info("GPT-4 model access verified successfully.")
