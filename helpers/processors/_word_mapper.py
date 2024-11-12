import logging
from helpers.processors._mapping_file_loader import load_mapping_file

log = logging.getLogger(__name__)

def map_words(output_text, mapping_file_path):
    """
    Maps words in the text using a JSON mapping file.

    Args:
        output_text (str): The text to process.
        mapping_file_path (str): The relative path to the JSON mapping file.

    Returns:
        str: The processed text.
    """
    log.info(f"Starting word mapping using file: {mapping_file_path}")

    # Load mapping from JSON
    mapping = load_mapping_file(mapping_file_path)
    log.debug(f"Loaded mapping: {mapping}")

    words = output_text.split()
    mapped_words = [
        mapping.get(word.lower(), word).capitalize() if word[0].isupper() else mapping.get(word.lower(), word)
        for word in words
    ]

    output_text = ' '.join(mapped_words)
    log.debug(f"Mapped words: {output_text}")
    log.info("Word mapping completed.")
    return output_text
