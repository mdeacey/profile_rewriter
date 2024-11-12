from helpers.requestors._api_requestor import make_api_request
import logging

log = logging.getLogger(__name__)

def make_openai_request(url, api_key, method="POST", data=None):
    log.info("Preparing OpenAI API request...")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        return make_api_request(url, None, method, data, headers=headers)
    except Exception as e:
        log.error(f"OpenAI API request failed: {str(e)}")
        raise RuntimeError("The OpenAI service is experiencing issues. Please try again later.")
