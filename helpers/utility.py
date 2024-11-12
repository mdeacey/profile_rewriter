from dotenv import load_dotenv
import os
import logging

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[95m',
    }
    RESET = '\033[0m'

    def format(self, record):
        if record.levelname == 'ERROR' and not record.msg.startswith("Error:"):
            record.msg = f"Error: {record.msg}"
        log_color = self.COLORS.get(record.levelname, self.RESET)
        log_msg = super().format(record)
        return f"{log_color}{log_msg}{self.RESET}"

def utility_processor():
    log.debug("Registering utility processor for Jinja templates.")
    return dict(enumerate=enumerate)

class ExcludeMessageFilter(logging.Filter):
    def __init__(self, *exclude_messages):
        self.exclude_messages = exclude_messages

    def filter(self, record):
        return not any(exclude_message in record.getMessage() for exclude_message in self.exclude_messages)

def init_logging(level=logging.INFO):
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    exclude_filter = ExcludeMessageFilter("POST /log HTTP/1.1")
    
    if not root_logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.NOTSET)
        console_handler.addFilter(exclude_filter)
        formatter = ColoredFormatter(
            "%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    root_logger.info("Logging is successfully initialized with color and error prefix support.")

def init_app(app):
    log.info("Starting application initialization...")
    log.info("Loading environment variables from .env file...")
    try:
        load_dotenv()
        log.debug("Environment variables loaded successfully.")
    except Exception as e:
        log.error(f"Failed to load environment variables: {e}")
    environment = os.getenv("ENVIRONMENT", "development")
    log_level = logging.INFO if environment == "production" else logging.DEBUG
    init_logging(level=log_level)
    log.info("Setting Flask configuration for environment and secret key...")
    app.config['ENVIRONMENT'] = environment
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
    log.debug(f"Flask environment set to: {app.config['ENVIRONMENT']}")
    log.debug("Flask secret key configured.")
    log.info("Configuring Flask session settings...")
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 604800
    app.config['SESSION_TYPE'] = 'filesystem'
    log.debug(f"Session permanent: {app.config['SESSION_PERMANENT']}")
    log.debug(f"Session lifetime (seconds): {app.config['PERMANENT_SESSION_LIFETIME']}")
    log.debug(f"Session type: {app.config['SESSION_TYPE']}")
    log.info("Adding utility processor to Flask's context processors...")
    app.context_processor(utility_processor)
    log.debug("Utility processor added successfully.")
    log.info("Application initialization completed successfully.")

log = logging.getLogger(__name__)
