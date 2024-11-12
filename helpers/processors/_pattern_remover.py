import re
import logging
from helpers.processors._mapping_file_loader import load_mapping_file

log = logging.getLogger(__name__)

def remove_patterns(output_text, rules_source):
    """
    Removes text fragments matching regex patterns with specified replacements.

    Args:
        output_text (str): The text to process.
        rules_source (str | list): A list of tuples (regex_pattern, replacement), 
                                   or the file path to a JSON file containing regex patterns.

    Returns:
        str: The processed text.
    """
    log.info("Starting pattern removal...")

    # Load patterns from a JSON file if a string (file path) is provided
    if isinstance(rules_source, str):
        log.info(f"Loading pattern rules from file: {rules_source}")
        pattern_rules = load_mapping_file(rules_source)
        # Transform JSON list into [(pattern, replacement)] format
        rules_source = [(pattern, '') for pattern in pattern_rules]
    else:
        log.debug(f"Using provided pattern rules: {rules_source}")

    # Apply each rule
    for pattern, replacement in rules_source:
        log.debug(f"Applying pattern rule: '{pattern}' -> '{replacement}'")
        compiled_pattern = re.compile(pattern, flags=re.IGNORECASE)
        output_text, count = compiled_pattern.subn(replacement, output_text)
        if count > 0:
            log.info(f"Pattern '{pattern}' removed {count} instance(s).")

    output_text = output_text.strip()
    log.debug(f"Final text after pattern removal: {output_text}")
    log.info("Pattern removal completed.")
    return output_text
