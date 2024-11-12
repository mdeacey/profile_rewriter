/**
 * Parent Manager: FormNavigationManager
 * Handles arrow key, number key navigation between form elements, and triggering submit with Enter key (except in dropdowns).
 * Also manages anchoring to and focusing on inputs with errors.
 */
const FormNavigationManager = {
    init() {
        log.debug('FormNavigationManager: Initializing form navigation.');
        this.handleArrowKeyNavigation();
        this.handleNumberKeyNavigation();
        this.handleEnterKeyForSubmission();
        this.handleShortcutClicks();
        this.setInitialFocus();
    },

    setInitialFocus() {
        try {
            const errorMessages = document.querySelectorAll('.error-message p');
            if (errorMessages.length > 0) {
                log.debug('FormNavigationManager: Found error messages. Focusing on the first input with an error.');
                const errorMap = {
                    'input-text-error': 'inputTextarea',
                    'output-error': 'outputTextarea1',
                    'sentence-limit-error': 'sentence_limit',
                    'num-outputs-error': 'num_outputs',
                    'api-key-error': 'apiKeyInput'
                };

                for (let [errorId, inputId] of Object.entries(errorMap)) {
                    const errorElement = document.getElementById(errorId);
                    if (errorElement && errorElement.textContent.trim()) {
                        const inputElement = document.getElementById(inputId);
                        if (inputElement) {
                            inputElement.focus();
                            inputElement.scrollIntoView({ block: 'center' });
                            log.debug(`FormNavigationManager: Focused on input with ID: ${inputId}`);
                            return;
                        }
                    }
                }
            }

            const apiKeyInput = document.getElementById('apiKeyInput');
            const inputTextarea = document.getElementById('inputTextarea');
            const firstOutputTextarea = document.getElementById('outputTextarea1');
            const apiKey = apiKeyInput && apiKeyInput.value.trim();
            const isSubmitURL = window.location.pathname === '/submit';

            if (!apiKey) {
                log.debug('FormNavigationManager: No API key found. Focusing on API key input.');
                if (apiKeyInput) {
                    apiKeyInput.focus();
                    apiKeyInput.scrollIntoView({ block: 'center' });
                }
            } else if (isSubmitURL && firstOutputTextarea) {
                log.debug('FormNavigationManager: URL is /submit. Focusing on the first output textarea.');
                firstOutputTextarea.focus();
                firstOutputTextarea.scrollIntoView({ block: 'center' });
            } else if (inputTextarea) {
                log.debug('FormNavigationManager: Focusing on input textarea.');
                inputTextarea.focus();
                inputTextarea.scrollIntoView({ block: 'center' });
            }

            log.debug('FormNavigationManager: Initial focus logic completed successfully.');
        } catch (error) {
            log.error(`FormNavigationManager: Error during initial focus - ${error.message}`);
        }
    },

    handleArrowKeyNavigation() {
        try {
            log.debug('FormNavigationManager: Setting up arrow key navigation.');
            const elements = this.getNavigableElements();
            const outputTextAreas = elements.slice(3);
            const hasOnlyOneOutput = outputTextAreas.length === 1;

            elements.forEach((element, index) => {
                element.addEventListener('keydown', (event) => {
                    if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
                        const activeElement = document.activeElement;
                        const isOutputTextareaActive = outputTextAreas.includes(activeElement);

                        if (hasOnlyOneOutput && event.key === 'ArrowDown' && isOutputTextareaActive) {
                            log.debug('FormNavigationManager: ArrowDown key uses default action because an output textarea is active and there is only one output.');
                            return;
                        }

                        if ((index === 0 && event.key === 'ArrowUp') || (index === elements.length - 1 && event.key === 'ArrowDown')) {
                            log.debug('FormNavigationManager: Arrow key at boundary element. Using default action.');
                            return;
                        }

                        event.preventDefault();
                        let targetIndex = event.key === 'ArrowUp' ? index - 1 : index + 1;
                        this.navigateToElement(targetIndex);
                    }
                });
            });
        } catch (error) {
            log.error(`FormNavigationManager: Error in arrow key navigation - ${error.message}`);
        }
    },

    handleNumberKeyNavigation() {
        try {
            log.debug('FormNavigationManager: Setting up number key navigation.');
            const elements = this.getNavigableElements();
            const outputTextAreas = elements.slice(3);
    
            if (outputTextAreas.length > 0) {
                document.addEventListener('keydown', (event) => {
                    const focusedElement = document.activeElement;
                    const isInNumberInputField = focusedElement && focusedElement.tagName === 'INPUT' && focusedElement.type === 'number';
                    if (isInNumberInputField) {
                        return;
                    }
                    if (event.key === '0') {
                        this.navigateToElement(2);
                    } else if (event.key >= '1' && event.key <= outputTextAreas.length.toString()) {
                        const targetIndex = parseInt(event.key, 10) - 1 + 3;
                        this.navigateToElement(targetIndex);
                    }
                });
            }
        } catch (error) {
            log.error(`FormNavigationManager: Error in number key navigation - ${error.message}`);
        }
    },

    handleEnterKeyForSubmission() {
        try {
            log.debug('FormNavigationManager: Setting up Enter key to trigger submit.');
            document.addEventListener('keydown', (event) => {
                const activeElement = document.activeElement;
                if (activeElement.tagName.toLowerCase() === 'select' && event.key === 'Enter') {
                    log.debug('FormNavigationManager: Enter key pressed in dropdown. Preventing submission.');
                    event.preventDefault();
                    return;
                }

                if (event.key === 'Enter') {
                    event.preventDefault();
                    log.debug('FormNavigationManager: Enter key pressed. Triggering submit.');
                    const submitButton = document.querySelector('.submit-btn');
                    if (submitButton) {
                        ButtonManager.simulateButtonPress(submitButton);
                        submitButton.click();
                    } else {
                        log.warn('FormNavigationManager: Submit button not found.');
                    }
                }
            });
        } catch (error) {
            log.error(`FormNavigationManager: Error setting up Enter key behavior - ${error.message}`);
        }
    },

    handleShortcutClicks() {
        window.handleShortcutClick = (index) => {
            this.navigateToElement(index);
        };
    },

    getNavigableElements() {
        const apiKeyInput = document.getElementById('apiKeyInput');
        const responderNameInput = document.getElementById('responder_name');
        const inputTextarea = document.getElementById('inputTextarea');
        const outputTextAreas = document.querySelectorAll('textarea[id^="outputTextarea"]');
        return [apiKeyInput, responderNameInput, inputTextarea, ...outputTextAreas];
    },

    navigateToElement(targetIndex) {
        try {
            const elements = this.getNavigableElements();
            const targetElement = elements[targetIndex];
            if (targetElement) {
                targetElement.focus();
                if (targetElement.tagName === 'TEXTAREA' || targetElement.tagName === 'INPUT') {
                    targetElement.select();
                }
                targetElement.scrollIntoView({ block: 'center' });
                log.debug(`FormNavigationManager: Navigated to element at index ${targetIndex}.`);
            } else {
                log.warn(`FormNavigationManager: Invalid target index ${targetIndex}. No element found.`);
            }
        } catch (error) {
            log.error(`FormNavigationManager: Error navigating to element - ${error.message}`);
        }
    }
};