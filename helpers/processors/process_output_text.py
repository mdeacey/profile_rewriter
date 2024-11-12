import logging
from helpers.processors._word_mapper import map_words
from helpers.processors._text_processor import process_text
from helpers.processors._pattern_remover import remove_patterns

log = logging.getLogger(__name__)

def process_output_text(output_text, parameters):
    log.info("Processing output text...")
    
    if parameters['greetings'] == 'exclude':
        output_text = remove_patterns(output_text, 'json/greeting_patterns.json')
        log.debug(f"Text after removing greetings: '{output_text}'")
        output_text = remove_patterns(output_text, 'json/signoff_patterns.json')
        log.debug(f"Text after removing sign-offs: '{output_text}'")
        
    if parameters['dialect'] in ['british', 'australian']:
        output_text = map_words(output_text, 'json/us_gb_spelling.json')
        log.debug(f"Text after applying spelling mapping: {output_text}")
        output_text = map_words(output_text, 'json/us_gb_vocabulary.json')
        log.debug(f"Text after applying vocabulary mapping: {output_text}")

    if parameters['formality'] == 'casual' and parameters['channel'] == 'chat':
        log.info("Starting casual text formatting...")

        processing_rules = [
            (r"\b(\w+)'(\w+)\b", r'\1\2'),  # Remove contractions
            (r'[;,]', ''),  # Remove commas and semicolons
            (r'(\w)[\-\u2013\u2014](\w)|\s*[\-\u2013\u2014]\s*', r'\1 \2'),  # Handle dashes
            (r"'(\w+)'", r'\1')  # Remove single quotes around words
        ]
        output_text = process_text(output_text, processing_rules)

        punctuation_rules = [
            (r'\s*([.!?])', r'\1'),  # Ensure no extra spaces before punctuation
            (r'\s+', ' ')  # Replace multiple spaces with a single space
        ]
        output_text = process_text(output_text, punctuation_rules, capitalize=True)

        output_text = map_words(output_text, 'json/text_slang.json')

        output_text = remove_patterns(output_text, 'json/greeting_patterns.json')
        output_text = remove_patterns(output_text, 'json/signoff_patterns.json')

        log.debug(f"Formatted text: '{output_text}'")
        log.info("Casual text formatting completed.")

    log.info("Output text processing completed.")
    return output_text