import logging
from flask import Flask, session, render_template, flash, request, redirect, url_for, jsonify
from helpers.utility import init_app
from helpers.params import get_params, get_flashes
from helpers.validators.form_validator import validate_form_params
from helpers.generators.output_generator import generate_output_text
from helpers.validators.api_key_validator_storer import validate_store_api_key

log = logging.getLogger(__name__)

app = Flask(__name__)

init_app(app)

@app.route('/log', methods=['POST'])
def receive_log():
    try:
        data = request.json
        message = data.get('message', 'No message provided')
        level = data.get('level', 'info').lower()
        if level == 'debug':
            log.debug(message)
        elif level == 'info':
            log.info(message)
        elif level in {'warn', 'warning'}:
            log.warning(message)
        elif level == 'error':
            log.error(message)
        elif level == 'critical':
            log.critical(message)
        else:
            log.info(f"Unknown log level '{level}': {message}")
        return jsonify({"status": "success", "message": "Log received"}), 200
    except Exception as e:
        log.error(f"Error processing log: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def index():
    parameters = get_params()
    log.debug(f"Index route accessed. Parameters: {parameters}")
    excluded_keys = {'api_key', 'input_text', 'output_texts'}
    missing_params = {k: v for k, v in parameters.items() if k not in request.args and k not in excluded_keys}
    if missing_params:
        log.info(f"Missing parameters detected: {missing_params}. Redirecting to include them in the URL.")
        updated_url = url_for('index', **{**request.args, **missing_params})
        return redirect(updated_url)
    log.info(f"Rendering index page with parameters: {parameters}")
    return render_template('index.html', **parameters, **get_flashes())

@app.route('/submit', methods=['POST'])
def submit_text():
    log.debug("Submit route accessed via POST request.")
    session['output_success'] = False
    parameters = get_params()
    log.debug(f"Form parameters received: {parameters}")
    log.info("Starting API key validation...")
    error_messages = validate_store_api_key(parameters['api_key'])
    if error_messages:
        flash(error_messages, 'api_key')
        log.error(f"API key validation failed with error: {error_messages}")
        return render_template('index.html', **parameters, **get_flashes())
    log.info("API key validation passed. Proceeding to form validation.")
    parameters, validation_errors = validate_form_params(parameters)
    num_outputs_warning = validation_errors.pop('num_outputs', None)
    if any(validation_errors.values()):
        log.warning(f"Form validation returned errors: {validation_errors}")
        for category, message in validation_errors.items():
            flash(message, category)
        return render_template('index.html', **parameters, **get_flashes())
    if num_outputs_warning:
        flash(num_outputs_warning, 'num_outputs')
        log.info(f"Issue with number of outputs: {num_outputs_warning}")
    log.info("Proceeding to output generation.")
    try:
        parameters, output_texts, error_messages = generate_output_text(parameters)
    except Exception as e:
        fallback_error_message = "The OpenAI service is currently experiencing issues. Please try again later."
        log.error(f"Critical error during output generation: {str(e)}")
        flash(fallback_error_message, 'output_error')
        return render_template('index.html', **parameters, **get_flashes())
    if error_messages:
        for message in error_messages:
            flash(message, 'output_error')
        log.error(f"Errors during output generation: {error_messages}")
    filtered_outputs = [text if text else "" for text in output_texts]
    parameters['output_texts'] = filtered_outputs
    if not any(filtered_outputs):
        log.debug("All outputs are empty, rendering page with error messages.")
        return render_template('index.html', **parameters, **get_flashes())
    session['output_success'] = True
    log.debug("Session flag 'output_success' set to True.")
    log.info(f"Rendering result with generated output and error messages. Parameters: {parameters}")
    return render_template('index.html', **parameters, **get_flashes())

if __name__ == "__main__":
    app.run()
