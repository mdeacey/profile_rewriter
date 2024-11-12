import logging
from helpers.requestors.openai_api_requestor import make_openai_request
from helpers.calculators.token_cost_estimator import distribute_tokens, calculate_individual_cost, calculate_total_cost
from helpers.validators.output_validator import check_and_update_uniqueness, validate_output_texts
from helpers.processors.process_output_text import process_output_text

log = logging.getLogger(__name__)

def construct_prompt(parameters):
    log.info("Constructing the prompt...")
    prompt = (f"Rewrite the following text in {parameters['dialect']} English, using a {parameters['formality']} tone "
              f"and reflecting a {parameters['tone']} mood, tailored for a {parameters['channel']}.")
    if parameters.get('responder_name'):
        prompt += f" The person you're sending this message to is named {parameters['responder_name']}."
    if parameters['sentence_limit'] != '∞':
        prompt += f" Limit the output to {parameters['sentence_limit']} sentences."
    prompt += f" Text: {parameters['input_text']}"
    log.info("Prompt construction completed.")
    return prompt

def make_api_call(parameters, prompt, num_outputs_to_generate):
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "n": num_outputs_to_generate,
        "temperature": parameters['creativity'],
    }
    return make_openai_request(
        "https://api.openai.com/v1/chat/completions",
        parameters['api_key'],
        method="POST",
        data=data
    )

def process_api_response(api_response):
    log.info("Processing API response...")
    log.debug(f"Full API response: {api_response}")
    try:
        output_texts = [response['message']['content'].strip() for response in api_response['choices']]
        log.info("Extracted output texts successfully.")
        total_completion_tokens = api_response.get('usage', {}).get('completion_tokens', 0)
        tokens_per_output = [response.get('usage', {}).get('completion_tokens', 0) for response in api_response['choices']]
        log.debug(f"Initial tokens per output: {tokens_per_output}")
        tokens_per_output = distribute_tokens(tokens_per_output, total_completion_tokens)
        log.debug(f"Tokens after distribution: {tokens_per_output}")
        return output_texts, tokens_per_output
    except KeyError as e:
        log.error(f"KeyError while processing API response: {str(e)}")
        raise RuntimeError("There was an issue processing the model's response. Please try again later.")
    except Exception as e:
        log.error(f"Unexpected error while processing API response: {str(e)}")
        raise RuntimeError("An unexpected error occurred while generating the response. Please try again later.")

def handle_generation_error(parameters, output_texts, total_tokens_used, total_estimated_cost, errors, exception):
    error_message = str(exception)
    if "connectivity" in error_message:
        error_message = "The OpenAI service is currently experiencing connectivity issues. Please try again later."
    elif "processing" in error_message:
        error_message = "There was an issue processing the model's response. Please try again later."
    else:
        error_message = "An unexpected error occurred while generating the response. Please try again later."
    log.error(error_message)
    parameters.update({
        'output_texts': output_texts,
        'total_tokens_used': total_tokens_used,
        'total_estimated_cost': total_estimated_cost,
        'tokens_used': [],
        'estimated_cost': [0.0] * len(output_texts)
    })
    errors.append(error_message)

def generate_output_text(parameters):
    uniqueness_attempts = parameters.get('uniqueness_attempts', 5)
    max_retries = uniqueness_attempts if uniqueness_attempts != 'unlimited' else 5
    output_texts = [''] * parameters['num_outputs']
    tokens_tracker = [0] * parameters['num_outputs']
    unique_outputs = set()
    non_unique_indices = list(range(parameters['num_outputs']))
    errors = []
    total_tokens_used = 0
    total_estimated_cost = 0.0
    try:
        log.info("Generating output text...")
        prompt = construct_prompt(parameters)
        for attempt in range(max_retries):
            if not non_unique_indices:
                break
            num_outputs_to_generate = len(non_unique_indices)
            log.info(f"Attempt {attempt + 1}/{max_retries}: Requesting {num_outputs_to_generate} outputs.")
            api_response = make_api_call(parameters, prompt, num_outputs_to_generate)
            new_outputs, tokens_per_output = process_api_response(api_response)
            processed_outputs = [process_output_text(output, parameters) for output in new_outputs]
            non_unique_indices = check_and_update_uniqueness(
                processed_outputs, tokens_per_output, non_unique_indices, output_texts, tokens_tracker, unique_outputs, parameters
            )
            if not non_unique_indices:
                log.info(f"All outputs are unique after {attempt + 1} attempts.")
                break
        remaining_non_unique = len(non_unique_indices)
        if remaining_non_unique > 0:
            log.warning(f"Failed to generate entirely unique outputs after {max_retries} attempts. {remaining_non_unique} non-unique outputs exist.")
        validation_errors = validate_output_texts(output_texts, parameters)
        estimated_cost = calculate_individual_cost(tokens_tracker)
        total_tokens_used, total_estimated_cost = calculate_total_cost(tokens_tracker, estimated_cost)
        parameters.update({
            'output_texts': output_texts,
            'total_tokens_used': total_tokens_used,
            'total_estimated_cost': total_estimated_cost,
            'tokens_used': tokens_tracker,
            'estimated_cost': estimated_cost
        })
        return parameters, output_texts, errors if validation_errors is None else [validation_errors]
    except Exception as e:
        handle_generation_error(parameters, output_texts, total_tokens_used, total_estimated_cost, errors, e)
        return parameters, output_texts, errors