import logging
from flask import request, session, get_flashed_messages
from markupsafe import escape

log = logging.getLogger(__name__)

initial_params_logged = False
previous_params = {}

def get_api_key():
    # Prioritize API key from form, then session (but not URL).
    form_value = escape(request.form.get('api_key')) if request.form.get('api_key') else None
    if form_value:
        log.info("API key found in form, storing in session.")
        session['api_key'] = form_value
        return form_value
    
    api_key_session_value = escape(session.get('api_key')) if session.get('api_key') else None
    if api_key_session_value:
        log.info("API key found in session.")
        return api_key_session_value
    
    log.warning("API key not found in form or session.")
    return ''

def get_param_value(param_name, default_value=None):
    # Check URL parameters first, then form, then cookies.
    if param_name not in ['api_key', 'input_text', 'output_texts']:
        url_value = escape(request.args.get(param_name)) if request.args.get(param_name) else None
        if url_value:
            log.debug(f"Parameter '{param_name}' found in URL: {url_value}")
            return url_value

    form_value = escape(request.form.get(param_name)) if request.form.get(param_name) else None
    if form_value:
        log.debug(f"Parameter '{param_name}' found in form: {form_value}")
        return form_value

    cookie_value = escape(request.cookies.get(param_name)) if request.cookies.get(param_name) else None
    if cookie_value:
        log.debug(f"Parameter '{param_name}' found in cookie: {cookie_value}")
        return cookie_value

    log.debug(f"Parameter '{param_name}' not found, using default: {default_value}")
    return default_value if default_value else ''

def log_param_updates(params):
    global initial_params_logged, previous_params

    if not initial_params_logged:
        log.info(f"Initial parameters: {params}")
        previous_params = params.copy()
        initial_params_logged = True
    else:
        updated_params = {k: v for k, v in params.items() if k not in previous_params or previous_params[k] != v}
        if updated_params:
            log.info(f"Updated parameters: {updated_params}")
            previous_params.update(updated_params)

def get_params():
    params = {
        'api_key': get_api_key(),
        'responder_name': get_param_value('responder_name', ''),
        'dialect': get_param_value('dialect', 'american'),
        'formality': get_param_value('formality', 'neutral'),
        'tone': get_param_value('tone', 'neutral'),
        'channel': get_param_value('channel', 'chat'),
        'greetings': get_param_value('greetings', 'include'),
        'creativity': get_param_value('creativity', 'med'),
        'sentence_limit': get_param_value('sentence_limit', 'none'),
        'num_outputs': int(get_param_value('num_outputs', 1)),
        'uniqueness_attempts': get_param_value('uniqueness_attempts', 5),
        'input_text': get_param_value('input_text', ''),
        'output_texts': request.form.get('output_texts', []),
    }
    
    log_param_updates(params)
    
    return params

def get_flashes():
    flashes = {
        'api_key_messages': get_flashed_messages(category_filter=['api_key']),
        'num_outputs_messages': get_flashed_messages(category_filter=['num_outputs']),
        'sentence_limit_messages': get_flashed_messages(category_filter=['sentence_limit']),
        'input_text_messages': get_flashed_messages(category_filter=['input_text']),
        'output_error_messages': get_flashed_messages(category_filter=['output'])
    }
    
    # Add the 'Error:' prefix to all error messages if not already present
    for category, messages in flashes.items():
        flashes[category] = [f"Error: {message}" if not message.startswith("Error:") else message for message in messages]

    log.info(f"Flash messages retrieved: {flashes}")
    return flashes

