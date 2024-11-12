/**
 * Parent Manager: TextareaManager
 * Handles all textarea-related behaviors like focus, highlight, navigation shortcuts, and copying to clipboard.
 */
const TextareaManager = {
    textAreas: [],
    apiKeyInput: null,

    init() {
        log.debug('TextareaManager: Initializing textarea behaviors.');
        this.textAreas = document.querySelectorAll('textarea[id^="inputTextarea"], textarea[id^="outputTextarea"]');
        this.apiKeyInput = document.getElementById('apiKeyInput');
        this.addTextareaListeners();
        this.addCopyListeners();
    },

    addTextareaListeners() {
        this.textAreas.forEach((textarea) => {
            textarea.addEventListener('focus', () => {
                this.showNavigationShortcuts(textarea.id);
                this.highlightTextareaText(textarea);
            });
    
            textarea.addEventListener('blur', (event) => {
                const relatedTarget = event.relatedTarget;
                if (relatedTarget && relatedTarget.id && relatedTarget.id.startsWith('copyBtn')) {
                    log.debug('TextareaManager: Blur event triggered by copy button, skipping hide.');
                    return;
                }
                setTimeout(() => {
                    this.hideNavigationShortcuts(textarea.id);
                }, 100);
            });
    
            log.debug(`TextareaManager: Event listeners added to textarea ${textarea.id}.`);
        });
    },    

    addCopyListeners() {
        this.textAreas.forEach((textarea) => {
            const copyBtn = document.getElementById(`copyBtn${textarea.id}`);
            
            if (copyBtn) {
                const toggleCopyButton = () => {
                    if (textarea.value.trim() === '') {
                        copyBtn.style.display = 'none';
                    } else {
                        copyBtn.style.display = 'block';
                    }
                };
    
                toggleCopyButton();
                textarea.addEventListener('input', toggleCopyButton);
                copyBtn.addEventListener('click', () => {
                    this.copyTextToClipboard(textarea.id);
                    log.debug(`Text copied from textarea with ID: ${textarea.id}`);
                });
            }
        });
    
        log.debug('TextareaManager: Copy button listeners added and visibility toggled.');
    },    

    copyTextToClipboard(textareaId) {
        try {
            const textarea = document.getElementById(textareaId);
            if (textarea) {
                textarea.select();
                textarea.setSelectionRange(0, textarea.value.length);
                navigator.clipboard.writeText(textarea.value).then(() => {
                    log.debug(`TextareaManager: Text in textarea ${textareaId} copied to clipboard.`);
                }).catch((err) => {
                    log.error(`TextareaManager: Failed to copy text from textarea ${textareaId} - ${err.message}`);
                });
            }
        } catch (error) {
            log.error(`TextareaManager: Error copying text to clipboard - ${error.message}`);
        }
    },

    highlightTextareaText(textarea) {
        try {
            log.debug(`TextareaManager: Highlighting text in textarea with id "${textarea.id}".`);
            textarea.select();
        } catch (error) {
            log.error(`TextareaManager: Error highlighting text in textarea - ${error.message}`);
        }
    },

    showNavigationShortcuts(textareaId) {
        log.debug(`TextareaManager: Showing navigation shortcuts for textarea ${textareaId}.`);
        const shortcuts = document.getElementById(`navigationShortcuts${textareaId}`);
        if (shortcuts) {
            shortcuts.style.display = 'flex';
        } else {
            log.warn(`TextareaManager: Navigation shortcuts not found for textarea ${textareaId}.`);
        }
    },
    
    hideNavigationShortcuts(textareaId) {
        log.debug(`TextareaManager: Hiding navigation shortcuts for textarea ${textareaId}.`);
        const shortcuts = document.getElementById(`navigationShortcuts${textareaId}`);
        if (shortcuts) {
            shortcuts.style.display = 'none';
        } else {
            log.warn(`TextareaManager: Navigation shortcuts not found for textarea ${textareaId}.`);
        }
    }
};