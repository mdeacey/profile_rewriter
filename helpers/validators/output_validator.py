import logging
import re
from difflib import SequenceMatcher
from helpers.calculators.token_cost_estimator import increment_tokens

log = logging.getLogger(__name__)

def standardize_text(text):
    return re.sub(r'[.,!?;]*$', '', text.strip().lower())

def are_texts_similar(text1, text2, threshold=0.95):
    return SequenceMatcher(None, text1, text2).ratio() > threshold

def update_output(output_texts, index, new_text, unique_outputs):
    output_texts[index] = new_text
    unique_outputs.add(standardize_text(new_text))
    log.debug(f"Updated output_texts[{index}]: {new_text}")

def check_and_update_uniqueness(new_outputs, tokens_per_output, non_unique_indices, output_texts, tokens_tracker, unique_outputs, parameters):
    still_non_unique_indices = []
    for idx, non_unique_idx in enumerate(non_unique_indices):
        output_text = new_outputs[idx]
        standardized_text = standardize_text(output_text)
        increment_tokens(tokens_tracker, non_unique_idx, tokens_per_output[idx])
        if standardized_text not in unique_outputs:
            if all(not are_texts_similar(output_text, existing_text) for existing_text in unique_outputs):
                update_output(output_texts, non_unique_idx, output_text, unique_outputs)
            else:
                still_non_unique_indices.append(non_unique_idx)
        else:
            still_non_unique_indices.append(non_unique_idx)
    return still_non_unique_indices

def validate_sentence_limit(output_texts, sentence_limit):
    log.info(f"Starting validation of sentence limit: {sentence_limit}...")
    if sentence_limit == '∞':
        log.info("No sentence limit provided or limit set to '∞', skipping validation.")
        return None

    def process_output_text(text, limit):
        sentences = re.split(r'[.!?](?:\s|$)', text)
        sentences = [sentence for sentence in sentences if sentence.strip()]
        log.debug(f"Processed text into {len(sentences)} sentences: {sentences}")
        return len(sentences) <= limit

    for index, text in enumerate(output_texts, start=1):
        if not process_output_text(text, sentence_limit):
            error_message = f"Output {index} exceeds the sentence limit of {sentence_limit}."
            log.error(error_message)
            return error_message

    log.info(f"All generated texts adhere to the sentence limit of {sentence_limit}.")
    return None

def validate_output_texts(output_texts, parameters):
    log.info("Starting validation of output texts...")
    log.info(f"{len(output_texts)} outputs successfully validated for the expected {parameters['num_outputs']} outputs.")
    if parameters['sentence_limit'] != '∞':
        log.info(f"Validating sentence limit of {parameters['sentence_limit']}...")
        error_message = validate_sentence_limit(output_texts, parameters['sentence_limit'])
        if error_message:
            log.error(f"Validation failed during sentence limit check: {error_message}")
            return None, None, error_message
    log.info("All output texts successfully passed validation.")
    return None
