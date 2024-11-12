# Profile Rewriter

The Profile Rewriter application is a Flask-based web tool designed to enhance and reformat text profiles using AI. The tool leverages the OpenAI API for generating rewritten content, providing options to customize tone, dialect, and formality. It includes a robust set of features, including API key validation, dynamic error handling, and Dockerized deployment for ease of use.

## Features

- **Text Profile Rewriting**: Enhance and format text using AI-powered tools.
- **API Key Validation**: Validate and securely store OpenAI API keys in sessions.
- **Dynamic Logging**: Adjustable logging levels via the `LOG_LEVEL` environment variable.
- **Error Handling**: User-friendly error messages with fallback mechanisms.
- **Dockerized Deployment**: Containerized setup using Docker and Docker Compose.
- **Production Ready**: Configured for scalable deployment with Gunicorn and Render.

## Directory Structure

```
./
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore rules
├── app.py                 # Main Flask application
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Dockerfile for building the application
├── render.yml            # Render deployment configuration
├── requirements.txt       # Python dependencies
├── static/               # Static assets (CSS, JavaScript, JSON)
│   ├── css/              # Stylesheets
│   ├── js/               # Client-side scripts
│   └── json/             # Mapping files for text processing
└── templates/            # HTML templates for the web interface
```

### Key Directories and Files

**Static Assets (/static)**:
- CSS: Contains modular stylesheets for specific components of the UI
- JavaScript: Client-side scripts for dynamic functionality
- JSON: Mapping files for text processing

**Templates (/templates)**:
- Modular HTML templates for constructing the user interface
- Includes reusable partials such as headers, footers, and form sections

**Configuration Files**:
- `.env.example`: Template for defining environment variables
- `docker-compose.yml`: Configuration for containerized deployment
- `render.yml`: Pre-configured settings for deploying on Render

**Python Files**:
- `app.py`: Main entry point for the Flask application
- `utility.py`: Handles logging, app initialization, and global utility functions
- `params.py`: Manages application parameters and logging updates

## Installation

### Prerequisites

Before installing the Profile Rewriter application, ensure you have the following tools and software installed:

- **Python**: Version 3.9 or higher
- **Docker and Docker Compose**: For containerized deployment
- **pip**: Python package manager for dependency installation

