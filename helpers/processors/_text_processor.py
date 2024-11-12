import re
import logging

log = logging.getLogger(__name__)

def process_text(output_text, rules, capitalize=False):
    """
    Processes text by applying a list of regex patterns with replacements.
    Optionally handles sentence capitalization.

    Args:
        output_text (str): The text to process.
        rules (list): A list of tuples (regex_pattern, replacement).
        capitalize (bool): Whether to capitalize the first letter of sentences. Defaults to False.

    Returns:
        str: The processed text.
    """
    log.info("Starting text processing with rules...")
    original_text = output_text

    # Apply regex rules
    for pattern, replacement in rules:
        log.debug(f"Applying processing rule: '{pattern}' -> '{replacement}'")
        output_text = re.sub(pattern, replacement, output_text)

    # Optionally capitalize sentences
    if capitalize:
        output_text = re.sub(r'(^\w)|([.!?]\s*\w)', lambda match: match.group(0).upper(), output_text)

    log.debug(f"Processed text from '{original_text}' to '{output_text}'")
    log.info("Text processing completed.")
    return output_text
