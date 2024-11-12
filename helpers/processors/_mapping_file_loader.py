import os
import json
import logging
from flask import current_app

log = logging.getLogger(__name__)

def load_mapping_file(relative_path):
    # Resolve the file path based on the static folder
    file_path = os.path.join(current_app.static_folder, relative_path)
    log.info(f"Loading mapping file from: {file_path}")

    try:
        with open(file_path, 'r') as file:
            mapping = json.load(file)
            log.info(f"Mapping file loaded successfully with {len(mapping)} entries.")
            return mapping
    except FileNotFoundError:
        log.error(f"Mapping file not found at: {file_path}")
        raise
    except json.JSONDecodeError as e:
        log.error(f"Error decoding mapping JSON from {file_path}: {e}")
        raise