### Local Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   ```bash
   cp .env.example .env
   ```

4. **Run the Application**:
   ```bash
   flask run --host=0.0.0.0 --port=5001
   ```
   The app will be available at http://localhost:5001.

### Docker Setup

1. **Build and Run the Container**:
   ```bash
   docker-compose up --build
   ```

2. **Access the App**: Open your browser and visit http://localhost:5001.

### Deployment on Render

1. Push the Repository to GitHub
2. Connect to Render and link the repository
3. Render will automatically build and deploy based on `render.yml`

## Configuration

### Environment Variables

| Key | Description | Default Value |
|-----|-------------|---------------|
| `FLASK_ENV` | Specifies the environment mode (`development`, `production`) | `development` |
| `LOG_LEVEL` | Sets the logging level (`DEBUG`, `INFO`, `WARNING`, etc.) | `DEBUG` |

### Logging Configuration

Logging levels are dynamically managed via the `LOG_LEVEL` environment variable:
- `DEBUG`: For development and debugging purposes
- `INFO`: For general informational logs
- `WARNING`: For non-critical issues

## JavaScript Functionality

The client-side behavior is powered by a modular JavaScript structure in the `static/js` directory.

### Form Management System Components

### 1. TextareaManager
Handles all textarea interactions and behaviors, ensuring seamless user interaction and accessibility.

#### Focus Management
- Highlights text on focus for easier editing
- Displays navigation shortcuts when a textarea is active and hides them on blur

#### Clipboard Integration
- Adds functionality for copying textarea content to the clipboard
- Automatically toggles the visibility of copy buttons based on textarea content

#### Text Highlighting
- Automatically selects all text in the textarea on focus for quick editing

#### Event Listeners
- Manages custom blur handling to prevent unintended behavior (e.g., when interacting with a copy button)
- Ensures every textarea has relevant event listeners for navigation and copy functionality

### 2. ButtonManager
Manages all button-related behaviors and interactions for consistent user experience.

#### Press Simulation
- Adds animations to simulate button presses with smooth transitions

#### State Management
- Prevents rapid repeated clicks with built-in safeguards
- Handles both click and touch events for cross-device compatibility

#### Logging Integration
- Tracks button interactions for better debugging and analytics

### 3. FormNavigationManager
Enhances keyboard navigation, accessibility, and error handling for form elements.

#### Keyboard Navigation
- Supports arrow key navigation between form fields, including textareas and input elements
- Allows number key navigation to quickly jump to specific output fields

#### Enter Key Behavior
- Prevents unintended form submissions when pressing Enter in dropdowns
- Triggers form submission with the Enter key elsewhere

#### Error Handling
- Automatically focuses and scrolls to fields with validation errors

#### Shortcut Support
- Enables clicking on navigation shortcuts for direct access to specific form sections

#### Smart Initial Focus
- Directs focus to the most relevant element based on validation errors, current context, or form state

### 4. LoadingManager
Handles all aspects of loading state visualization and progress tracking for better user feedback.

#### Progress Tracking
- Updates progress bars and messages dynamically during multi-step operations
- Provides real-time elapsed time and step-based progress percentage

#### Step Management
- Manages sequential execution of tasks with optional delays between steps
- Allows infinite steps for processes like finalization

#### Visual Feedback
- Customizable progress bar with percentage display
- Displays meaningful messages during each step of the process

#### Operation Control
- Supports operation cancellation and recovery from failures
- Handles timeouts for long-running processes

### 5. FormManager
Centralizes form behavior management, including validation, cookies, and URL parameter synchronization.

#### Data Persistence
- Automatically syncs form data with cookies for persistent states
- Updates URL parameters in real-time for shareable form states

#### Real-time Validation
- Dynamically updates dependent fields like uniqueness attempts based on input length
- Allows cross-field validation and maintains validation states

#### Field Interactions
- Adds listeners for input changes to maintain synchronization across cookies, URL parameters, and form fields

#### Custom Logic
- Implements intelligent adjustments for fields like `uniqueness_attempts` based on the content length

### General Features Across Managers

#### Logging Integration
- Comprehensive logging at different levels (`debug`, `info`, `warn`, `error`, `critical`) for easier debugging and system monitoring

#### Event-Driven Architecture
- Modular design ensures managers are independent yet cohesive
- Easy to extend and customize for additional functionality

### Initialization
All managers are initialized on page load to ensure full functionality:

```javascript
window.addEventListener('DOMContentLoaded', () => {
    TextareaManager.init();
    ButtonManager.init();
    LoadingManager.init();
    FormNavigationManager.init();
    FormManager.init();
    log.info('All managers initialized.');
});
```

## Python Helpers

The Python helpers are organized into modular files, each specializing in specific functionality. 

### Directory Structure
```
helpers/
├── calculators/
│   └── token_cost_estimator.py
├── generators/
│   ├── __init__.py
│   └── output_generator.py
├── loaders/
│   ├── __init__.py
│   └── mapping_file_loader.py
├── processors/
│   ├── __init__.py
│   ├── casual_chat_formattor.py
│   ├── dialect_mapper.py
│   └── greetings_signoffs_remover.py
├── requestors/
│   ├── __init__.py
│   └── openai_api_requestor.py
├── validators/
│   ├── __init__.py
│   ├── api_key_validator_storer.py
│   ├── form_validator.py
│   └── output_validator.py
├── __init__.py
├── params.py
└── utility.py
```

### Business Logic Components

### 1. Token Calculator (`helpers/calculators/token_cost_estimator.py`)
Handles token management and cost estimation for text generation tasks.

#### Token Distribution:
- Ensures even token distribution across multiple outputs
- Adds safety buffers to maintain quality across outputs

#### Cost Calculation:
- Provides real-time cost estimates for each output and overall usage
- Handles model-specific rates

#### Usage Tracking:
- Tracks and logs token usage for better transparency

### 2. Output Generator (`helpers/generators/output_generator.py`)
Manages the generation and post-processing of text outputs using AI models.

#### Prompt Engineering:
- Dynamically constructs prompts based on user parameters like tone, formality, and dialect

#### Output Processing:
- Applies transformations such as greeting removal, dialect mapping, and casual formatting
- Validates outputs for quality and uniqueness

#### Error Handling:
- Gracefully manages connectivity issues and model errors
- Logs and retries failed attempts where applicable

### 3. Mapping File Loader (`helpers/loaders/mapping_file_loader.py`)
Provides efficient file loading and caching for JSON-based mappings used in text processing.

#### File Management:
- Loads JSON files atomically to prevent corruption
- Caches files for improved performance

#### Error Handling:
- Detects and logs missing or corrupted files
- Raises exceptions for unresolvable issues

### 4. Text Processors

#### a. Casual Formatter (`helpers/processors/casual_chat_formattor.py`)
Transforms formal text into a casual style suitable for informal communication.

##### Text Transformation:
- Removes unnecessary punctuation and simplifies sentence structures
- Incorporates slang using a predefined mapping file

##### Readability Improvements:
- Formats sentences for improved readability

#### b. Dialect Mapper (`helpers/processors/dialect_mapper.py`)
Converts text between dialects like American, British, and Australian English.

##### Dialect Conversion:
- Applies word replacements for spelling and vocabulary differences
- Uses JSON files for customizable mappings

##### Extensibility:
- Supports adding new dialects through external files

#### c. Greeting and Signoff Remover (`helpers/processors/greetings_signoffs_remover.py`)
Removes greetings and signoffs from text for cleaner outputs.

##### Pattern Matching:
- Uses predefined patterns loaded from JSON files to identify and remove greetings/signoffs

##### Customization:
- Supports user-defined patterns for additional flexibility

### 5. Validators

#### a. API Key Validator (`helpers/validators/api_key_validator_storer.py`)
Validates and securely stores OpenAI API keys.

##### Validation:
- Verifies keys with OpenAI services
- Ensures rate limit compliance and model access

##### Security:
- Stores keys in sessions for secure access
- Logs all key-related actions for auditing

#### b. Form Validator (`helpers/validators/form_validator.py`)
Validates user inputs to ensure they meet the application's requirements.

##### Input Validation:
- Checks text inputs for word count and meaningfulness
- Validates numerical fields like output count and sentence limits

##### Error Management:
- Provides user-friendly error messages

#### c. Output Validator (`helpers/validators/output_validator.py`)
Validates generated outputs for quality and uniqueness.

##### Uniqueness Checks:
- Compares outputs to ensure they are distinct

##### Sentence Limit Validation:
- Ensures outputs adhere to the specified sentence limit

## Contributing

### How to Contribute

1. **Fork and Clone**:
   ```bash
   git clone <your-fork-url>
   cd <repository-name>
   ```

2. **Set Up Development Environment**:
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   ```

3. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes and Test**:
   ```bash
   pytest
   ```

5. **Commit and Push**:
   ```bash
   git add .
   git commit -m "Add feature: description"
   git push origin feature/your-feature-name
   ```

### Guidelines

- Follow PEP 8 for Python code style
- Write tests for new features
- Update documentation as needed
- Use clear commit messages

## License

Licensed under the MIT License.

### MIT License Terms

Permission is granted, free of charge, to use, modify, and distribute the software, subject to:
- Including the copyright notice in all copies
- Software provided "as is" without warranty
- Authors not liable for any claims or damages

### Contributions and Licensing

All contributions are licensed under the MIT License.