import logging
import re
from helpers.validators.api_key_validator_storer import validate_store_api_key

log = logging.getLogger(__name__)

def is_input_gibberish(input_text):
    GIBBERISH_THRESHOLD = 0.5
    REPEATED_CHARS_THRESHOLD = 0.4
    word_list = re.findall(r'\b\w+\b', input_text)
    if not word_list:
        return True
    gibberish_count = 0
    for word in word_list:
        repeated_char_ratio = len(set(word)) / len(word)
        if repeated_char_ratio < REPEATED_CHARS_THRESHOLD:
            gibberish_count += 1
            continue
        if len(re.findall(r'[aeiou]', word, re.IGNORECASE)) < 1 and len(word) > 3:
            gibberish_count += 1
    return gibberish_count / len(word_list) > GIBBERISH_THRESHOLD

def is_name_gibberish(name):
    REPEATED_CHARS_THRESHOLD = 0.4
    repeated_char_ratio = len(set(name)) / len(name)
    if repeated_char_ratio < REPEATED_CHARS_THRESHOLD:
        return True
    if len(re.findall(r'[aeiou]', name, re.IGNORECASE)) < 1 and len(name) > 3:
        return True
    return False

def validate_name(name):
    log.info(f"Starting name validation: '{name}'...")
    cleaned_name = name.strip()
    if not cleaned_name:
        log.info("Responder name is empty, skipping validation.")
        return cleaned_name, None
    if not re.match(r"^[A-Za-z\s\-]+$", cleaned_name):
        log.error(f"Invalid name format: '{name}'")
        return None, "Invalid name format. Please provide a valid name with only letters, spaces, or hyphens."
    if len(cleaned_name) < 2:
        log.error(f"Name is too short: '{name}'")
        return None, "Name is too short. Please provide a valid name."
    if is_name_gibberish(cleaned_name):
        log.error(f"Name appears to be gibberish: '{name}'")
        return None, "Name appears to contain nonsensical characters. Please provide a more meaningful name."
    log.info(f"Name format is valid: '{name}'")
    return cleaned_name, None

def validate_num_outputs(num_outputs):
    log.info(f"Starting num_outputs validation: '{num_outputs}'...")
    try:
        num_outputs = int(num_outputs)
        if num_outputs > 10:
            log.warning(f"Number of outputs {num_outputs} exceeds the maximum allowed (10). Defaulting to 10.")
            return 10, "Number of responses exceeds the maximum allowed (10). Defaulting to 10."
        if num_outputs < 1:
            log.error(f"Invalid num_outputs value: {num_outputs}, defaulting to 1.")
            return 1, "Invalid number of responses. Please provide a valid number (greater than 0). Defaulting to 1."
        log.info(f"Number of outputs set to: {num_outputs}")
        return num_outputs, None
    except ValueError:
        log.error(f"Invalid num_outputs '{num_outputs}', defaulting to 1.")
        return 1, "Invalid number of responses. Please provide a valid number (greater than 0). Defaulting to 1."

def validate_sentence_limit(sentence_limit):
    log.info(f"Starting sentence_limit validation: '{sentence_limit}'...")
    if not sentence_limit or sentence_limit.lower() == 'unlimited':
        log.info("Sentence limit is set to unlimited or not provided.")
        return '∞', None
    try:
        sentence_limit = int(sentence_limit)
        if sentence_limit < 1:
            log.error(f"Invalid sentence_limit: {sentence_limit}. Defaulting to no limit.")
            return 'None', "Sentence limit must be a positive integer. Defaulting to no limit (None)."
        log.info(f"Sentence limit set to: {sentence_limit}")
        return sentence_limit, None
    except ValueError:
        log.error(f"Invalid sentence_limit '{sentence_limit}'. Defaulting to no limit.")
        return '∞', None

