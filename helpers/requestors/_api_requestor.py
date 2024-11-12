import logging
import json
from urllib import error, request

log = logging.getLogger(__name__)

def make_api_request(url, api_key=None, method="GET", data=None, headers=None, timeout=10):
    log.info(f"Initiating API request to {url} with method {method}.")
    if headers is None:
        headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    req = request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode("utf-8")
        log.debug(f"Request payload: {data}")
    try:
        with request.urlopen(req, timeout=timeout) as response:
            response_data = json.loads(response.read())
            log.info("API request successful.")
            log.debug(f"Response data: {response_data}")
            return response_data
    except error.HTTPError as e:
        log.error(f"HTTP error {e.code}: {e.reason}")
        raise
    except error.URLError as e:
        log.error(f"URL error: {e.reason}")
        raise
    except Exception as e:
        log.error(f"Unexpected error during API request: {str(e)}")
        raise