def validate_input_text(input_text):
    log.info(f"Starting input_text validation: '{input_text}'...")
    if not input_text or not input_text.strip():
        log.error("Input text is empty or blank after stripping.")
        return None, "Input cannot be blank. Please try again."
    cleaned_input = input_text.strip()
    word_count = len(cleaned_input.split())
    if word_count < 2:
        log.error(f"Input text contains less than 2 words: '{cleaned_input}'")
        return None, "Input must contain at least two words. Please provide more detailed text."
    if is_input_gibberish(cleaned_input):
        log.error("Input text appears to be gibberish.")
        return None, "Input contains too many nonsensical words. Please use more meaningful text."
    log.info("Input text is valid.")
    return cleaned_input, None

def validate_api_key_format(api_key):
    log.info(f"Starting API key format validation: '{api_key}'...")
    if not api_key:
        log.error("No API key provided.")
        return "An OpenAI API key is required to use this tool. Please provide your key and try again."
    if not re.match(r'^sk-[\w-]+$', api_key):
        log.error(f"Invalid API key format: '{api_key}'")
        return "Invalid API key format. The key should start with 'sk-' followed by alphanumeric characters and hyphens."
    log.info("API key format is valid.")
    return None

def validate_creativity(creativity):
    log.info(f"Starting creativity validation: '{creativity}'...")
    creativity_mapping = {'low': 0.5, 'med': 0.7, 'high': 0.9}
    creativity_value = creativity_mapping.get(creativity, 0.7)
    log.info(f"Creativity value set to: {creativity_value}")
    return creativity_value, None

def validate_uniqueness_attempts(uniqueness_attempts):
    log.info(f"Starting uniqueness_attempts validation: '{uniqueness_attempts}'...")
    try:
        uniqueness_attempts = int(uniqueness_attempts)
    except ValueError:
        log.error(f"Invalid uniqueness_attempts '{uniqueness_attempts}', defaulting to 5.")
        return 5, "Invalid uniqueness attempts. Please provide a valid number between 1 and 10. Defaulting to 5."
    if uniqueness_attempts > 10:
        log.warning(f"Number of uniqueness attempts {uniqueness_attempts} exceeds the maximum allowed (10). Defaulting to 10.")
        return 10, "Number of uniqueness attempts exceeds the maximum allowed (10). Defaulting to 10."
    if uniqueness_attempts < 1:
        log.warning(f"Number of uniqueness attempts {uniqueness_attempts} is less than the minimum allowed (1). Defaulting to 1.")
        return 1, "Number of uniqueness attempts is less than the minimum allowed (1). Defaulting to 1."
    log.info(f"Uniqueness attempts set to: {uniqueness_attempts}")
    return uniqueness_attempts, None

def validate_form_params(parameters):
    log.info("Starting form parameter validation...")
    api_key_message = validate_store_api_key(parameters['api_key'])
    if api_key_message:
        log.error(f"API key validation error: {api_key_message}")
        return parameters, {'api_key': api_key_message}
    parameters['responder_name'], name_message = validate_name(parameters['responder_name'])
    parameters['creativity'], creativity_message = validate_creativity(parameters['creativity'])
    parameters['num_outputs'], num_outputs_message = validate_num_outputs(parameters['num_outputs'])
    parameters['sentence_limit'], sentence_limit_message = validate_sentence_limit(parameters['sentence_limit'])
    parameters['input_text'], input_text_message = validate_input_text(parameters['input_text'])
    parameters['uniqueness_attempts'], uniqueness_attempts_message = validate_uniqueness_attempts(parameters.get('uniqueness_attempts', 5))
    error_messages = {
        'num_outputs': num_outputs_message,
        'sentence_limit': sentence_limit_message,
        'input_text': input_text_message,
        'responder_name': name_message,
        'api_key': api_key_message,
        'creativity': creativity_message,
        'uniqueness_attempts': uniqueness_attempts_message
    }
    return parameters, {k: v for k, v in error_messages.items() if v}
